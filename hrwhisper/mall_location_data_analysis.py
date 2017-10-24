# -*- coding: utf-8 -*-
# @Date    : 2017/10/24
# @Author  : hrwhisper

from parse_data import read_mall_data
from use_location import get_distance_by_latitude_and_longitude, center_latitudes_and_longitudes


def mall_area():
    """
    计算中心点、以及mall大小
    """

    def cal_mall_area(data, mall_id):
        data = data[data['mall_id'] == mall_id]
        x = list(data['latitude'])
        y = list(data['longitude'])
        center = center_latitudes_and_longitudes(list(zip(x, y)))
        max_area = 0
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                max_area = max(max_area, get_distance_by_latitude_and_longitude(x[i], y[i], x[j], y[j]))
        return max_area, center[0], center[1]

    train_data = read_mall_data()  # read_train_join_mall()
    with open('./feature_save/mall_center_and_area.csv', 'w') as f:
        f.write('mall_id,max_area,center_latitude,center_longitude\n')
        for mall_id in train_data['mall_id'].unique():
            max_area, lan, long = cal_mall_area(train_data, mall_id)
            print(mall_id, max_area, lan, long)
            f.write('{},{},{},{}\n'.format(mall_id, max_area, lan, long))


if __name__ == '__main__':
    mall_area()
