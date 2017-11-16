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

from common_helper import XXToVec


class UserToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/user_features_{}_{}.pkl')
        self.shop_to_index = None
        self.user_counter = None

    def _fit(self, train_data):
        self.user_counter = collections.defaultdict(lambda: collections.Counter())
        shops = np.sort(train_data['shop_id'].unique())
        self.shop_to_index = {shop_id: i for i, shop_id in enumerate(shops)}
        for user_id, shop_id in zip(train_data['user_id'], train_data['shop_id']):
            self.user_counter[user_id][shop_id] += 1

    def _fit_transform(self, train_data, mall_id):
        self._fit(train_data)
        return self._transform(train_data, mall_id)

    def _transform(self, data, mall_id):
        features = []
        n = len(self.shop_to_index)

        for user_id in data['user_id']:
            feature = np.zeros(n)
            if user_id in self.user_counter:
                user = self.user_counter[user_id]
                for shop_id, cnt in user.items():
                    index = self.shop_to_index[shop_id]
                    feature[index] = cnt
            else:  # TODO 冷启动问题
                pass

            features.append(feature)
        return csr_matrix(features)
