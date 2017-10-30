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

from use_time import TimeToVec
from use_wifi import WifiToVec


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

        for train_index, test_index in kf.split(_train_data):
            fold_X_train, fold_y_train = _train_data.iloc[train_index], _train_label[train_index]
            fold_X_test, fold_y_test = _train_data.iloc[test_index], _train_label[test_index]

            self._trained_and_predict(vec_func, fold_X_train, fold_y_train, fold_X_test, fold_y_test, _test_data,
                                      oof_train, oof_test)
        oof_test /= fold

        joblib.dump(oof_train, self.feature_save_path + '_oof_train.pkl')
        joblib.dump(oof_test, self.feature_save_path + '_oof_test.pkl')

        with open(self.feature_save_path, 'w') as f:
            f.write('row_id,{}\n'.format(','.join(str(i) for i in range(n))))
            for i, row_id in enumerate(_train_data['row_id']):
                f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_train[row_id]))))
            for i, row_id in enumerate(_test_data['row_id']):
                f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_test[row_id]))))
        print('done')

    def _trained_and_predict(self, vec_func, fold_X_train, fold_y_train, fold_X_test, fold_y_test, R_X_test,
                             oof_train, oof_test):
        clf = list(self._get_classifiers().values())[0]
        for ri, mall_id in enumerate(fold_X_train['mall_id'].unique()):
            X_train, y_train, X_test, y_test = self._train_and_test_to_vec(mall_id, vec_func, fold_X_train,
                                                                           fold_y_train, fold_X_test, fold_y_test)

            clf.fit(X_train, y_train)

            oof_train[
                np.ix_(fold_X_test.index[fold_X_test['mall_id'] == mall_id], clf.classes_)] = clf.predict_log_proba(
                X_test)

            predicted = clf.predict(X_test)

            score = accuracy_score(y_test, predicted)
            print(ri, mall_id, score)

            X_test, _ = self._data_to_vec(mall_id, vec_func, R_X_test, None, is_train=False)
            oof_test[np.ix_(R_X_test.index[R_X_test['mall_id'] == mall_id], clf.classes_)] += clf.predict_log_proba(
                X_test)


def train_test():
    task = CategoryPredicted()
    func = [LocationToVec(), WifiToVec(), TimeToVec()]
    task.train_test(func, 'category_id')


if __name__ == '__main__':
    train_test()
