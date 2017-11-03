# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
import abc
import os
import time

from scipy import sparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

from parse_data import read_test_data, read_train_join_mall


def train_test_split(X, y, test_size=0.2):
    train_size = int((1 - test_size) * X.shape[0])
    return X.iloc[:train_size], X.iloc[train_size:], y.iloc[:train_size], y.iloc[train_size:]


class XXToVec(abc.ABC):
    def __init__(self, feature_save_path):
        self.FEATURE_SAVE_PATH = feature_save_path

    @abc.abstractclassmethod
    def _fit_transform(self, train_data, mall_id):
        pass

    @abc.abstractclassmethod
    def _transform(self, test_data, mall_id):
        pass

    def fit_transform(self, train_data, mall_id, renew=True, should_save=False):
        """

        :param train_data:
        :param mall_id:
        :param renew
        :param should_save:
        :return:
        """
        if renew:
            train_data = train_data.loc[train_data['mall_id'] == mall_id]
            features = self._fit_transform(train_data, mall_id)
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('train', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return features

    def transform(self, test_data, mall_id, renew=True, should_save=False):
        """

        :param test_data:
        :param mall_id:
        :param renew
        :param should_save:
        :return:
        """
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            features = self._transform(test_data, mall_id)
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return features


class ModelBase(object):
    """
        多分类
        划分训练集依据： 总体按时间排序后20%
    """

    def __init__(self, test_ratio=0.2, random_state=42, n_jobs=None):
        self._test_ratio = test_ratio
        self._random_state = random_state
        if n_jobs is None:
            self.n_jobs = os.cpu_count() // 2 if os.name == 'nt' else os.cpu_count()
        else:
            self.n_jobs = n_jobs

    def get_name(self):
        return self.__class__.__name__

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=self.n_jobs, n_estimators=200,
                                                    random_state=self._random_state, class_weight='balanced'),
        }

    @staticmethod
    def trained_and_predict_location(cls, X_train, y_train, X_test, y_test=None):
        print('fitting....')
        cls = cls.fit(X_train, y_train)
        print('predict....')
        predicted = cls.predict(X_test)
        return predicted

    def _data_to_vec(self, mall_id, vec_func, data, label=None, is_train=True):
        vectors = [func.fit_transform(data, mall_id) if is_train else func.transform(data, mall_id)
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
                predicted = self.trained_and_predict_location(cls, X_train, y_train, X_test, y_test)
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
