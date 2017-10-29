# -*- coding: utf-8 -*-
# @Date    : 2017/10/29
# @Author  : hrwhisper
"""
    Given a user feature, predict the category_id. the predicted category_id will be use as a feature for predicting
    shop_id.
"""
import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from common_helper import ModelBase
from parse_data import read_train_join_mall, read_test_data

from use_location3 import LocationToVec3
from use_time import TimeToVec
from use_wifi3 import WifiToVec3


def split_cross_data(data, label=None, fold=5):
    n = data.shape[0]
    each_len = n // fold
    mask = np.array([True] * n)
    for i in range(fold):
        s, e = i * each_len, (i + 1) * each_len if i < fold - 1 else n
        mask[s:e] = False
        X_train, X_test = data[mask], data[~mask]
        if label is not None:
            y_train, y_test = label[mask], label[~mask]
            yield X_train, X_test, y_train, y_test
        else:
            yield X_train, X_test
        mask[s:e] = True


class CategoryPredicted(ModelBase):
    def __init__(self):
        super().__init__()
        self.feature_save_path = './feature_save/predicted_category.csv'

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=os.cpu_count() // 2, n_estimators=400,
                                                    random_state=self._random_state, class_weight='balanced'),
        }

    def train_test(self, vec_func, target_column='category_id'):
        """

        :param vec_func: list of vector function
        :param target_column: the target column you want to predict.
        :return:
        """
        # ------input data -----------
        _train_data = read_train_join_mall()
        _train_data = _train_data.sort_values(by='time_stamp')
        _train_label = _train_data[target_column].values

        ans = {}
        for X_train, X_test, y_train, y_test in split_cross_data(_train_data, _train_label):
            ans.update(
                self._trained_by_mall_and_predict_location(vec_func, X_train, y_train, X_test, y_test))

        with open(self.feature_save_path, 'w') as f:
            f.write('row_id,p_category_id\n')
            for row_id in _train_data['row_id']:
                f.write('{},{}\n'.format(row_id, ans[row_id]))
        print('done')

    def train_and_on_test_data(self, vec_func, target_column='category_id'):
        train_data = read_train_join_mall()
        train_label = train_data[target_column]
        test_data = read_test_data()

        ans = self._trained_by_mall_and_predict_location(vec_func, train_data, train_label, test_data)
        with open(self.feature_save_path, 'a') as f:
            for row_id in test_data['row_id']:
                f.write('{},{}\n'.format(row_id, ans[row_id]))
        print('done')


def train_test():
    task = CategoryPredicted()
    func = [LocationToVec3(), WifiToVec3(), TimeToVec()]
    task.train_test(func, 'category_id')
    task.train_and_on_test_data(func, 'category_id')


if __name__ == '__main__':
    train_test()
