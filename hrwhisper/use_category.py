# -*- coding: utf-8 -*-
# @Date    : 2017/10/28
# @Author  : hrwhisper
import os

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from common_helper import ModelBase, XXToVec
from parse_data import read_mall_data



class CategoryToVec(XXToVec):
    """
        using the category feature which has been predicted by 'predict_category.py'
    """
    CATEGORY_ID = {_id: i for i, _id in enumerate(sorted(set(read_mall_data()['category_id'])))}
    TRAIN_CATEGORY = pd.read_csv('./feature_save/predicted_category.csv')

    def __init__(self):
        super().__init__('./feature_save/time_features_{}_{}.pkl', './feature_save/time_features_{}_{}.pkl')

    def _extract_feature(self, data):
        d = data.join(self.TRAIN_CATEGORY.set_index('row_id'), on='row_id', rsuffix='_train')
        d = d['p_category_id']
        features = np.array([self.CATEGORY_ID[i] for i in d]).reshape(-1, 1)
        return csr_matrix(features)

    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        """
        :param data: pandas. train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
        :param mall_id: str
        :param renew: renew the feature
        :param should_save: bool, should save the feature on disk or not.
        :return: csr_matrix
        """
        if renew:
            train_data = train_data[train_data['mall_id'] == mall_id]
            features = self._extract_feature(train_data)
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('train', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data[test_data['mall_id'] == mall_id]
            features = self._extract_feature(test_data)
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return features


class UseCategory(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=os.cpu_count() // 2, n_estimators=200,
                                                    random_state=self._random_state, class_weight='balanced'),
        }


def train_test():
    task = UseCategory()
    task.train_test([CategoryToVec()], 'shop_id')
    # task.train_and_on_test_data([CategoryToVec()])


if __name__ == '__main__':
    train_test()
