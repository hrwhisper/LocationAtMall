# -*- coding: utf-8 -*-
# @Date    : 2017/10/29
# @Author  : hrwhisper
"""
    Given a user feature, predict the category_id. the predicted category_id will be use as a feature for predicting
    shop_id.
"""
import os

import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

from common_helper import ModelBase
from parse_data import read_train_join_mall, read_test_data
from use_location import LocationToVec
from use_location2 import LocationToVec2
from use_strong_wifi import WifiStrongToVec

from use_time import TimeToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


class CategoryPredicted(ModelBase):
    def __init__(self):
        super().__init__()
        self.feature_save_path = './feature_save/predicted_category_pro.csv'

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=os.cpu_count() // 2, n_estimators=400,
                                                    random_state=self._random_state, class_weight='balanced'),
        }

    def train_test(self, vec_func, target_column='category_id', fold=5):
        """

        :param vec_func: list of vector function
        :param target_column: the target column you want to predict.
        :param fold: the fold of cross-validation.
        :return: None
        """
        # ------input data -----------
        _train_data = read_train_join_mall()
        _train_data = _train_data.sort_values(by='time_stamp')
        _train_label = _train_data[target_column].values
        _test_data = read_test_data()

        le = preprocessing.LabelEncoder().fit(_train_label)
        # print(le.classes_)
        _train_label = le.transform(_train_label)

        kf = KFold(n_splits=fold, random_state=self._random_state)
        m, n = _train_data.shape[0], len(le.classes_)
        oof_train = np.zeros((m, n))
        oof_test = np.zeros((m, n))
        print(m, n)

        for i, (train_index, test_index) in enumerate(kf.split(_train_data)):
            print(i)
            self._trained_and_predict(vec_func, _train_data, _train_label, _test_data, oof_train, oof_test,
                                      train_index, test_index)
        oof_test /= fold

        joblib.dump(oof_train, self.feature_save_path + '_oof_train.pkl', compress=3)
        joblib.dump(oof_test, self.feature_save_path + '_oof_test.pkl', compress=3)

        with open(self.feature_save_path, 'w') as f:
            f.write('row_id,{}\n'.format(','.join(str(i) for i in range(n))))
            for i, row_id in enumerate(_train_data['row_id']):
                f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_train[i]))))
            for i, row_id in enumerate(_test_data['row_id']):
                f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_test[i]))))
        print('done')

    def _trained_and_predict(self, vec_func, _train_data, _train_label, R_X_test,
                             oof_train, oof_test, _train_index, _test_index):
        mall_id_list = _train_data.iloc[_train_index]['mall_id'].unique()
        _train_index = set(_train_index)
        _test_index = set(_test_index)
        clf = list(self._get_classifiers().values())[0]
        for ri, mall_id in enumerate(mall_id_list):
            # 先得到当前商场的所有下标，然后和训练的下标做交集才对。
            index = set(np.where(_train_data['mall_id'] == mall_id)[0])

            train_index = np.array(list(_train_index & index))
            test_index = np.array(list(_test_index & index))

            data = _train_data
            label = _train_label

            fold_X_train, fold_y_train = data.iloc[train_index], label[train_index]
            fold_X_test, fold_y_test = data.iloc[test_index], label[test_index]

            assert len(fold_X_train['mall_id'].unique()) == 1

            X_train, y_train, X_test, y_test = self._train_and_test_to_vec(mall_id, vec_func, fold_X_train,
                                                                           fold_y_train, fold_X_test, fold_y_test)

            clf.fit(X_train, y_train)

            oof_train[np.ix_(test_index, clf.classes_)] = clf.predict_log_proba(X_test)

            predicted = clf.predict(X_test)

            score = accuracy_score(y_test, predicted)
            print(ri, mall_id, score)

            X_test, _ = self._data_to_vec(mall_id, vec_func, R_X_test, None, is_train=False)
            oof_test[np.ix_(np.where(R_X_test['mall_id'] == mall_id)[0], clf.classes_)] += clf.predict_log_proba(
                X_test)


def recovery_probability_from_pkl():
    _train_data = read_train_join_mall()
    _train_data = _train_data.sort_values(by='time_stamp')
    _train_label = _train_data['category_id'].values
    _test_data = read_test_data()

    le = preprocessing.LabelEncoder().fit(_train_label)
    # print(le.classes_)
    _train_label = le.transform(_train_label)

    m, n = _train_data.shape[0], len(le.classes_)
    print(m, n)

    oof_train = joblib.load('./feature_save/predicted_category_pro.csv_oof_train2.pkl')
    oof_test = joblib.load('./feature_save/predicted_category_pro.csv_oof_test2.pkl')
    with open('./feature_save/predicted_category_pro.csv', 'w') as f:
        f.write('row_id,{}\n'.format(','.join(str(i) for i in range(n))))
        for i, row_id in enumerate(_train_data['row_id']):
            f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_train[i]))))
        for i, row_id in enumerate(_test_data['row_id']):
            f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_test[i]))))


def train_test():
    task = CategoryPredicted()
    func = [LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec()]
    task.train_test(func, 'category_id')


if __name__ == '__main__':
    train_test()
    # recovery_probability_from_pkl

    # 修改输出文件，先将-inf变为0，然后不为0 的减去最小值。
    # with open('./feature_save/predicted_category_pro.csv', 'r') as f:
    #     a = f.read()
    # with open('./feature_save/predicted_category_pro.csv', 'w') as f:
    #     a = a.replace('-inf', '0.0')
    #     f.write(a)

    # import pandas as pd
    #
    # a = pd.read_csv('./feature_save/predicted_category_pro.csv')
    # print(a[[str(i) for i in range(64)]].min().min())  # -11.354029078800002
    # with open('./feature_save/predicted_category_pro.csv', 'r') as f, \
    #         open('./feature_save/predicted_category_pro2.csv', 'w') as fw:
    #     for i, row in enumerate(f):
    #         if i == 0:
    #             fw.write(row + '\n')
    #         else:
    #             row = row.split(',')
    #             row_id = row[0]
    #             vals = list(map(float, row[1:]))
    #             # print(vals)
    #             vals = [(0.0 if v == 0 else v + 12) for v in vals]
    #             # print(vals)
    #             fw.write('{},{}\n'.format(row_id, ','.join(map(str, vals))))
