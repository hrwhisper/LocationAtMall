# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
    经纬度*10, 线上0.9101
    LocationToVec3(), WifiToVec3(), TimeToVec()
    RandomForestClassifier(class_weight='balanced',n_estimators=400,
                    n_jobs=-1, random_state=42,e) Mean: 0.9093965396494474
"""

from math import sin, cos, atan2, sqrt, pi

import gpxpy.geo
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier

from common_helper import ModelBase, XXToVec

"""
LocationToVec(), WifiToVec3(), TimeToVec()
RandomForestClassifier(bootstrap=True, class_weight='balanced',
            criterion='gini', max_depth=None, max_features='auto',
            max_leaf_nodes=None, min_impurity_decrease=0.0,
            min_impurity_split=None, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=400, n_jobs=-1, oob_score=False, random_state=42,
            verbose=0, warm_start=False) Mean: 0.9093965396494474
"""


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


class LocationToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/location_features_{}_{}.pkl')
        self.scale = 10

    def _do_transform(self, train_data):
        indptr = [0]
        indices = []
        data = []
        for log, lat in zip(train_data['longitude'], train_data['latitude']):
            indices.extend([0, 1])
            data.extend([log * self.scale, lat * self.scale])
            indptr.append(len(indices))
        return csr_matrix((data, indices, indptr))

    def _fit_transform(self, train_data, mall_id):
        return self._do_transform(train_data)

    def _transform(self, test_data, mall_id):
        return self._do_transform(test_data)


class UseLoc(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=3, n_estimators=200, random_state=self._random_state,
                                                    class_weight='balanced'),
        }


def train_test():
    task = UseLoc()
    task.train_test([LocationToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
