# -*- coding: utf-8 -*-
# @Date    : 2017/11/6
# @Author  : hrwhisper


# -*- coding: utf-8 -*-
# @Date    : 2017/10/29
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

from common_helper import ModelBase, DataVector, safe_dump_model
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
        self.label_encoders = None
        self.new_feature_save_base_path = './feature_save/stacking/'

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_estimators=400,
                                                    random_state=self._random_state,
                                                    class_weight='balanced',
                                                    n_jobs=self.n_jobs),
            'xgb': XGBClassifier(colsample_bytree=0.7,
                                 learning_rate=0.025,
                                 max_depth=6,
                                 min_child_weight=1,
                                 missing=-999,
                                 n_jobs=os.cpu_count() // 3 * 2,
                                 n_estimators=500,
                                 objective='binary:logistic',
                                 random_state=1024,
                                 _silent=1,
                                 subsample=0.6),
            'binary random forest': OneVsRestClassifier(RandomForestClassifier(n_estimators=400,
                                                                               random_state=self._random_state,
                                                                               class_weight='balanced'),
                                                        n_jobs=self.n_jobs),
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
        _train_label = _train_data[target_column].values
        _test_data = read_test_data()

        self.label_encoders = label_encoders = {
            mall_id: preprocessing.LabelEncoder().fit(_train_data.loc[_train_data['mall_id'] == mall_id][target_column])
            for mall_id in _train_data['mall_id'].unique()
        }

        train_res = {mall_id: [] for mall_id in label_encoders.keys()}
        test_res = {mall_id: [] for mall_id in label_encoders.keys()}

        kf = KFold(n_splits=fold, random_state=self._random_state)

        for clf_name, clf in self._get_classifiers():
            oof_train = {
                mall_id: np.zeros((_train_data.shape[0], len(le.classes_))) for mall_id, le in label_encoders.items()
            }
            oof_test = {
                mall_id: np.zeros((_test_data.shape[0], len(le.classes_))) for mall_id, le in label_encoders.items()
            }

            for i, (train_index, test_index) in enumerate(kf.split(_train_data)):
                self._trained_and_predict(vec_func, _train_data, _train_label, _test_data, oof_train, oof_test,
                                          train_index, test_index, i, clf_name)
            for mall_id, arr in oof_train:
                train_res[mall_id].append(arr)
            for mall_id, arr in oof_test:
                test_res[mall_id].append(arr / fold)

        safe_dump_model(train_res, self.new_feature_save_base_path + 'new_train_feature.pkl')
        safe_dump_model(train_res, self.new_feature_save_base_path + 'new_test_feature.pkl')
        print('feature_save done')
        # clf = self._get_classifiers()['random forest']
        # for mall_id, X_train in train_res.items():
        #     X_test = train_res[mall_id]
        #
        #     # todo hstack
        #     y_train = _train_data.loc[_train_data[mall_id] == mall_id]
        #
        #     clf.fit(X_train, y_train)

    # joblib.dump(oof_train, self.feature_save_path + '_oof_train.pkl', compress=3)
    # joblib.dump(oof_test, self.feature_save_path + '_oof_test.pkl', compress=3)

    # with open(self.feature_save_path, 'w') as f:
    #     f.write('row_id,{}\n'.format(','.join(str(i) for i in range(n))))
    #     for i, row_id in enumerate(_train_data['row_id']):
    #         f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_train[i]))))
    #     for i, row_id in enumerate(_test_data['row_id']):
    #         f.write('{},{}\n'.format(row_id, ','.join(list(str(x) for x in oof_test[i]))))
    # print('done')

    def _trained_and_predict(self, vec_func, _train_data, _train_label, R_X_test,
                             oof_train, oof_test, _train_index, _test_index, cur_fold, clf_name):
        mall_id_list = sorted(list(_train_data.iloc[_train_index]['mall_id'].unique()))
        _train_index = set(_train_index)
        _test_index = set(_test_index)
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

            X_train, y_train, X_test, y_test = DataVector.train_and_test_to_vec(mall_id, vec_func, fold_X_train,
                                                                                fold_y_train, fold_X_test,
                                                                                fold_y_test)
            y_train = self.label_encoders[mall_id].transform(y_train)
            y_test = self.label_encoders[mall_id].transform(y_test)

            cur_save_path = '{}/{}/{}_{}'.format(self.SAVE_MODEL_BASE_PATH, clf_name, mall_id, cur_fold)
            if self.renew:
                clf = self._get_classifiers()[clf_name]
                clf.fit(X_train, y_train)
                if self.SAVE_MODEL:
                    safe_dump_model(clf, cur_save_path, compress=5)
            else:
                clf = joblib.load(cur_save_path)

            oof_train[mall_id][test_index] = clf.predict_log_proba(X_test)

            predicted = clf.predict(X_test)
            score = accuracy_score(y_test, predicted)
            print(ri, mall_id, score)

            X_test, _ = DataVector.data_to_vec(mall_id, vec_func, R_X_test, None, is_train=False)
            oof_test[mall_id] += clf.predict_log_proba(X_test)


def train_test():
    task = ModelStacking(renew=True)
    task.train_test([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])
    task.train_and_on_test_data([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])


if __name__ == '__main__':
    train_test()
