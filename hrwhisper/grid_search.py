# -*- coding: utf-8 -*-
# @Date    : 2017/11/3
# @Author  : hrwhisper
from lightgbm import LGBMClassifier
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
from sklearn.multiclass import OneVsRestClassifier
from xgboost import XGBClassifier

from common_helper import get_recommend_cpu_count, DataVector
from parse_data import read_train_join_mall
from use_location import LocationToVec2
from use_price import PriceToVec
from use_strong_wifi import WifiStrongToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


def multiclass_xgboost():
    parameters = {'estimator__n_jobs': [1],
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
    parameters = {'estimator__n_jobs': [1],
                  'estimator__objective': ['binary:logistic'],
                  'estimator__learning_rate': [0.01, 0.025, 0.05, 0.1],  # 0.015,
                  'estimator__max_depth': [5, 7, 9, 12, 15],  # 3, 17
                  'estimator__gamma': [0, 0.05, 0.1],  # 0.3 0.75
                  'estimator__min_child_weight': [1, 3, 5],  # 7
                  'estimator__subsample': [0.6, 0.7, 0.8, 1.0],  # 0.9,
                  'estimator__colsample_bytree': [0.6, 0.7, 0.8, 1.0],  # 0.9,
                  'estimator__reg_alpha': [0, 0.1, ],  # 0.5
                  'estimator__reg_lambda': [0.01, 0.05, 1],  # 0.01,
                  'estimator__n_estimators': [600],
                  'estimator__silent': [1],
                  'estimator__missing': [-999],
                  'estimator__random_state': [1080],
                  }

    clf = GridSearchCV(XGBClassifier(), parameters, n_jobs=get_recommend_cpu_count(),
                       cv=KFold(n_splits=5, random_state=42),
                       verbose=1, refit=True)
    return clf

    # 'light gbm': LGBMClassifier(n_jobs=self.n_jobs,
    #                             n_estimators=500,
    #                             learning_rate=0.05,
    #                             num_leaves=127,
    #                             max_depth=8,
    #                             ),


def lightgbm():
    parameters = {'n_jobs': [1],
                  'n_estimators': [500, 1000],
                  'num_leaves': [60, 70, 80, 90, 110, 120, 140],
                  'learning_rate': [0.01, 0.015, 0.025, 0.05, 0.1],
                  'max_depth': [5, 7, 9, 12, 15, 17],  # 3
                  'min_child_weight': [1, 3, 5],  # 7
                  # 'subsample': [0.6, 0.7, 0.8, 1.0],  # 0.9,
                  # 'colsample_bytree': [0.6, 0.7, 0.8, 1.0],  # 0.9,
                  # 'reg_alpha': [0, 0.1, ],  # 0.5
                  # 'reg_lambda': [0.01, 0.05, 1],  # 0.01,
                  'silent': [1],
                  'random_state': [1080],
                  }

    clf = GridSearchCV(LGBMClassifier(), parameters, n_jobs=get_recommend_cpu_count(),
                       cv=KFold(n_splits=3, random_state=42),
                       verbose=1, refit=True)
    return clf


def grid_search(clf):
    train_data = read_train_join_mall()
    train_data = train_data.sort_values(by='time_stamp')
    train_label = preprocessing.LabelEncoder().fit_transform(train_data['shop_id'])

    for mall_id in ['m_7374']:  # train_data['mall_id'].unique():
        X_train, y_train = DataVector.data_to_vec(mall_id,
                                                  [LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(),
                                                   PriceToVec()],
                                                  train_data, train_label)
        # print('fit.....')
        clf.fit(X_train, y_train)
        # print('fit done')

        print('{} score: {}'.format(mall_id, clf.best_score_))
        for name, val in clf.best_params_.items():
            print("{}  {}".format(name, val))
        print('----------')
        with open('./console_output/grid_search_res.txt', 'a') as f:
            f.write('{} score: {}\n'.format(mall_id, clf.best_score_))
            for name, val in clf.best_params_.items():
                f.write("{}  {}\n".format(name, val))
            f.write('------\n\n\n')
            f.flush()


if __name__ == '__main__':
    grid_search(lightgbm())

    # train_data = read_train_join_mall()
    # train_data = train_data.loc[train_data['mall_id'] == 'm_6803']
    # train_data = train_data.sort_values(by='time_stamp')
    # train_label = train_data['shop_id']
    # train_data, test_data, train_label, test_label = train_test_split(train_data, train_label, 0.2)
    #
    # b = ModelBase()
    # X_train, y_train, X_test, y_test = b._train_and_test_to_vec('m_6803',
    #                                                             [LocationToVec2(), WifiToVec(), WifiStrongToVec(),
    #                                                              WifiKStrongToVec(),
    #                                                              PriceToVec()],
    #                                                             train_data, train_label, test_data, test_label)
    # clf = OneVsRestClassifier(RandomForestClassifier(n_jobs=4, n_estimators=400,
    #                                                  random_state=42, class_weight='balanced'))
    #
    # print('fit.....')
    # clf.fit(X_train, y_train)
    #
    # print('fit done')
    # print(accuracy_score(y_test, clf.predict(X_test)))
