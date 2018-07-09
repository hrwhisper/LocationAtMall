# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
"""
    经纬度 超过中心点多少的去掉。
    好像没啥用？
"""
import collections
from datetime import datetime

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

from analysis_mall_location_data import get_distance_by_latitude_and_longitude
from common_helper import ModelBase, XXToVec

"""
LocationToVec(), WifiToVec(), TimeToVec()
RandomForestClassifier(bootstrap=True, class_weight='balanced',
            criterion='gini', max_depth=None, max_features='auto',
            max_leaf_nodes=None, min_impurity_decrease=0.0,
            min_impurity_split=None, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=400, n_jobs=-1, oob_score=False, random_state=42,
            verbose=0, warm_start=False) Mean: 0.9093965396494474
"""


class LocationToVec2(XXToVec):
    _mall_center_and_area = pd.read_csv('./feature_save/mall_center_and_area.csv')
    MAX_EXCEED_AREA = 1
    """
            scale10            scale 1
    0.52  0.9136276668284586    0.91339786
    0.6   0.9135071499148205
    0.7   0.9134939307403611
    0.8   0.913459231292
    1                           0.9137623822655955
    1.1                         0.913664140543424
    1.2                         0.91370422291071
    1.3                         0.9137034974928522
     0.914946325351 
    """

    def __init__(self):
        super().__init__('./feature_save/location_features_{}_{}.pkl')
        self.scale = 1

    def __get_wifi_number(self, train_data):
        wifi_and_date = collections.defaultdict(set)
        wifi_rows = []
        for wifi_infos, _time in zip(train_data['wifi_infos'], train_data['time_stamp']):
            _time = datetime.strptime(_time, "%Y-%m-%d %H:%M")
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                wifi_and_date[_id].add(str(_time.date()))

        wifi_bssid = set()
        for wifi_infos in train_data['wifi_infos']:
            row = {}
            cur_wifi_len = len(wifi_infos.split(';'))
            for wifi in wifi_infos.split(';'):
                _id, _strong, _connect = wifi.split('|')
                _strong = int(_strong) + 120
                if _id not in row:
                    row[_id] = [_strong, _connect == 'true']
                    wifi_bssid.add(_id)
                else:
                    for i in range(1, cur_wifi_len):
                        _t_id = _id + '_' + str(i)
                        if _t_id in row:
                            row[_t_id] = [_strong, _connect == 'true']
                            wifi_bssid.add(_t_id)
                            break

            wifi_rows.append(row)

        wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
        indptr = [0]
        indices = []
        data = []
        for row in wifi_rows:
            indices.extend([wifi_bssid[i] for i in row.keys()])
            data.extend([t[0] for t in row.values()])
            indptr.append(len(indices))
        return csr_matrix((data, indices, indptr))

    def _fit_transform(self, train_data, mall_id):
        return self._transform(train_data, mall_id)

    def _transform(self, test_data, mall_id):
        wifi_rows = self.__get_wifi_number(test_data)
        simility = cosine_similarity(wifi_rows)

        t = self._mall_center_and_area[self._mall_center_and_area['mall_id'] == mall_id]
        center_lat, center_log = t['center_latitude'].iat[0], t['center_longitude'].iat[0]
        max_area = t['max_area'].iat[0]

        indptr = [0]
        indices = []
        data = []

        lats, logs = test_data['latitude'], test_data['longitude']
        for i, (log, lat) in enumerate(zip(logs, lats)):
            indices.extend([0, 1])

            dis_to_center = get_distance_by_latitude_and_longitude(lat, log, center_lat, center_log)
            if max_area * self.MAX_EXCEED_AREA < dis_to_center:
                dis = sorted([(simility[i][j], j)
                              for j in range(len(test_data)) if i != j], reverse=True)
                found = False
                for d, j in dis:
                    dis_to_center = get_distance_by_latitude_and_longitude(lats.iat[j], logs.iat[j], center_lat,
                                                                           center_log)
                    if max_area * self.MAX_EXCEED_AREA < dis_to_center:
                        data.extend(
                            [lats.iat[j] * self.scale, logs.iat[j] * self.scale])
                        found = True
                        break
                if not found:
                    data.extend([center_lat * self.scale, center_log * self.scale])
            else:
                data.extend([lat * self.scale, log * self.scale])
            indptr.append(len(indices))

        return csr_matrix((data, indices, indptr))


def train_test():
    task = ModelBase()
    task.train_test([LocationToVec2()])
    # task.train_and_on_test_data([LocationToVec2()])


if __name__ == '__main__':
    train_test()
