# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from hrwhisper.common_helper import trained_and_predict_location
from hrwhisper.parse_data import read_test_data, read_train_data, read_mall_data


def train_test():
    mall_data = read_mall_data()  # 8477
    train_data = read_train_data()  # 1138015
    mall_data = mall_data[['shop_id', 'longitude', 'latitude']]
    y_mall = mall_data['shop_id']
    X_mall = mall_data[['longitude', 'latitude']]
    y_train = train_data['shop_id']

    X_train = train_data[['longitude', 'latitude']]
    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.1, random_state=42)
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    # print(X_train.info())
    # print(X_test.info())
    # X_train = pd.concat([X_train, X_mall])
    # y_train = pd.concat([y_train,y_mall])
    cls = KNeighborsClassifier()
    predicted = trained_and_predict_location(cls, X_train, y_train, X_test)
    print(accuracy_score(y_test, predicted))
    # data = pd.concat([X_train, X_mall])
    # print(mall_data.info())
    # print(train_data.info())
    # print(data.info())


def get_result():
    mall_data = read_mall_data()
    train_data = read_train_data()  # 8477 1138015
    test_data = read_test_data()
    mall_data = mall_data[['shop_id', 'longitude', 'latitude']]
    y_mall = mall_data[['shop_id']]
    X_mall = mall_data[['longitude', 'latitude']]
    y_train = train_data[['shop_id']]
    X_train = train_data[['longitude', 'latitude']]
    X_test = test_data[['longitude', 'latitude']]
    predicted = trained_and_predict_location(KNeighborsClassifier(), X_train, y_train, X_test)
    np.save(r'./res.npy', predicted)
    with open('./res.csv', 'w') as f:
        for row_id, label in zip(test_data['row_id'], predicted):
            f.write('{},{}\n'.format(row_id, label))


if __name__ == '__main__':
    train_test()
