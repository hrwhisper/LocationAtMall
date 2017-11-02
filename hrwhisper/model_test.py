# -*- coding: utf-8 -*-
# @Date    : 2017/10/29
# @Author  : hrwhisper
import os

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from common_helper import ModelBase
from use_category import CategoryToVec
from use_location import LocationToVec
from use_location2 import LocationToVec2
from use_price import PriceToVec
from use_strong_wifi import WifiStrongToVec
from use_time import TimeToVec
from use_wifi import WifiToVec
from use_wifi_kstrong import WifiKStrongToVec


class UseTime(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        """
        :return: dict. {name:classifier}
        """
        return {
            'random forest': RandomForestClassifier(n_jobs=os.cpu_count() // 2, n_estimators=400,
                                                    random_state=self._random_state, class_weight='balanced'),
        }


def train_test():
    task = UseTime()
    task.train_test([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])
    task.train_and_on_test_data([LocationToVec2(), WifiToVec(), WifiStrongToVec(), WifiKStrongToVec(), PriceToVec()])


if __name__ == '__main__':
    train_test()
