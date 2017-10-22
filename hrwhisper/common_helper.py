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
from parse_data import read_mall_data, read_train_data, read_test_data


def trained_and_predict_location(cls, X_train, y_train, X_test):
    print('fitting....')
    cls = cls.fit(X_train, y_train)
    print('predict....')
    predicted = cls.predict(X_test)
    return predicted


def train_test_split(X, y, test_size=0.2):
    train_size = int((1 - test_size) * X.shape[0])
    return X.iloc[:train_size], X.iloc[train_size:], y.iloc[:train_size], y.iloc[train_size:]


class XXToVec(ABC):
    def __init__(self, feature_save_path, how_to_vec_save_path):
        self.FEATURE_SAVE_PATH = feature_save_path
        self.HOW_TO_VEC_SAVE_PATH = how_to_vec_save_path

    @abc.abstractclassmethod
    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        """

        :param train_data:
        :param mall_id:
        :param renew:
        :param should_save:
        :return:
        """

    @abc.abstractclassmethod
    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        """

        :param test_data:
        :param mall_id:
        :param renew:
        :return:
        """


class ModelBase(object):
    def __init__(self, test_ratio=0.2, random_state=42):
        self._test_ratio = test_ratio
        self._random_state = random_state

    def get_name(self):
        return self.__class__.__name__

    def _get_classifiers(self):
        """
        :return: dict. {name:classifer}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=3, n_estimators=100, random_state=self._random_state),
        }

    def _trained_by_mall_and_predict_location(self, vec_func, train_data, test_data, has_test_label=True):
        """

        :param vec_func:
        :param train_data:
        :param test_data:
        :param has_test_label: bool
        :return:
        """
        ans = {}
        for mall_id in train_data['mall_id'].unique():
            vectors = []
            for func in vec_func:
                vectors.append(func.train_data_to_vec(train_data, mall_id))
            X_train = sparse.hstack(vectors)
            y_train = train_data.loc[train_data['mall_id'] == mall_id]['shop_id']

            vectors = []
            for func in vec_func:
                vectors.append(func.test_data_to_vec(test_data, mall_id))

            X_test = sparse.hstack(vectors)
            assert X_test.shape[0] == len(test_data.loc[test_data['mall_id'] == mall_id])

            print(X_train.shape, y_train.shape)
            print(X_test.shape)
            if has_test_label:
                y_test = test_data.loc[test_data['mall_id'] == mall_id]['shop_id']
                print(y_test.shape)

            classifiers = self._get_classifiers()
            for name, cls in classifiers.items():
                predicted = trained_and_predict_location(cls, X_train, y_train, X_test)
                if has_test_label:
                    score = accuracy_score(y_test, predicted)
                    ans[name] = ans.get(name, 0) + score
                    print(mall_id, name, score)
                else:
                    for row_id, label in zip(test_data.loc[test_data['mall_id'] == mall_id]['row_id'], predicted):
                        ans[row_id] = label
                        # joblib.dump(cls, './model_save/use_wifi_{}_{}.pkl'.format(name, mall_id))
        return ans

    def train_test(self, vec_func):
        """

        :param vec_func: list of vector function
        :return:
        """
        # ------input data -----------
        mall_data = read_mall_data()
        train_data = read_train_data()  # 1138015
        train_data = train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
        train_data = train_data.sort_values(by='time_stamp')
        train_label = train_data['shop_id']
        train_data, test_data, _, _ = train_test_split(train_data, train_label, self._test_ratio)

        cnt = train_data['mall_id'].unique().shape[0]
        total_cnt = self._trained_by_mall_and_predict_location(vec_func, train_data, test_data, has_test_label=True)
        for name, score in total_cnt.items():
            print("{} Mean: {}".format(name, score / cnt))

    def train_and_on_test_data(self, vec_func):
        mall_data = read_mall_data()
        train_data = read_train_data()  # 1138015
        train_data = train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
        test_data = read_test_data()
        ans = self._trained_by_mall_and_predict_location(vec_func, train_data, test_data, False)

        with open('./res.csv', 'w') as f:
            f.write('row_id,shop_id\n')
            for row_id in test_data['row_id']:
                f.write('{},{}\n'.format(row_id, ans[row_id]))
