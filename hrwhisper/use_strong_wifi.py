# -*- coding: utf-8 -*-
"""
    merge from @Peishichao.
    [LocationToVec(), WifiToVec(),  WifiStrongToVec()] 0.911611732342327
    RandomForestClassifier(class_weight='balanced', n_estimators=400, n_jobs=4, oob_score=False, random_state=42,
            verbose=0, warm_start=False) Mean: 0.911611732342327
    线上0.9116
"""
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from common_helper import ModelBase, XXToVec
import pandas as pd
from collections import Counter


class WifiStrongToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_strong_features_{}_{}.pkl')
        self.min_strong = -300

    def _fit_transform(self, data, mall_id):
        return self._transform(data, mall_id)

    def _transform(self, data, mall_id):
        ret_list = []
        for wifi_infos in data['wifi_infos']:
            list_id = []
            list_strong = []
            list_connect = []
            if wifi_infos:
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    list_id.append(_id)
                    list_strong.append(int(_strong))
                    list_connect.append(_connect)
                max_strong_index = list_strong.index(max(list_strong))
                temp_id = list_id[max_strong_index]
                ret_list.append(int(temp_id.replace('b_', '')))
            else:
                ret_list.append(list(Counter(ret_list).keys())[0])
        data = data.assign(wifi_strong=pd.Series(ret_list).values)
        data = pd.concat([data['wifi_strong'], data['longitude'], data['latitude']], axis=1)
        wifi_features = csr_matrix(data)  # TODO normalize
        return wifi_features


class UseStrongWifi(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=-1, n_estimators=300, random_state=self._random_state),
        }


def train_test():
    task = UseStrongWifi()
    task.train_test([WifiStrongToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
