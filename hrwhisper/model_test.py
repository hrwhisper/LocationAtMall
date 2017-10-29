# -*- coding: utf-8 -*-
# @Date    : 2017/10/29
# @Author  : hrwhisper
import os

from sklearn.ensemble import RandomForestClassifier

from common_helper import ModelBase
from use_location import LocationToVec
from use_time import TimeToVec
from use_wifi import WifiToVec


class UseTime(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=os.cpu_count() // 2, n_estimators=200,
                                                    random_state=self._random_state, class_weight='balanced'),
        }


def train_test():
    task = UseTime()
    task.train_test([LocationToVec(), WifiToVec(), TimeToVec()])
    # task.train_and_on_test_data([LocationToVec(), WifiToVec(), TimeToVec()])


if __name__ == '__main__':
    train_test()
