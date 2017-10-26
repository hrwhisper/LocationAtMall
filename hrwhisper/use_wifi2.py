# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    使用了wifi特征，类似BOW
    标准化
"""
from scipy import sparse
import collections
import numpy as np
from scipy.sparse import csr_matrix
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score

from common_helper import ModelBase, XXToVec, trained_and_predict_location
from parse_data import read_train_join_mall
from use_location import LocationToVec


def train_test_split(X, y, test_size=0.2):
    train_size = int((1 - test_size) * X.shape[0])
    print('train_size:{}'.format(train_size))
    return X[:train_size], X[train_size:], y[:train_size], y[train_size:]


class WifiToVec2(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl', './feature_save/wifi_bssid_{}_{}.pkl')
        self.min_strong = -300
        self.SCALER_SAVE_PATH = './feature_save/wifi_scaler_{}.pkl'

    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        """
        :param data: pandas. train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
        :param mall_id: str
        :param renew: renew the feature
        :param should_save: bool, should save the feature on disk or not.
        :return: csr_matrix
        """
        if renew:
            wifi_bssid = set()

            train_data = train_data.loc[train_data['mall_id'] == mall_id]
            for wifi_infos in train_data['wifi_infos']:
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    wifi_bssid.add(_id)

            wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
            vector = []
            for wifi_infos in train_data['wifi_infos']:
                cur = np.zeros(len(wifi_bssid))
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    _id = wifi_bssid[_id]
                    cur[_id] = int(_strong) - self.min_strong
                vector.append(cur)
            vector = np.array(vector)
            scaler = preprocessing.StandardScaler()
            scaler.fit_transform(vector)

            wifi_features = csr_matrix(vector)  # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(wifi_bssid, self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            # joblib.dump(scaler, self.SCALER_SAVE_PATH.format(mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            wifi_bssid = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            scaler = joblib.load(self.SCALER_SAVE_PATH.format(mall_id))

            vector = []
            not_in = set()
            for wifi_infos in test_data['wifi_infos']:
                cur = np.zeros(len(wifi_bssid))
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    if _id not in wifi_bssid:
                        not_in.add(_id)
                        continue
                    _id = wifi_bssid[_id]
                    cur[_id] = int(_strong) - self.min_strong
                vector.append(cur)

            vector = np.array(vector)
            scaler.transform(vector)

            print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
            wifi_features = csr_matrix(vector)
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
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=200, random_state=self._random_state),
        }


def train_test():
    task = UseWifi()
    task.train_test([LocationToVec(), WifiToVec2()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
