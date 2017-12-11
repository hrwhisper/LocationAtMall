# -*- coding: utf-8 -*-
# @Date    : 2017/10/29
# @Author  : hrwhisper
"""
    Given a user feature, predict the category_id. the predicted category_id will be use as a feature for predicting
    shop_id.
"""
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

from common_helper import ModelBase, DataVector, safe_dump_model, safe_save_csv_result
from parse_data import read_train_join_mall, read_test_data
from use_location import LocationToVec2
from use_price import PriceToVec
from use_strong_wifi import WifiStrongToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


class CategoryPredicted(ModelBase):
    def __init__(self):
        super().__init__(save_model_base_path='./feature_save/category/')

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return RandomForestClassifier(n_jobs=self.n_jobs,
                                      n_estimators=400,
                                      bootstrap=False,
                                      min_samples_split=4,
                                      min_samples_leaf=1,
                                      random_state=self._random_state,
                                      class_weight='balanced')

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
        _test_data = read_test_data()

        for mall_id in _train_data['mall_id'].unique():
            train_data = _train_data.loc[_train_data['mall_id'] == mall_id]
            train_label = train_data[target_column].values
            test_data = _test_data.loc[_test_data['mall_id'] == mall_id]

            label_encoder = preprocessing.LabelEncoder()
            train_label = label_encoder.fit_transform(train_label)

            kf = KFold(n_splits=fold, random_state=self._random_state)

            oof_train = np.zeros((train_data.shape[0], len(label_encoder.classes_)))
            oof_test = np.zeros((test_data.shape[0], len(label_encoder.classes_)))

            for i, (train_index, test_index) in enumerate(kf.split(train_data)):
                self._trained_and_predict(vec_func, train_data, train_label, test_data, train_index, test_index,
                                          oof_train, oof_test, i, mall_id)
            oof_test /= fold

            cur_save_path = '{}/{}'.format(self.SAVE_MODEL_BASE_PATH, mall_id)

            safe_dump_model(oof_train, cur_save_path + '_train.pkl')
            safe_dump_model(oof_test, cur_save_path + '_test.pkl')

            row_ids = pd.DataFrame(train_data['row_id'].values, columns=['row_id'])
            oof_train = pd.DataFrame(oof_train, columns=label_encoder.classes_)
            safe_save_csv_result(pd.concat([row_ids, oof_train], axis=1).set_index('row_id'),
                                 cur_save_path + '_train.csv')

            row_ids = pd.DataFrame(test_data['row_id'].values, columns=['row_id'])
            oof_test = pd.DataFrame(oof_test, columns=label_encoder.classes_)
            safe_save_csv_result(pd.concat([row_ids, oof_test], axis=1).set_index('row_id'),
                                 cur_save_path + '_test.csv')

    def _trained_and_predict(self, vec_func, _train_data, _train_label, R_X_test,
                             train_index, test_index, oof_train, oof_test, cur_fold, mall_id):

        fold_X_train, fold_y_train = _train_data.iloc[train_index], _train_label[train_index]
        fold_X_test, fold_y_test = _train_data.iloc[test_index], _train_label[test_index]

        assert len(fold_X_train['mall_id'].unique()) == 1

        X_train, y_train, X_test, y_test = DataVector.train_and_test_to_vec(mall_id, vec_func, fold_X_train,
                                                                            fold_y_train, fold_X_test,
                                                                            fold_y_test)

        clf = self._get_classifiers()
        clf.fit(X_train, y_train)

        res = clf.predict_proba(X_test)
        res[np.isnan(res)] = 0
        oof_train[np.ix_(test_index, clf.classes_)] = res

        predicted = clf.predict(X_test)
        score = accuracy_score(y_test, predicted)

        X_test, _ = DataVector.data_to_vec(mall_id, vec_func, R_X_test, None, is_train=False)

        res = clf.predict_proba(X_test)
        # set the inf to zero. OneVsRestClassifier has done normalized, it cause some value to inf.
        res[np.isnan(res)] = 0
        oof_test[:, clf.classes_] += res

        print('mall_id: {}  cur_fold: {}   score: {}'.format(mall_id, cur_fold, score))


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
    func = [LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()]
    task.train_test(func, 'category_id', fold=10)


if __name__ == '__main__':
    train_test()
