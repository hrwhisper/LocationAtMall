# -*- coding: utf-8 -*-
# @Date    : 2017/11/10
# @Author  : hrwhisper
"""
    classifier voting. the idea is the same as sklearn's VotingClassifier.
    But it load the probability result file.

    ['random forest 0.9169', 'binary random forest 0.9174'] [1, 1]
    Mean: 0.9192280256032719
    online:0.9214

    ['random forest 0.9169', 'binary random forest 0.9174','binary xgb 0.9142'] [10, 10, 5]
    Mean: 0.920154410602307
    online:0.9234

    ['random forest 0.91828', 'binary random forest 0.91813', 'binary xgb 0.9147'] weights = [10, 9, 6]
    Mean: 0.920985617387946
    online:0.9234 比上面的略高

    ['random forest 0.9185', 'binary random forest 0.91813', 'binary xgb 0.9147'] weights = [10, 9, 6]
    Mean: 0.9210399096493549
    online:0.9237

    ['random forest 0.9198', 'binary random forest 0.91813', 'binary xgb 0.9147'] [1, 0.8, 0.4]
    Mean: 0.9221356685641695
    online: 0.9243

    ['random forest 0.9198', 'binary random forest 0.9200', 'binary xgb 0.9147'] [0.98, 1, 0.47]
    Mean: 0.9232737732023647
    online: 0.9264
    online B:0.9207

    ['random forest 0.919969', 'binary random forest 0.9200', 'binary xgb 0.9147'] [80, 78, 34]
    Mean: 0.923497179961667
    online B:0.9207 略高于上面


    ['random forest 0.919969', 'binary random forest not price 0.91998', 'binary xgb 0.9149'] [78, 80, 34]
    Mean: 0.923978501467714
    online B:0.9213


    ['random forest not price 0.9199', 'binary random forest not price 0.91998', 'binary xgb 0.9149', 'xgb 0.9123'] [78, 80, 34, 5]
    Mean: 0.9240684683620611
    online B 0.9115
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
    models = ['random forest not price 0.9199', 'binary random forest not price 0.91998', 'binary xgb 0.9149',
              'xgb 0.9123']
    weights = [78, 80, 34, 5]  # Mean: 0.9240684683620611
    task = ModelVoting(models, weights=weights)
    task.train_test(vec_func=None)
    print(models, weights)
    task.train_and_on_test_data(vec_func=None)


if __name__ == '__main__':
    train_test()
