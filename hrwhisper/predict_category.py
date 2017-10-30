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
from sklearn.model_selection import KFold

from common_helper import ModelBase
from parse_data import read_train_join_mall, read_test_data
from use_location import LocationToVec

from use_time import TimeToVec
from use_wifi import WifiToVec


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
        kf = KFold(n_splits=5, random_state=self._random_state)
        ans = {}
        for train_index, test_index in kf.split(_train_data):
            X_train, y_train = _train_data.iloc[train_index], _train_label[train_index]
            X_test, y_test = _train_data.iloc[test_index], _train_label[test_index]
            ans.update(self._trained_by_mall_and_predict_location(vec_func, X_train, y_train, X_test, y_test))

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
    func = [LocationToVec(), WifiToVec(), TimeToVec()]
    task.train_test(func, 'category_id')
    task.train_and_on_test_data(func, 'category_id')


if __name__ == '__main__':
    train_test()
