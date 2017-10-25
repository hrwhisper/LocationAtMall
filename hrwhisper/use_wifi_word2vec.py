# -*- coding: utf-8 -*-
# @Date    : 2017/10/24
# @Author  : hrwhisper

import gensim
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from common_helper import XXToVec, ModelBase
from use_location import LocationToVec
from use_wifi2 import WifiToVec


class WifiWordToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_word2vec_features_{}_{}.pkl',
                         './feature_save/wifi_word2vec_how_to_{}.pkl')
        self.WORD2VEC_SIZE = 10
        self.MIN_STRONG = -120

    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        if renew:
            train_data = train_data.loc[train_data['mall_id'] == mall_id]
            wifi_rows = []
            for wifi_infos in train_data['wifi_infos']:
                row = []
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    row.append(_id)  # TODO sort by strong?
                wifi_rows.append(row)

            word2vec = gensim.models.Word2Vec(wifi_rows, size=self.WORD2VEC_SIZE, min_count=0)
            print('word2vec done')
            features = []
            for wifi_infos in train_data['wifi_infos']:
                cur = np.zeros(self.WORD2VEC_SIZE).astype(float)
                cnt = 0
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    cur += word2vec[_id] * np.log2(int(_strong) - self.MIN_STRONG)
                    cnt += np.log2(int(_strong) - self.MIN_STRONG)
                cur /= cnt
                features.append(cur)

            wifi_features = csr_matrix(np.array(features))  # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(word2vec, self.HOW_TO_VEC_SAVE_PATH.format(mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            word2vec = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format(mall_id))

            features = []
            for wifi_infos in test_data['wifi_infos']:
                cur = np.zeros(self.WORD2VEC_SIZE).astype(float)
                cnt = 0
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    if _id not in word2vec:
                        continue
                    cur += word2vec[_id] * np.log2(int(_strong) - self.MIN_STRONG)
                    cnt += np.log2(int(_strong) - self.MIN_STRONG)
                if cnt:
                    cur /= cnt
                features.append(cur)

            wifi_features = csr_matrix(np.array(features))
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return wifi_features


class UseWifiWord2vec(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=200, random_state=self._random_state),
        }


def train_test():
    task = UseWifiWord2vec()
    task.train_test([LocationToVec(), WifiToVec(), WifiWordToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
