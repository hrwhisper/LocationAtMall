# -*- coding: utf-8 -*-
# @Date    : 2017/10/24
# @Author  : hrwhisper

import gensim
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from common_helper import XXToVec, ModelBase
from use_location import LocationToVec
from use_wifi import WifiToVec


class WifiWordToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_word2vec_features_{}_{}.pkl',
                         './feature_save/wifi_word2vec_how_to_{}.pkl')
        self.WORD2VEC_SAVE_PATH = './feature_save/wifi_word2vec_model_{}.pkl'
        self.word2vec_size = 5

    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        if renew:
            train_data = train_data.loc[train_data['mall_id'] == mall_id]
            wifi_bssid = set()
            wifi_rows = []
            for wifi_infos in train_data['wifi_infos']:
                row = []
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    row.append(_id)  # TODO sort by strong?
                    wifi_bssid.add(_id)
                wifi_rows.append(row)

            word2vec = gensim.models.Word2Vec(wifi_rows, window=2, size=self.word2vec_size, min_count=0)
            wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
            indptr = [0]
            indices = []
            data = []
            for wifi_infos in train_data['wifi_infos']:
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    data.extend([i for i in word2vec[_id]])
                    _id = wifi_bssid[_id]
                    indices.extend([_id * self.word2vec_size + i for i in range(self.word2vec_size)])
                indptr.append(len(indices))

            wifi_features = csr_matrix((data, indices, indptr))  # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(wifi_bssid, self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            joblib.dump(word2vec, self.WORD2VEC_SAVE_PATH.format(mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            wifi_bssid = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            word2vec = joblib.load(self.WORD2VEC_SAVE_PATH.format(mall_id))
            not_in = set()
            indptr = [0]
            indices = []
            data = []
            for wifi_infos in test_data['wifi_infos']:
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    if _id not in wifi_bssid:
                        not_in.add(_id)
                        continue
                    data.extend([i for i in word2vec[_id]])
                    _id = wifi_bssid[_id]
                    indices.extend([_id * self.word2vec_size + i for i in range(self.word2vec_size)])
                indptr.append(len(indices))

            print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
            wifi_features = csr_matrix((data, indices, indptr),
                                       shape=(len(test_data), len(wifi_bssid) * self.word2vec_size))
            # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features


class UseWifiWord2vec(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=3, n_estimators=200, random_state=self._random_state),
        }


def train_test():
    task = UseWifiWord2vec()
    task.train_test([LocationToVec(), WifiToVec(), WifiWordToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
