# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
    经纬度 超过中心点多少的去掉。
    好像没啥用？
"""

import pandas as pd
from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec
from use_location import get_distance_by_latitude_and_longitude


class LocationToVec2(XXToVec):
    _mall_center_and_area = pd.read_csv('./feature_save/mall_center_and_area.csv')
    MAX_EXCEED_AREA = 0.52

    def __init__(self):
        super().__init__('./feature_save/location_features_{}_{}.pkl')

    def _fit_transform(self, train_data, mall_id):
        return self._transform(train_data, mall_id)

    def _transform(self, test_data, mall_id):
        indptr = [0]
        indices = []
        data = []

        t = self._mall_center_and_area[self._mall_center_and_area['mall_id'] == mall_id]
        center_lat, center_log = t['center_latitude'].iat[0], t['center_longitude'].iat[0]
        max_area = t['max_area'].iat[0]

        for log, lat in zip(test_data['longitude'], test_data['latitude']):
            indices.extend([0, 1])

            dis_to_center = get_distance_by_latitude_and_longitude(lat, log, center_lat, center_log)
            if max_area * self.MAX_EXCEED_AREA < dis_to_center:
                data.extend([center_lat, center_log]) # TODO get the wifi cosine distance.
            else:
                data.extend([lat, log])
            indptr.append(len(indices))

        return csr_matrix((data, indices, indptr))


def train_test():
    task = ModelBase()
    task.train_test([LocationToVec2()])
    # task.train_and_on_test_data([LocationToVec2()])


if __name__ == '__main__':
    train_test()
