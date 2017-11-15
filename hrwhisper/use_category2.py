# -*- coding: utf-8 -*-
# @Date    : 2017/11/15
# @Author  : hrwhisper

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec
from parse_data import read_mall_data


class CategoryToVec2(XXToVec):
    """
        using the category feature which has been predicted by 'predict_category_pro.py'
        RF: k=all 0.9195226506115334
    """

    def __init__(self):
        super().__init__('./feature_save/category_pro_features_{}_{}.pkl')
        self.k = 2
        self.feature_load_path = './feature_save/category/{}_{}.csv'

    def _do_transform(self, data, mall_id):
        categories = pd.concat((pd.read_csv(self.feature_load_path.format(mall_id, 'train'), dtype={'row_id': str}),
                                pd.read_csv(self.feature_load_path.format(mall_id, 'test'), dtype={'row_id': str})),
                               0).set_index('row_id')

        features = data[['row_id']].join(categories, on='row_id', rsuffix='_train').set_index('row_id')
        # features = np.argpartition(features.values, -self.k)[:, -self.k:]
        return csr_matrix(features)

    def _fit_transform(self, train_data, mall_id):
        return self._do_transform(train_data, mall_id)

    def _transform(self, test_data, mall_id):
        return self._do_transform(test_data, mall_id)


def train_test():
    task = ModelBase()
    task.train_test([CategoryToVec2()], 'shop_id')
    # task.train_and_on_test_data([CategoryToVec()])


if __name__ == '__main__':
    train_test()
