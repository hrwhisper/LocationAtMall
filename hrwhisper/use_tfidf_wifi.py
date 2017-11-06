# -*- coding: utf-8 -*-
# @Date    : 2017/11/6
# @Author  : hrwhisper
"""
    使用了wifi特征，tf-idf
    好像没啥用
"""

import collections
from datetime import datetime

import math
from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec


class WifiTfIdfToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_tfidf_features_{}_{}.pkl')
        self.min_strong = -120
        self._WIFI_BSSID = None
        self._WIFI_TF_IDF = {}

    def _fit_transform(self, train_data, mall_id):
        wifi_and_date = collections.defaultdict(set)
        wifi_rows = []
        # 去除移动热点
        for wifi_infos, _time in zip(train_data['wifi_infos'], train_data['time_stamp']):
            _time = datetime.strptime(_time, "%Y-%m-%d %H:%M")
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                wifi_and_date[_id].add(str(_time.date()))

        wifi_bssid = set()
        wifi_df_cnt = collections.defaultdict(set)
        wifi_tf_cnt = collections.Counter()

        for wifi_infos, shop_id in zip(train_data['wifi_infos'], train_data['shop_id']):
            row = {}
            cur_wifi_len = len(wifi_infos.split(';'))
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                if len(wifi_and_date[_id]) < 2:
                    continue
                _strong = int(_strong) - self.min_strong
                wifi_tf_cnt[_id] += 1
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
            for _id in row.keys():
                wifi_df_cnt[_id].add(shop_id)
            wifi_rows.append(row)

        self._WIFI_BSSID = {_id: i for i, _id in
                            enumerate(sorted(set(wifi_df_cnt.keys()) & set(wifi_tf_cnt.keys())))}

        self._WIFI_TF_IDF = {
            key: wifi_tf_cnt[key] * math.log2(train_data.shape[0] / len(wifi_df_cnt[key])) for key in self._WIFI_BSSID
        }

        return self._transform(train_data, mall_id)

    def _transform(self, test_data, mall_id):
        wifi_bssid = self._WIFI_BSSID
        indptr = [0]
        indices = []
        data = []
        for wifi_infos in test_data['wifi_infos']:
            row = {}
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                if _id not in self._WIFI_TF_IDF: continue
                row[_id] = self._WIFI_TF_IDF[_id]

            norm = math.sqrt(sum(x ** 2 for x in row.values()))
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                if _id not in self._WIFI_TF_IDF: continue
                indices.append(wifi_bssid[_id])
                data.append(self._WIFI_TF_IDF[_id] * (int(_strong) - self.min_strong)) # / norm
            indptr.append(len(indices))

        # print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
        wifi_features = csr_matrix((data, indices, indptr), shape=(len(test_data), len(wifi_bssid)), dtype=int)
        # TODO normalize
        return wifi_features


def train_test():
    task = ModelBase()
    task.train_test([WifiTfIdfToVec()])
    # task.train_and_on_test_data([WifiToVec2()])


if __name__ == '__main__':
    train_test()
