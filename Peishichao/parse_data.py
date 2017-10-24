# -*- coding: utf-8 -*-
# @Date    : 2017/10/20
# @Author  : hrwhisper
import pandas as pd


def read_mall_data():
    mall_data_path = '../data/mall.csv'
    return pd.read_csv(mall_data_path)


def read_train_data():
    train_data_path = '../data/train.csv'
    return pd.read_csv(train_data_path)


def read_test_data():
    test_data_path = '../data/test.csv'
    test_data = pd.read_csv(test_data_path)
    return test_data


def read_train_join_mall():
    mall_data = read_mall_data()
    train_data = read_train_data()  # 1138015
    return train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')


if __name__ == '__main__':
    mall_data = read_mall_data()
    train_data = read_train_data()
    # print(train_data.head())
    res = train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
    # print(res.head())
    print(res.loc[res['mall_id'] == 'm_1409'].head())
    # print(res.info())
