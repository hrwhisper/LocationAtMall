# -*- coding: utf-8 -*-
# @Date    : 2017/10/25
# @Author  : hrwhisper


import numpy as np
from scipy.sparse import csr_matrix
from datetime import datetime
from common_helper import ModelBase, XXToVec


"""
LocationToVec(), WifiToVec3(), TimeToVec()
RandomForestClassifier(class_weight='balanced',n_estimators=400, n_jobs=4,
              random_state=42) Mean: 0.909196793335719
            
RandomForestClassifier(class_weight='balanced',n_estimators=200, n_jobs=4,
              random_state=42) Mean: 0.9086988576400435
"""


class TimeToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/time_features_{}_{}.pkl')

    @staticmethod
    def _do_transform(train_data):
        features = np.array([
            np.array([_time.isoweekday(),
                      _time.isoweekday() >= 6,  # Mean: 0.9109541149905104 0.9076093830826543
                      # _time.hour // 6,  # 0.9110178129353056 0.907882340
                      # _time.hour // 5,  # 0.9070676933021364 0.9077367366607973
                      # _time.hour, #  0.9105093297197597  0.9070204350804165 0.9070565010851597(time//5)
                      ])
            for _time in map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M"), train_data['time_stamp'].astype('str'))])
        return csr_matrix(np.hstack([features, train_data[['longitude', 'latitude']]]))

    def _fit_transform(self, train_data, mall_id):
        return self._do_transform(train_data)

    def _transform(self, data, mall_id):
        return self._do_transform(data)


def train_test():
    task = ModelBase()
    task.train_test([TimeToVec()])
    # task.train_and_on_test_data([LocationToVec(), WifiToVec(), TimeToVec()])


if __name__ == '__main__':
    train_test()
    # 2017-08-06 21:20
    # _time = datetime.strptime('2017-08-06 21:20', "%Y-%m-%d %H:%M")
    # print(_time.hour)
    # print(_time.weekday() >= 5)
    # print(type(_time.isoweekday()))
