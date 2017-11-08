# -*- coding: utf-8 -*-
# @Date    : 2017/11/1
# @Author  : hrwhisper

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec
from parse_data import read_mall_data, read_train_join_mall, read_test_data


class PriceToVec(XXToVec):
    """
        using the price feature which has been predicted by 'predict_price.py'
    """
    TRAIN_PRICE = pd.read_csv('./feature_save/predicted_price2.csv', dtype={'row_id': str})

    def __init__(self):
        super().__init__('./feature_save/price_features_{}_{}.pkl')

    def _do_transform(self, data):
        d = data.join(self.TRAIN_PRICE.set_index('row_id'), on='row_id', rsuffix='_train')
        d = d['p_price']
        features = d.values.reshape(-1, 1)
        # features = np.array([round(i) for i in d]).reshape(-1, 1)  # d.values.reshape(-1, 1)
        return csr_matrix(features)

    def _fit_transform(self, train_data, mall_id):
        return self._do_transform(train_data)

    def _transform(self, test_data, mall_id):
        return self._do_transform(test_data)


def train_test():
    task = ModelBase()
    task.train_test([PriceToVec()])
    task.train_and_on_test_data([PriceToVec()])


def analysis():
    TRAIN_PRICE = pd.read_csv('./feature_save/predicted_price.csv')
    data = read_train_join_mall()
    data = data.loc[data['mall_id'] == 'm_1790']
    d = data.join(TRAIN_PRICE.set_index('row_id'), on='row_id', rsuffix='_train')
    print(d.shape)
    diff = []
    for row_id, shop_id, price, p_price in zip(d['row_id'], d['shop_id'], d['price'], d['p_price']):
        print(row_id, shop_id, price, p_price, p_price - price)
        diff.append(abs(p_price - price))
    print(sum(diff), d.shape[0], sum(diff) / d.shape[0])


if __name__ == '__main__':
    train_test()
    # analysis()
