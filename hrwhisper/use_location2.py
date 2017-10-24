# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
    经纬度 超过中心点多少的去掉。
    好像没啥用？
"""
from math import sin, cos, atan2, sqrt, pi

import pandas as pd
import gpxpy.geo
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from common_helper import ModelBase, XXToVec
from use_wifi import WifiToVec


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
    _mall_center_and_area = pd.read_csv('./feature_save/mall_center_and_area.csv')
    MAX_EXCEED_AREA = 0.52
    """
    dis 100  0.9019085399039125
    """

    def __init__(self):
        super().__init__('./feature_save/location_features_{}_{}.pkl', './feature_save/location_features_{}_{}.pkl')

    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        """
        :param train_data: pandas. train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
        :param mall_id: str
        :param renew: renew the feature
        :param should_save: bool, should save the feature on disk or not.
        :return: csr_matrix
        """
        if renew:
            train_data = train_data.loc[train_data['mall_id'] == mall_id]
            indptr = [0]
            indices = []
            data = []

            t = self._mall_center_and_area[self._mall_center_and_area['mall_id'] == mall_id]
            center_lat, center_log = t['center_latitude'].iat[0], t['center_longitude'].iat[0]
            max_area = t['max_area'].iat[0]

            for log, lat in zip(train_data['longitude'], train_data['latitude']):
                indices.extend([0, 1])

                dis_to_center = get_distance_by_latitude_and_longitude(lat, log, center_lat, center_log)
                if max_area * self.MAX_EXCEED_AREA < dis_to_center:
                    data.extend([center_lat, center_log])
                else:
                    data.extend([lat, log])

                indptr.append(len(indices))

            features = csr_matrix((data, indices, indptr))
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('train', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
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
                    data.extend([center_lat, center_log])
                else:
                    data.extend([lat, log])
                indptr.append(len(indices))

            features = csr_matrix((data, indices, indptr))
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return features


class UseLoc(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=100, random_state=self._random_state),
        }


def train_test():
    task = UseLoc()
    task.train_test([LocationToVec(), WifiToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
