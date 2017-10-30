# -*- coding: utf-8 -*-
# @Date    : 2017/10/25
# @Author  : hrwhisper
"""
    使用了wifi特征，类似BOW (本地：0.8942214814065961    提交：0.8951)
    update: 同一个用户可能检测多个相同的bssid，将这些bssid编号
    update2: 去除mobile hotspot，若某wifi只有某天出现，则判定为mobile hotspot.
    update3: 对于测试集中wifi信息为空的，选择经纬度最近的用户的wifi作为该用户的wifi信息（本地0.91358）
"""

import collections
from datetime import datetime

from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec
from use_location import get_distance_by_latitude_and_longitude


class WifiToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl')
        self.min_strong = -120
        self._WIFI_BSSID = None

    def _fit_transform(self, train_data, mall_id):
        wifi_and_date = collections.defaultdict(set)
        wifi_rows = []
        # 去除同一条记录中多个bssid
        for wifi_infos, _time in zip(train_data['wifi_infos'], train_data['time_stamp']):
            _time = datetime.strptime(_time, "%Y-%m-%d %H:%M")
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                wifi_and_date[_id].add(str(_time.date()))

        wifi_bssid = set()
        for wifi_infos in train_data['wifi_infos']:
            row = {}
            cur_wifi_len = len(wifi_infos.split(';'))
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                if len(wifi_and_date[_id]) < 2:
                    continue
                _strong = int(_strong) - self.min_strong
                if _id not in row:
                    row[_id] = [_strong, _connect == 'true']
                    wifi_bssid.add(_id)
                else:
                    for i in range(1, cur_wifi_len):
                        _t_id = _id + '_' + str(i)
                        if _t_id in row:
                            row[_t_id] = [_strong, _connect == 'true']
                            wifi_bssid.add(_t_id)
                            break

            wifi_rows.append(row)

        self._WIFI_BSSID = wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
        indptr = [0]
        indices = []
        data = []
        for row in wifi_rows:
            for _id, (_strong, _connect) in row.items():
                _id = wifi_bssid[_id]
                indices.append(_id)
                data.append(_strong)
            indptr.append(len(indices))

        wifi_features = csr_matrix((data, indices, indptr), dtype=int)  # TODO normalize
        return wifi_features

    def _transform(self, test_data, mall_id):
        wifi_bssid = self._WIFI_BSSID
        wifi_rows = []
        not_in = set()
        to_add = []
        for i, wifi_infos in enumerate(test_data['wifi_infos']):
            row = {}
            cur_wifi_len = len(wifi_infos.split(';'))
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                if _id not in wifi_bssid:
                    not_in.add(_id)
                    continue
                _strong = int(_strong) - self.min_strong
                if _id not in row:
                    row[_id] = [_strong, _connect == 'true']
                else:
                    for i in range(1, cur_wifi_len):
                        _t_id = _id + '_' + str(i)
                        if _t_id not in row and _t_id in wifi_bssid:
                            row[_t_id] = [_strong, _connect == 'true']
                            break
            if len(row) == 0:
                to_add.append(i)
            wifi_rows.append(row)

        # 找最近的不为空的wifi
        lats, logs = test_data['latitude'], test_data['longitude']
        for i in to_add:
            lat, log = lats.iat[i], logs.iat[i]
            dis = sorted([(get_distance_by_latitude_and_longitude(lat, log, lats.iat[j], logs.iat[j]), j)
                          for j in range(len(test_data)) if i != j])
            for d, j in dis:
                if len(wifi_rows[j]) != 0:
                    wifi_rows[i] = wifi_rows[j]
                    break

        indptr = [0]
        indices = []
        data = []
        for row in wifi_rows:
            for _id, (_strong, _connect) in row.items():
                _id = wifi_bssid[_id]
                indices.append(_id)
                data.append(_strong)
            indptr.append(len(indices))

        # print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
        wifi_features = csr_matrix((data, indices, indptr), shape=(len(test_data), len(wifi_bssid)), dtype=int)
        # TODO normalize
        return wifi_features


def train_test():
    task = ModelBase()
    task.train_test([WifiToVec()])
    # task.train_and_on_test_data([WifiToVec2()])


if __name__ == '__main__':
    train_test()
