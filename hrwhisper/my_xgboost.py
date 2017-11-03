# -*- coding: utf-8 -*-
# @Date    : 2017/11/2
# @Author  : hrwhisper
import os

import numpy as np
import xgboost as xgb
from sklearn import preprocessing
from xgboost import XGBClassifier

from common_helper import ModelBase, get_recommend_cpu_count
from use_location2 import LocationToVec2
from use_price import PriceToVec
from use_strong_wifi import WifiStrongToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


class MyXGoostBase(object):
    def __init__(self, param, number_round, n_jobs=4, early_stopping_rounds=50, verbose=True):
        """

        :param param:
        :param number_round:
        :param n_jobs:
        :param early_stopping_rounds:
        :param verbose: (bool or int) Fasle不打印。 int的话多少轮打印一次
        """
        self.param = param
        self.number_round = number_round
        self.n_jobs = n_jobs
        self.early_stopping_rounds = early_stopping_rounds
        self.verbose = verbose


class MyXGBoost(MyXGoostBase):
    """
        多分类的XGBoost
    """

    def __init__(self, param, number_round, n_jobs=4, early_stopping_rounds=50, verbose=True):
        super().__init__(param, number_round, n_jobs, early_stopping_rounds, verbose)
        self.bst = None
        self.label_encoder = preprocessing.LabelEncoder()
        self.param['eval_metric'] = 'merror'

    def fit(self, X_train, y_train, X_test=None, y_test=None):
        labels = set(list(y_train))
        if y_test is not None:
            labels = labels | set(list(y_test))

        self.label_encoder.fit(np.array(list(labels)))
        y_train = self.label_encoder.transform(y_train)
        self.param['num_class'] = len(self.label_encoder.classes_)

        eval_list = [(X_train, 'train')]
        X_train = xgb.DMatrix(X_train, label=y_train, nthread=self.n_jobs)
        if y_test is not None:
            y_test = self.label_encoder.transform(y_test)
            X_test = xgb.DMatrix(X_test, label=y_test, nthread=self.n_jobs)
            eval_list += [(X_test, 'test')]

        self.bst = xgb.train(self.param, X_train, self.number_round, eval_list,
                             early_stopping_rounds=self.early_stopping_rounds)
        return self

    def predict(self, X):
        X = xgb.DMatrix(X, nthread=self.n_jobs)
        predicted = self.bst.predict(X)
        return self.label_encoder.inverse_transform(predicted.astype(int))


class BinaryClassifierMyXGBoost(MyXGoostBase):
    """
        二分类的XGBoost
    """

    def __init__(self, param, number_round, n_jobs=4, early_stopping_rounds=50, verbose=True):
        super().__init__(param, number_round, n_jobs, early_stopping_rounds, verbose)
        self.estimators_ = None
        self.classes_ = None
        self.param['eval_metric'] = 'error'

    def fit(self, _X_train, _y_train, _X_test=None, _y_test=None):
        self.classes_ = np.array(sorted(list(set(list(_y_train)))))
        self.estimators_ = []
        for label in self.classes_:
            y_train = (_y_train == label).astype(int)
            X_train = xgb.DMatrix(_X_train, label=y_train, nthread=self.n_jobs)
            eval_list = [(X_train, 'train')]
            if _y_test is not None:
                y_test = (_y_test == label).astype(int)
                X_test = xgb.DMatrix(_X_test, label=y_test, nthread=self.n_jobs)
                eval_list += [(X_test, 'test')]

            # TODO parallel
            self.estimators_.append(xgb.train(self.param, X_train, self.number_round, eval_list,
                                              early_stopping_rounds=self.early_stopping_rounds,
                                              verbose_eval=self.verbose))
        return self

    def predict(self, X):
        n_samples = X.shape[0]
        maxima = np.empty(n_samples, dtype=float)
        X = xgb.DMatrix(X, nthread=self.n_jobs)
        maxima.fill(-np.inf)
        arg_maxima = np.zeros(n_samples, dtype=int)
        for i, e in enumerate(self.estimators_):
            pred = e.predict(X)
            np.maximum(maxima, pred, out=maxima)
            arg_maxima[maxima == pred] = i
        return self.classes_[np.array(arg_maxima.T)]


class UseMyXgboost(ModelBase):
    """
        depth(subsample 0.8 colsample_bytree 0.85 min_child_weight:1) :
        10   0.919133893062
        8    0.919575784357
        7    0.918250110473

        subsample(depth 8 colsample_bytree 0.85 min_child_weight:1)
        1   0.916482545294
        0.6 0.917366327883
    """

    def _get_classifiers(self):
        return {
            'BinaryClassifierMyXGBoost':
                BinaryClassifierMyXGBoost(
                    {
                        'booster': 'gbtree',
                        'objective': 'binary:logistic',
                        'eta': 0.1,
                        'max_depth': 8,
                        'subsample': 0.8,
                        'min_child_weight': 1,
                        'seed': 42,  # 1080 1024 1412
                        'missing': -999,
                        'silent': 1,
                        'nthread': get_recommend_cpu_count()
                    }
                    , number_round=500
                    , early_stopping_rounds=50
                ),
            'MyXgboost':
                MyXGBoost(
                    {
                        'booster': 'gbtree',
                        'objective': 'multi:softmax',
                        'eta': 0.1,
                        'max_depth': 8,
                        'subsample': 0.8,
                        'colsample_bytree': 0.85,
                        'min_child_weight': 1,
                        'eval_metric': 'merror',
                        'seed': 42,  # 1080 1024 1412
                        'missing': -999,
                        'silent': 1,
                        'nthread': get_recommend_cpu_count()
                    }
                    , number_round=500
                    , early_stopping_rounds=50

                )
        }

    @staticmethod
    def trained_and_predict_location(cls, X_train, y_train, X_test, y_test=None):
        print('fitting2....')
        cls = cls.fit(X_train, y_train, X_test, y_test)
        print('predict....')
        predicted = cls.predict(X_test)
        return predicted


def train_test():
    XGBClassifier()
    task = UseMyXgboost()
    task.train_test([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])
    task.train_and_on_test_data([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])


if __name__ == '__main__':
    train_test()
