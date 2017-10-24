# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    使用了wifi特征，类似BOW
"""
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn import preprocessing
from parse_data import read_train_data
from common_helper import ModelBase, XXToVec


class WifiToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl', './feature_save/wifi_bssid_{}_{}.pkl')
        self.min_strong = -300

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
            indptr = [0]
            indices = []
            data = []
            for wifi_infos in train_data['wifi_infos']:
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    _id = wifi_bssid[_id]
                    indices.append(_id)
                    if _connect == 'true':
                        data.append((int(_strong) - self.min_strong))
                    else:
                        data.append(int(_strong) - self.min_strong)
                indptr.append(len(indices))

            wifi_features = csr_matrix((data, indices, indptr), dtype=int)  # TODO normalize
            # return preprocessing.scale(wifi_features, with_mean=False)
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(wifi_bssid, self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            wifi_bssid = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            indptr = [0]
            indices = []
            data = []
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            not_in = set()
            for wifi_infos in test_data['wifi_infos']:
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    if _id in wifi_bssid:
                        _id = wifi_bssid[_id]
                        indices.append(_id)
                        if _connect == 'true':
                            data.append((int(_strong) - self.min_strong))
                        else:
                            data.append(int(_strong) - self.min_strong)
                    else:
                        not_in.add(_id)
                indptr.append(len(indices))
            # for i in range(len(wifi_bssid) - len(indptr)):

            # indptr.extend([len(indices)] * (len(wifi_bssid) - len(indptr)))
            print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
            wifi_features = csr_matrix((data, indices, indptr), dtype=int, shape=(len(test_data), len(wifi_bssid)))
            # TODO normalize
            # return preprocessing.scale(wifi_features, with_mean=False)
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
        'random forest': RandomForestClassifier(n_jobs=-1, n_estimators=100, random_state=self._random_state),
        }

def train_test():
    task = UseWifi()
    task.train_test([WifiToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
