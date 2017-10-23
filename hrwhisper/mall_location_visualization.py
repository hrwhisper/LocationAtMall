# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper

import matplotlib.pyplot as plt

from parse_data import read_train_join_mall, read_mall_data


def only_mall_visualization():
    train_data = read_mall_data()  # read_train_join_mall()
    print(train_data.size)
    x = train_data['latitude']
    y = train_data['longitude']

    id2color = {mall_id: i for i, mall_id in enumerate(train_data['mall_id'].unique())}
    print(id2color)
    colors = [id2color[i] for i in train_data['mall_id']]
    print(colors)
    area = 100
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()



if __name__ == '__main__':
    only_mall_visualization()
