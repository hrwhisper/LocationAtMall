# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
import abc
import collections
import os
import time

from scipy import sparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from parse_data import read_test_data, read_train_join_mall


def trained_and_predict_location(cls, X_train, y_train, X_test):
    print('fitting....')
    cls = cls.fit(X_train, y_train)
    print('predict....')
    predicted = cls.predict(X_test)
    return predicted


def train_test_split(X, y, test_size=0.2):
    train_size = int((1 - test_size) * X.shape[0])
    return X.iloc[:train_size], X.iloc[train_size:], y.iloc[:train_size], y.iloc[train_size:]


class XXToVec(abc.ABC):
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
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=200, random_state=self._random_state,
                                                    class_weight='balanced'),
        }

    def _trained_by_mall_and_predict(self, vec_func, train_data, test_data, mall_id, has_test_label=True):
        """

        :param vec_func:
        :param train_data:
        :param test_data:
        :param mall_id:
        :param has_test_label: bool
        :return:
        """
        ans = {}
        vectors = [func.train_data_to_vec(train_data, mall_id) for func in vec_func]
        X_train = sparse.hstack(vectors)
        y_train = train_data['shop_id']
        # print(X_train.shape, y_train.shape)

        vectors = [func.test_data_to_vec(test_data, mall_id) for func in vec_func]
        X_test = sparse.hstack(vectors)
        assert X_test.shape[0] == test_data.shape[0]
        # print(X_test.shape)

        if has_test_label:
            y_test = test_data['shop_id']
            # print(y_test.shape)

        classifiers = self._get_classifiers()
        for name, cls in classifiers.items():
            predicted = trained_and_predict_location(cls, X_train, y_train, X_test)
            if has_test_label:
                score = accuracy_score(y_test, predicted)
                ans[name] = ans.get(name, 0) + score
                print(mall_id, name, score)
            else:
                for row_id, label in zip(test_data['row_id'], predicted):
                    ans[row_id] = label
                    # joblib.dump(cls, './model_save/use_wifi_{}_{}.pkl'.format(name, mall_id))
        return ans

    def train_test(self, vec_func):
        """

        :param vec_func: list of vector function
        :return:
        """
        # ------input data -----------
        train_data = read_train_join_mall()
        train_data = train_data.sort_values(by='time_stamp')

        total_cnt = collections.Counter()
        for ri, mall_id in enumerate(train_data['mall_id'].unique()):
            print(ri)
            cur_train_data = train_data[train_data['mall_id'] == mall_id]
            train_label = cur_train_data['shop_id']
            cur_train_data, cur_test_data, _, _ = train_test_split(cur_train_data, train_label, self._test_ratio)
            cur_cnt = self._trained_by_mall_and_predict(vec_func, cur_train_data, cur_test_data, mall_id,
                                                        has_test_label=True)
            total_cnt.update(cur_cnt)

        cnt = train_data['mall_id'].unique().shape[0]
        classifiers = self._get_classifiers()
        for name, score in total_cnt.items():
            print("{} Mean: {}".format(classifiers[name], score / cnt))

    def train_and_on_test_data(self, vec_func):
        train_data = read_train_join_mall()
        _test_data = read_test_data()
        train_data = train_data.sort_values(by='time_stamp')
        test_data = _test_data.sort_values(by='time_stamp')

        ans = {}
        for ri, mall_id in enumerate(test_data['mall_id'].unique()):
            print(ri)
            cur_train_data = train_data[train_data['mall_id'] == mall_id]
            cur_test_data = test_data[test_data['mall_id'] == mall_id]
            cur_ans = self._trained_by_mall_and_predict(vec_func, cur_train_data, cur_test_data, mall_id, False)
            ans.update(cur_ans)

        _save_path = './result'
        if not os.path.exists(_save_path):
            os.mkdir(_save_path)
        with open(_save_path + '/hrwhisper_res_{}.csv'.format(time.strftime("%Y%m%d-%H%M%S")), 'w') as f:
            f.write('row_id,shop_id\n')
            for row_id in _test_data['row_id']:
                f.write('{},{}\n'.format(row_id, ans[row_id]))
        print('done')
