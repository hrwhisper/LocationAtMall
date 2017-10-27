# -*- coding: utf-8 -*-
# @Date    : 2017/10/25
# @Author  : hrwhisper
"""
    去除了疑似商场非店铺的wifi，但是反而下降了。
"""

import collections
from datetime import datetime
from scipy import sparse

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score

from common_helper import ModelBase, XXToVec, trained_and_predict_location
from use_location import LocationToVec
from use_location3 import LocationToVec3
from use_time import TimeToVec
from use_wifi3 import WifiToVec3


class WifiToVec4(XXToVec):
    MALL_WIFI = pd.read_csv('./feature_save/wifi_co_occurrence.csv')

    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl', './feature_save/wifi_bssid_{}_{}.pkl')
        self.min_strong = -120

    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        """
        :param train_data: pandas. train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
        :param mall_id: str
        :param renew: renew the feature
        :param should_save: bool, should save the feature on disk or not.
        :return: csr_matrix
        """
        if renew:
            train_data = train_data[train_data['mall_id'] == mall_id]
            mall_wifi = self.MALL_WIFI[self.MALL_WIFI['mall_id'] == mall_id]
            mall_wifi = set(mall_wifi['bssid'].unique())

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
                    if len(wifi_and_date[_id]) < 2 or _id in mall_wifi:
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

            wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
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
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(wifi_bssid, self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            wifi_bssid = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            wifi_rows = []
            not_in = set()
            for wifi_infos in test_data['wifi_infos']:
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
                wifi_rows.append(row)

            indptr = [0]
            indices = []
            data = []
            for row in wifi_rows:
                for _id, (_strong, _connect) in row.items():
                    _id = wifi_bssid[_id]
                    indices.append(_id)
                    data.append(_strong)
                indptr.append(len(indices))

            print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
            wifi_features = csr_matrix((data, indices, indptr), shape=(len(test_data), len(wifi_bssid)), dtype=int)
            # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return wifi_features


class UseWifi(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=200, random_state=self._random_state,
                                                    class_weight='balanced'),
        }


    def _trained_by_mall_and_predict_location(self, vec_func, train_data, test_data, has_test_label=True):
        """

        :param vec_func:
        :param train_data:
        :param test_data:
        :param has_test_label: bool
        :return:
        """
        ans = {}
        for ri, mall_id in enumerate({
        'm_7168': 0.708214760008,
        'm_7800': 0.721053965037,
        'm_1920': 0.764782750735,
        'm_4422': 0.767413834659,
        'm_2224': 0.790900290416,
        'm_4079': 0.793646944714,
        'm_6803': 0.825242718447,
        'm_1950': 0.924817798236,
        'm_5076': 0.948070175439,
        'm_4495': 0.972508591065
    }.keys()):
            vectors = [func.train_data_to_vec(train_data, mall_id) for func in vec_func]
            X_train = sparse.hstack(vectors)
            y_train = train_data.loc[train_data['mall_id'] == mall_id]['shop_id']
            # print(X_train.shape, y_train.shape)

            vectors = [func.test_data_to_vec(test_data, mall_id) for func in vec_func]
            X_test = sparse.hstack(vectors)
            assert X_test.shape[0] == len(test_data.loc[test_data['mall_id'] == mall_id])
            # print(X_test.shape)

            if has_test_label:
                y_test = test_data.loc[test_data['mall_id'] == mall_id]['shop_id']
                # print(y_test.shape)

            classifiers = self._get_classifiers()
            for name, cls in classifiers.items():
                predicted = trained_and_predict_location(cls, X_train, y_train, X_test)
                if has_test_label:
                    score = accuracy_score(y_test, predicted)
                    ans[name] = ans.get(name, 0) + score
                    print(ri, mall_id, name, score)
                else:
                    print(ri, mall_id)
                    for row_id, label in zip(test_data.loc[test_data['mall_id'] == mall_id]['row_id'], predicted):
                        ans[row_id] = label
                        # joblib.dump(cls, './model_save/use_wifi_{}_{}.pkl'.format(name, mall_id))
        return ans


def train_test():
    task = UseWifi()
    task.train_test([LocationToVec(), WifiToVec4(), TimeToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
    # t = WifiToVec4()
    # print(set(t.MALL_WIFI['bssid'].unique()))
