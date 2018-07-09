# -*- coding: utf-8 -*-
# @Date    : 2017/10/24
# @Author  : hrwhisper

import os
from math import pi, cos, sin, atan2, sqrt

import gpxpy.geo

from parse_data import read_mall_data


def get_distance_by_latitude_and_longitude(lat1, lon1, lat2, lon2):
    return gpxpy.geo.haversine_distance(lat1, lon1, lat2, lon2)


def center_latitudes_and_longitudes(geo_coordinates):
    """

    :param geo_coordinates: [[latitude,longtitude],...]
    :return: [latitude,longitudes]
    """
    x = y = z = 0
    for (lat, lng) in geo_coordinates:
        lat, lng = lat * pi / 180, lng * pi / 180
        x += cos(lat) * cos(lng)
        y += cos(lat) * sin(lng)
        z += sin(lat)

    x = x / len(geo_coordinates)
    y = y / len(geo_coordinates)
    z = z / len(geo_coordinates)
    lng = atan2(y, x)
    hyp = sqrt(x ** 2 + y ** 2)
    lat = atan2(z, hyp)
    return lat * 180 / pi, lng * 180 / pi


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
    os.makedirs('./feature_save', exist_ok=True)
    with open('./feature_save/mall_center_and_area.csv', 'w') as f:
        f.write('mall_id,max_area,center_latitude,center_longitude\n')
        for mall_id in train_data['mall_id'].unique():
            max_area, lan, long = cal_mall_area(train_data, mall_id)
            print(mall_id, max_area, lan, long)
            f.write('{},{},{},{}\n'.format(mall_id, max_area, lan, long))


if __name__ == '__main__':
    mall_area()
