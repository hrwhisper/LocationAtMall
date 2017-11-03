# -*- coding: utf-8 -*-
# @Date    : 2017/11/3
# @Author  : hrwhisper
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
from sklearn.multiclass import OneVsRestClassifier
from xgboost import XGBClassifier

from common_helper import ModelBase, get_recommend_cpu_count
from parse_data import read_train_join_mall
from use_location2 import LocationToVec2
from use_price import PriceToVec
from use_strong_wifi import WifiStrongToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


def multiclass_xgboost():
    parameters = {'nthread': [2],
                  'objective': ['multi:softmax'],
                  'learning_rate': [0.025, 0.05, 0.1],
                  'max_depth': [6, 7, 8, 10],
                  'min_child_weight': [1, 5, 10],
                  'silent': [1],
                  'subsample': [0.6, 0.8, 0.9, 1],
                  'colsample_bytree': [0.7, 0.8, ],
                  'n_estimators': [100, 200, 500],
                  'missing': [-999],
                  'random_state': [1337, 1080, 1024, 1226]}
    clf = GridSearchCV(XGBClassifier(), parameters, n_jobs=get_recommend_cpu_count() // 2,
                       cv=KFold(n_splits=5, random_state=42),
                       verbose=1, refit=True)
    return clf


def binary_xgboost():
    parameters = {'estimator__nthread': [2],
                  'estimator__objective': ['binary:logistic'],
                  'estimator__learning_rate': [0.025, 0.05, 0.1],
                  'estimator__max_depth': [6, 7, 8, 10],
                  'estimator__min_child_weight': [1, 5, 10],
                  'estimator__silent': [1],
                  'estimator__subsample': [0.6, 0.8, 0.9, 1],
                  'estimator__colsample_bytree': [0.7, 0.8, ],
                  'estimator__n_estimators': [100, 200, 500],
                  'estimator__missing': [-999],
                  'estimator__random_state': [1337, 1080, 1024, 1226]}

    clf = GridSearchCV(OneVsRestClassifier(XGBClassifier()), parameters, n_jobs=get_recommend_cpu_count() // 2,
                       cv=KFold(n_splits=5, random_state=42),
                       verbose=1, refit=True)
    return clf


def grid_search_xgboost(clf):
    train_data = read_train_join_mall()
    train_data = train_data.sort_values(by='time_stamp')
    train_label = preprocessing.LabelEncoder().fit_transform(train_data['shop_id'])

    b = ModelBase()
    X_train, y_train = b._data_to_vec('m_6803', [LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(),
                                                 PriceToVec()],
                                      train_data, train_label)
    print('fit.....')
    clf.fit(X_train, y_train)
    print('fit done')
    best_parameters, score, _ = max(clf.grid_scores_, key=lambda x: x[1])

    print('score:', clf.best_score_)
    for name, val in clf.best_params_.items():
        print("{}  {}".format(name, val))


if __name__ == '__main__':
    grid_search_xgboost(binary_xgboost())
