# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
import abc
from abc import ABC
import collections
from scipy import sparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from hrwhisper.parse_data import read_mall_data, read_train_data


def trained_and_predict_location(cls, X_train, y_train, X_test):
    print('fitting....')
    cls = cls.fit(X_train, y_train)
    print('predict....')
    predicted = cls.predict(X_test)
    return predicted


class ModelBase(ABC):
    def __init__(self, test_size=0.2, random_state=42):
        self._test_size = test_size
        self._random_state = random_state

    def get_classifiers(self):
        """
        :return: dict. {name:classifer}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=-1, n_estimators=100, random_state=42),
        }

    def train_test(self, vec_func):
        """

        :param vec_func: list of vector function
        :return:
        """
        mall_data = read_mall_data()
        train_data = read_train_data()  # 1138015
        train_data = train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')

        total = collections.Counter()
        cnt = 0
        for mall_id in train_data['mall_id'].unique():
            vectors = []
            for func in vec_func:
                vectors.append(func(train_data, mall_id))
            # X_train = wifi_to_vec(train_data, mall_id)
            X_train = sparse.hstack(vectors)
            y_train = train_data.loc[train_data['mall_id'] == mall_id]['shop_id']
            X_train, X_test, y_train, y_test = train_test_split(X_train, y_train,
                                                                test_size=self._test_size,
                                                                random_state=self._random_state)
            # print(X_train.shape,y_train.shape)
            # print(X_test.shape,y_test.shape)
            cnt += 1
            classifiers = self.get_classifiers()
            for name, cls in classifiers.items():
                # cls = KNeighborsClassifier()
                # print(name)
                predicted = trained_and_predict_location(cls, X_train, y_train, X_test)
                score = accuracy_score(y_test, predicted)
                total[name] += score
                print(mall_id, name, score)
                joblib.dump(cls, './model_save/use_wifi_{}_{}.pkl'.format(name, mall_data))
        for name, score in total.items():
            print("{} Mean: {}".format(name, score / cnt))
