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
    """
        划分训练集依据： 总体按时间排序后20%
    """

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
            'random forest': RandomForestClassifier(n_jobs=os.cpu_count() // 2, n_estimators=200,
                                                    random_state=self._random_state, class_weight='balanced'),
        }

    def _data_to_vec(self, mall_id, vec_func, data, label=None, is_train=True):
        vectors = [func.train_data_to_vec(data, mall_id) if is_train else func.test_data_to_vec(data, mall_id)
                   for func in vec_func]
        X = sparse.hstack(vectors)
        y = label[data['mall_id'] == mall_id] if label is not None else None
        return X, y

    def _train_and_test_to_vec(self, mall_id, vec_func, train_data, train_label, test_data, test_label=None):
        X_train, y_train = self._data_to_vec(mall_id, vec_func, train_data, train_label)
        X_test, y_test = self._data_to_vec(mall_id, vec_func, test_data, test_label, is_train=False)
        return X_train, y_train, X_test, y_test

    def _trained_by_mall_and_predict_location(self, vec_func, train_data, train_label, test_data, test_label=None):
        """

        :param vec_func:
        :param train_data:
        :param train_label
        :param test_data:
        :param test_label:
        :return:
        """
        ans = {}
        cls_report = {}
        for ri, mall_id in enumerate(train_data['mall_id'].unique()):
            X_train, y_train, X_test, y_test = self._train_and_test_to_vec(mall_id, vec_func, train_data,
                                                                           train_label, test_data, test_label)
            classifiers = self._get_classifiers()
            for name, cls in classifiers.items():
                predicted = trained_and_predict_location(cls, X_train, y_train, X_test)
                for row_id, label in zip(test_data[test_data['mall_id'] == mall_id]['row_id'], predicted):
                    ans[row_id] = label

                if test_label is not None:
                    score = accuracy_score(y_test, predicted)
                    cls_report[name] = cls_report.get(name, 0) + score
                    print(ri, mall_id, name, score)
                else:
                    print(ri, mall_id)

        if test_label is not None:
            cnt = train_data['mall_id'].unique().shape[0]
            classifiers = self._get_classifiers()
            for name, score in cls_report.items():
                print("{} Mean: {}".format(classifiers[name], score / cnt))
        return ans

    def train_test(self, vec_func, target_column='shop_id'):
        """

        :param vec_func: list of vector function
        :param target_column: the target column you want to predict.
        :return:
        """
        # ------input data -----------
        train_data = read_train_join_mall()
        train_data = train_data.sort_values(by='time_stamp')
        train_label = train_data[target_column]
        train_data, test_data, train_label, test_label = train_test_split(train_data, train_label, self._test_ratio)

        ans = self._trained_by_mall_and_predict_location(vec_func, train_data, train_label, test_data, test_label)

    def train_and_on_test_data(self, vec_func, target_column='shop_id'):
        train_data = read_train_join_mall()
        train_label = train_data[target_column]
        test_data = read_test_data()

        ans = self._trained_by_mall_and_predict_location(vec_func, train_data, train_label, test_data)
        _save_path = './result'
        if not os.path.exists(_save_path):
            os.mkdir(_save_path)
        with open(_save_path + '/hrwhisper_res_{}.csv'.format(time.strftime("%Y-%m-%d-%H-%M-%S")), 'w') as f:
            f.write('row_id,shop_id\n')
            for row_id in test_data['row_id']:
                f.write('{},{}\n'.format(row_id, ans[row_id]))
        print('done')


class ModelBase2(ModelBase):
    """
        划分训练集依据： 每个商场按时间排序后20%
        建议用ModelBase，而不是ModelBase2，ModelBase更能模拟线上测试。
    """

    def __init__(self, test_ratio=0.2, random_state=42):
        super().__init__(test_ratio, random_state)

    def get_name(self):
        return self.__class__.__name__

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
        with open(_save_path + '/hrwhisper_res_{}.csv'.format(time.strftime("%Y-%m-%d-%H-%M-%S")), 'w') as f:
            f.write('row_id,shop_id\n')
            for row_id in _test_data['row_id']:
                f.write('{},{}\n'.format(row_id, ans[row_id]))
        print('done')
