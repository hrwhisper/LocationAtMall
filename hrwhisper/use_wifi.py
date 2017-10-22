# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    使用了wifi特征，类似BOW
"""
import pandas as pd
import numpy as np
import collections
from scipy.sparse import csr_matrix, hstack
from sklearn import naive_bayes, svm, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

from hrwhisper.parse_data import read_train_data, read_mall_data
from hrwhisper.common_helper import trained_and_predict_location, ModelBase


def location_to_vec(train_data, mall_id):
    """

    :param train_data:
    :return: csr_matrix
    """
    if train_data is None:
        train_data = read_train_data()  # 1138015
    location_feature = train_data[['longitude', 'latitude']]
    # return csr_matrix(location_feature.values)
    return preprocessing.scale(location_feature.values)


def wifi_to_vec(train_data, mall_id):
    """
    :param data: pandas. train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
    :param mall_id: str
    :return: csr_matrix
    """
    # _wifi_feature_save_path = './feature_save/wifi_features.pkl'
    # _wifi_bssid_save = './feature_save/wifi_bssid.pkl'
    wifi_bssid = set()
    min_strong = 0x7fffffff

    train_data = train_data.loc[train_data['mall_id'] == mall_id]
    for wifi_infos in train_data['wifi_infos']:
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            wifi_bssid.add(_id)
            min_strong = min(min_strong, int(_strong) - 100)

    wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
    indptr = [0]
    indices = []
    data = []
    for wifi_infos in train_data['wifi_infos']:
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            _id = wifi_bssid[_id]
            indices.append(_id)
            data.append(int(_strong) - min_strong)
        indptr.append(len(indices))

    wifi_features = csr_matrix((data, indices, indptr), dtype=int)  # TODO normalize
    # return preprocessing.scale(wifi_features, with_mean=False)
    # joblib.dump(wifi_features, _wifi_feature_save_path)
    # joblib.dump(wifi_bssid, _wifi_bssid_save)
    return wifi_features


class UseWifi(ModelBase):
    def __init__(self):
        super().__init__()


def train_test():
    task = UseWifi()
    task.train_test([wifi_to_vec])


if __name__ == '__main__':
    train_test()
