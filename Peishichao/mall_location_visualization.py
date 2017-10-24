# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
画图
"""
from math import radians, atan, acos, sin, tan, cos

import matplotlib.pyplot as plt
from parse_data import read_train_join_mall, read_mall_data


def show_plt():
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.tight_layout()
    plt.show()


def only_mall_visualization():
    train_data = read_mall_data()  # read_train_join_mall()
    print(train_data.size)
    x = train_data['latitude']
    y = train_data['longitude']

    id2color = {mall_id: i for i, mall_id in enumerate(train_data['mall_id'].unique())}
    colors = [id2color[i] for i in train_data['mall_id']]
    area = 100
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    show_plt()


def shop_mall_visualization(mall_id='m_4572'):
    """
    画出某mall_id商场的所有店铺和用户位置
    """
    train_data = read_train_join_mall()
    train_data = train_data[train_data['mall_id'] == mall_id]

    x = train_data['latitude']
    y = train_data['longitude']

    id2color = {mall_id: i for i, mall_id in enumerate(train_data['shop_id'].unique())}
    colors = [id2color[i] for i in train_data['shop_id']]
    plt.scatter(x, y, s=100, c=colors, alpha=0.5, marker='^')

    train_data = read_mall_data()
    train_data = train_data[train_data['mall_id'] == mall_id]
    x = train_data['latitude']
    y = train_data['longitude']

    colors = [id2color[i] for i in train_data['shop_id']]
    plt.scatter(x, y, s=600, c=colors, alpha=0.5)

    show_plt()


if __name__ == '__main__':
    # only_mall_visualization()
    shop_mall_visualization()
