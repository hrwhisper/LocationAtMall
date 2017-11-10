# -*- coding: utf-8 -*-
# @Date    : 2017/11/10
# @Author  : hrwhisper
"""
    classifier voting. the idea is the same as sklearn's VotingClassifier.
    But it load the probability result file.
"""

import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score

from common_helper import ModelBase


class ModelVoting(ModelBase):
    def __init__(self, estimators, weights=None):
        super().__init__(save_model=False, use_multiprocess=False)
        self.estimators = estimators
        self.weights = weights

    def _single_trained_by_mall_and_predict_location(self, vec_func, train_data, train_label, test_data,
                                                     test_label=None):
        ans = {}
        is_train = test_label is not None
        total_score = 0
        for ri, mall_id in enumerate(train_data['mall_id'].unique()):
            y_test = test_label[test_data['mall_id'] == mall_id] if test_label is not None else None
            probas = [
                pd.read_csv('{}/{}/{}_{}.csv'.format(self.RESULT_SAVE_BASE_PATH, name,
                                                     'train' if is_train else 'test', mall_id)).set_index('row_id')
                for name in self.estimators
            ]

            class_ = probas[0].columns.values
            res = np.average([p.values for p in probas], weights=self.weights, axis=0)
            predicted = class_[np.argmax(res, axis=1)]
            # print(predicted)

            for row_id, label in zip(test_data[test_data['mall_id'] == mall_id]['row_id'], predicted):
                ans[row_id] = label

            if is_train:
                score = accuracy_score(y_test, predicted)
                total_score += score
                print(ri, mall_id, score)
            else:
                print(ri, mall_id)

        if is_train:
            cnt = train_data['mall_id'].unique().shape[0]
            print("Mean: {}".format(total_score / cnt))
        return ans


def train_test():
    task = ModelVoting(['random forest', 'binary random forest'])
    task.train_test(vec_func=None)
    task.train_and_on_test_data(vec_func=None)


if __name__ == '__main__':
    train_test()
