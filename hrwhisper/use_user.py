# -*- coding: utf-8 -*-
# @Date    : 2017/11/15
# @Author  : hrwhisper

"""
    用户特征
    binary rf 0.9182->0.9200
"""
import collections

import numpy as np
from scipy.sparse import csr_matrix
from sklearn import preprocessing

from common_helper import XXToVec


class UserToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/user_features_{}_{}.pkl')
        self.shop_to_index = None
        self.user_counter = None
        self.total_counter = None
        self.norm = 1
        self._scaler = preprocessing.MaxAbsScaler()

    def _fit(self, train_data):
        self.user_counter = collections.defaultdict(lambda: collections.Counter())
        self.total_counter = collections.Counter()

        shops = np.sort(train_data['shop_id'].unique())
        self.shop_to_index = {shop_id: i for i, shop_id in enumerate(shops)}
        for user_id, shop_id in zip(train_data['user_id'], train_data['shop_id']):
            self.user_counter[user_id][shop_id] += 1
            self.total_counter[shop_id] += 1

        self.norm = train_data.shape[0]

    def _fit_transform(self, train_data, mall_id):
        self._fit(train_data)
        return self._scaler.fit_transform(self._do_transform(train_data, mall_id))

    def _do_transform(self, data, mall_id):
        features = []
        n = len(self.shop_to_index)

        for user_id in data['user_id']:
            feature = np.zeros(n)
            if user_id in self.user_counter:
                user = self.user_counter[user_id]
                for shop_id, cnt in user.items():
                    feature[self.shop_to_index[shop_id]] = cnt
            else:  # TODO 冷启动问题
                pass
                # for shop_id, cnt in self.total_counter.items():
                #     feature[self.shop_to_index[shop_id]] = cnt
                # feature /= self.norm
            features.append(feature)
        return csr_matrix(features)

    def _transform(self, data, mall_id):
        return self._scaler.transform(self._do_transform(data,mall_id))
