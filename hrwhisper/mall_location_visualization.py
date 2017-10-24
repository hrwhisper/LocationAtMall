# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
画图
"""
import matplotlib.pyplot as plt
from parse_data import read_train_join_mall, read_mall_data
from use_location import center_latitudes_and_longitudes, get_distance_by_latitude_and_longitude


def show_plt():
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.tight_layout()
    plt.show()


def only_mall_visualization(mall_id=None):
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


if __name__ == '__main__':
    only_mall_visualization('m_1621')
    # shop_mall_visualization('m_1621')
    # (Lat_A, Lng_A) = (32.060255, 118.796877)
    # (Lat_B, Lng_B) = (39.904211, 116.407395)
    # print(gpxpy.geo.haversine_distance(Lat_A, Lng_A, Lat_B, Lng_B))
