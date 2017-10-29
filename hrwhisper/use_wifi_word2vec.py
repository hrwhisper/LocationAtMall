# -*- coding: utf-8 -*-
# @Date    : 2017/10/24
# @Author  : hrwhisper

import gensim
import numpy as np
from scipy.sparse import csr_matrix

from common_helper import XXToVec, ModelBase


class WifiWordToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_word2vec_features_{}_{}.pkl')
        self.WORD2VEC_SIZE = 10
        self.MIN_STRONG = -120
        self.word2vec = None

    def _fit_transform(self, train_data, mall_id):
        wifi_rows = []
        for wifi_infos in train_data['wifi_infos']:
            row = []
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                row.append(_id)  # TODO sort by strong?
            wifi_rows.append(sorted(row))

        self.word2vec = word2vec = gensim.models.Word2Vec(wifi_rows, sg=1, size=self.WORD2VEC_SIZE, min_count=0)
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
        return wifi_features

    def _transform(self, test_data, mall_id):
        word2vec = self.word2vec
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

        return csr_matrix(np.array(features))


class UseWifiWord2vec(ModelBase):
    def __init__(self):
        super().__init__()


def train_test():
    task = UseWifiWord2vec()
    task.train_test([WifiWordToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
