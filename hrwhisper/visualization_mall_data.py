# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
画图
"""
import collections

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd

from parse_data import read_train_join_mall, read_mall_data
from use_location import center_latitudes_and_longitudes


def show_plt():
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.tight_layout()
    plt.show()


def only_mall_visualization(mall_id=None):
    """
    根据经纬度信息，画mall
    若给定mall_id则画特定mall否则画全部mall
    :param mall_id:  str
    :return:
    """
    train_data = read_mall_data()  # read_train_join_mall()
    if mall_id:
        train_data = train_data[train_data['mall_id'] == mall_id]

    x = train_data['latitude']
    y = train_data['longitude']

    if mall_id:
        id2color = {shop_id: i for i, shop_id in enumerate(train_data['shop_id'].unique())}
        colors = [id2color[i] for i in train_data['shop_id']]
    else:
        id2color = {mall_id: i for i, mall_id in enumerate(train_data['mall_id'].unique())}
        colors = [id2color[i] for i in train_data['mall_id']]

    counter = collections.Counter(zip(x, y))
    for (a, b), cnt in counter.items():
        if cnt > 1:
            plt.text(a, b, cnt)

    plt.scatter(x, y, s=100, c=colors, alpha=0.5)
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

    center = center_latitudes_and_longitudes(list(zip(x, y)))
    plt.scatter(center[0], center[1], s=1000, marker='s')

    show_plt()


def mall_shop_day_sales_volume(mall_id='m_1621'):
    """
    画出某店铺的每日销量
    """
    _train_data = read_train_join_mall()
    train_data = _train_data.loc[_train_data['mall_id'] == mall_id]
    train_data = train_data.assign(time_stamp=pd.to_datetime(train_data['time_stamp']))
    train_data['time_stamp'] = train_data['time_stamp'].dt.day

    total_count = [collections.Counter() for _ in range(31)]
    for shop_id, day in zip(train_data['shop_id'], train_data['time_stamp']):
        total_count[day - 1][shop_id] += 1

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    z = 0
    shop_dis = 60

    for shop_id in ['s_389866', 's_432426', 's_459836', 's_634174', 's_1215854',
                    's_1287028', 's_2110248', 's_2670603', 's_2862961', 's_2922711',
                    's_3418707', 's_3479448', 's_3558937', 's_3658245', 's_3711363',
                    's_3716008', 's_3790469', 's_4001714', 's_4021610', 's_4050122']:
        if total_count[-1][shop_id] > 0: continue # 只画最后一天没有卖东西的，减少数量
        xs = list(range(31))
        ys = [total_count[i][shop_id] for i in xs]
        ax.bar(xs, ys, z, zdir='y', alpha=0.8)
        z += shop_dis

    ax.set_xlabel('days')
    ax.set_ylabel('shops')
    ax.set_zlabel('sales volume')

    show_plt()


if __name__ == '__main__':
    # only_mall_visualization('m_968')
    # shop_mall_visualization('m_1621')
    mall_shop_day_sales_volume('m_968')
