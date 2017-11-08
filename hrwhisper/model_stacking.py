# -*- coding: utf-8 -*-
# @Date    : 2017/11/6
# @Author  : hrwhisper

import os

import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.multiclass import OneVsRestClassifier
from xgboost import XGBClassifier

from common_helper import ModelBase, DataVector, safe_dump_model, train_test_split
from parse_data import read_train_join_mall, read_test_data
from use_category import CategoryToVec
from use_location import LocationToVec
from use_location2 import LocationToVec2
from use_price import PriceToVec
from use_strong_wifi import WifiStrongToVec
from use_tfidf_wifi import WifiTfIdfToVec
from use_time import TimeToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


class ModelStacking(ModelBase):
    def __init__(self, renew=False, save_model=True, save_model_base_path='./model_save/stacking'):
        super().__init__(save_model=save_model, save_model_base_path=save_model_base_path)
        self.renew = renew
        self.new_feature_save_base_path = './feature_save/stacking/'

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=self.n_jobs,
                                                    n_estimators=400,
                                                    bootstrap=False,
                                                    min_samples_split=4,
                                                    min_samples_leaf=1,
                                                    random_state=self._random_state,
                                                    class_weight='balanced'),
            'binary random forest': OneVsRestClassifier(RandomForestClassifier(n_estimators=400,
                                                                               bootstrap=False,
                                                                               random_state=self._random_state,
                                                                               class_weight='balanced'),
                                                        n_jobs=self.n_jobs),
            # 'xgb': XGBClassifier(colsample_bytree=0.7,
            #                      learning_rate=0.025,
            #                      max_depth=6,
            #                      min_child_weight=1,
            #                      missing=-999,
            #                      n_jobs=os.cpu_count() // 3 * 2,
            #                      n_estimators=500,
            #                      objective='binary:logistic',
            #                      random_state=1024,
            #                      _silent=1,
            #                      subsample=0.6),
            'binary xgb': OneVsRestClassifier(XGBClassifier(colsample_bytree=0.7,
                                                            learning_rate=0.025,
                                                            max_depth=6,
                                                            min_child_weight=1,
                                                            missing=-999,
                                                            # n_jobs=os.cpu_count() // 3 * 2,
                                                            n_estimators=500,
                                                            objective='binary:logistic',
                                                            random_state=1024,
                                                            _silent=1,
                                                            subsample=0.6
                                                            )
                                              , n_jobs=self.n_jobs)
        }

    def train_test(self, vec_func, target_column='shop_id', fold=5):
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

        ans = {}
        total_score = 0
        for mall_id in _train_data['mall_id'].unique():
            train_data = _train_data.loc[_train_data['mall_id'] == mall_id]
            train_label = train_data[target_column].values
            test_data = _test_data.loc[_test_data['mall_id'] == mall_id]

            label_encoder = preprocessing.LabelEncoder()
            train_label = label_encoder.fit_transform(train_label)

            new_train_feature, new_test_feature = [], []
            kf = KFold(n_splits=fold, random_state=self._random_state)

            for clf_name, clf in self._get_classifiers().items():
                oof_train = np.zeros((train_data.shape[0], len(label_encoder.classes_)))
                oof_test = np.zeros((test_data.shape[0], len(label_encoder.classes_)))

                for i, (train_index, test_index) in enumerate(kf.split(train_data)):
                    self._trained_and_predict(vec_func, train_data, train_label, test_data, train_index, test_index,
                                              oof_train, oof_test, i, clf_name, mall_id)

                new_train_feature.append(oof_train)
                new_test_feature.append(oof_test / fold)

            new_train_feature = np.hstack(new_train_feature)
            new_test_feature = np.hstack(new_test_feature)
            # print(new_train_feature.shape)

            # ------- second layer.
            clf = self._get_classifiers()['random forest']

            # -------- on test data
            clf.fit(new_train_feature, train_label)
            predicted = clf.predict(new_test_feature)

            for row_id, label in zip(test_data['row_id'], predicted):
                ans[row_id] = label

            # ---------to report accuracy score
            train_data, test_data, train_label, test_label = train_test_split(new_train_feature, train_label,
                                                                              self._test_ratio)
            predicted = self.trained_and_predict_location(clf, train_data, train_label, test_data, test_label)
            score = accuracy_score(test_label, predicted)
            total_score += score
            print('---second layer: {}  {}'.format(mall_id, score))

        print('mean score{}'.format(total_score / _train_data['mall_id'].unique()))
        self.result_to_csv(ans)

    def _trained_and_predict(self, vec_func, _train_data, _train_label, R_X_test,
                             train_index, test_index, oof_train, oof_test, cur_fold, clf_name, mall_id):

        fold_X_train, fold_y_train = _train_data.iloc[train_index], _train_label[train_index]
        fold_X_test, fold_y_test = _train_data.iloc[test_index], _train_label[test_index]

        assert len(fold_X_train['mall_id'].unique()) == 1

        X_train, y_train, X_test, y_test = DataVector.train_and_test_to_vec(mall_id, vec_func, fold_X_train,
                                                                            fold_y_train, fold_X_test,
                                                                            fold_y_test)

        cur_save_path = '{}/{}/{}_{}'.format(self.SAVE_MODEL_BASE_PATH, clf_name, mall_id, cur_fold)
        if self.renew:
            clf = self._get_classifiers()[clf_name]
            clf.fit(X_train, y_train)
            if self.SAVE_MODEL:
                safe_dump_model(clf, cur_save_path)
        else:
            clf = joblib.load(cur_save_path)

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

        print('mall_id: {}  cur_fold: {}  classifier name: {}  score: {}'.format(mall_id, cur_fold, clf_name, score))


def train_test():
    task = ModelStacking(renew=True)
    task.train_test([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])
    task.train_and_on_test_data([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])


if __name__ == '__main__':
    train_test()
