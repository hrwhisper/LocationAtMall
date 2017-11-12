# -*- coding: utf-8 -*-
# @Date    : 2017/10/27
# @Author  : hrwhisper

import numpy as np
import matplotlib.pyplot as plt


def draw_wifi(wifi_counter, mall_id):
    N = len(wifi_counter)
    height = [len(l) for l in wifi_counter.values()]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, height, width)

    ax.set_ylabel('Counts')
    ax.set_title('mall={}  WIFI co-occurrence statics'.format(mall_id))
    ax.set_xticks(ind + width / 2)
    # ax.set_xticklabels(list(wifi_counter.keys()))
    plt.show()
