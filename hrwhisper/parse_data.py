# -*- coding: utf-8 -*-
# @Date    : 2017/10/20
# @Author  : hrwhisper
import pandas as pd


def read_train_data():
    mall_data_path = '../data/训练数据-ccf_first_round_shop_info.csv'
    train_data_path = '../data/训练数据-ccf_first_round_user_shop_behavior.csv'
    return pd.read_csv(mall_data_path), pd.read_csv(train_data_path)


def read_test_data():
    test_data_path = '../data/AB榜测试集-evaluation_public.csv'
    test_data = pd.read_csv(test_data_path)
    return test_data


if __name__ == '__main__':
    mall_data, train_data = read_train_data()
    print(mall_data)
    print(train_data.head())
    # res = (train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall'))
    # print(res.head())
    # print(res.info())

