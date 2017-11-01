# -*- coding: utf-8 -*-
# @Date    : 2017/10/31
# @Author  : wqs
"""
    使用了wifi强度
"""

import collections
from datetime import datetime

from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec
from use_location import get_distance_by_latitude_and_longitude

'''
k=2 [LocationToVec2(), WifiToVec(), WifiKStrongToVec()] 0.9113118530195635
k= 1 [LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec()] 0.9142910658123108
k= 2 0.9142498942590803
k= 3 0.9136532388641382
'''


class WifiKStrongToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl')
        self.min_strong = -120
        self._WIFI_BSSID = None
        self.kstrong = 1

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
            tmp = [(_id, _strong, _connect) for _id, (_strong, _connect) in row.items()]
            tmp = sorted(tmp, key=lambda x: -x[1])[:self.kstrong]
            for i in range(len(tmp)):
                _id = wifi_bssid[tmp[i][0]]
                indices.append(i)
                data.append(tmp[i][1])
            # for _id, (_strong, _connect) in row.items():
            #     _id = wifi_bssid[_id]
            #     indices.append(_id)
            #     data.append(_strong)
            indptr.append(len(indices))

        wifi_features = csr_matrix((data, indices, indptr), shape=(len(train_data), self.kstrong),
                                   dtype=int)  # TODO normalize
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
            tmp = [(_id, _strong, _connect) for _id, (_strong, _connect) in row.items()]
            tmp = sorted(tmp, key=lambda x: -x[1])[:self.kstrong]
            for i in range(len(tmp)):
                _id = wifi_bssid[tmp[i][0]]
                indices.append(i)
                data.append(tmp[i][1])
            # for _id, (_strong, _connect) in row.items():
            #     _id = wifi_bssid[_id]
            #     indices.append(_id)
            #     data.append(_strong)
            indptr.append(len(indices))

        # print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
        wifi_features = csr_matrix((data, indices, indptr), shape=(len(test_data), self.kstrong), dtype=int)
        # TODO normalize
        return wifi_features


def train_test():
    task = ModelBase()
    task.train_test([WifiKStrongToVec()])
    # task.train_and_on_test_data([WifiToVec2()])


if __name__ == '__main__':
    train_test()
