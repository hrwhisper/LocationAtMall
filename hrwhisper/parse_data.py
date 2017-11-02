# -*- coding: utf-8 -*-
# @Date    : 2017/10/20
# @Author  : hrwhisper
import pandas as pd


def read_mall_data():
    mall_data_path = '../data/mall.csv'
    return pd.read_csv(mall_data_path)


def read_train_data():
    _path = '../data/train_row_id.csv'
    return pd.read_csv(_path, dtype={'row_id': str})


def read_test_data():
    test_data_path = '../data/test.csv'
    return pd.read_csv(test_data_path, dtype={'row_id': str})


def read_train_join_mall():
    mall_data = read_mall_data()
    train_data = read_train_data()  # 1138015
    return train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')


def add_row_id_for_train_data():
    train_data = pd.read_csv('../data/train.csv')
    df1 = train_data.assign(row_id=pd.Series(['_{}'.format(i) for i in range(train_data.shape[0])]))
    df1.to_csv('../data/train_row_id.csv')


if __name__ == '__main__':
    read_test_data()
    # mall_data = read_mall_data()
    # train_data = read_train_data()
    # # print(train_data.head())
    # res = train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
    # # print(res.head())
    # print(res.loc[res['mall_id'] == 'm_1409'].head())
    # # print(res.info())
    add_row_id_for_train_data()
    print('add')
    t = read_train_data()
    print(t[[True, True] + [False] * (t.shape[0] - 2)])
    # print(t.head())
