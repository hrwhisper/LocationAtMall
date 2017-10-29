# -*- coding: utf-8 -*-
# @Date    : 2017/10/26
# @Author  : hrwhisper
"""
    1. user 在某个时间段对某类别商店的需求 应该有一定的关系。
"""
import collections
from datetime import datetime

import copy
from scipy.sparse import csr_matrix

from common_helper import ModelBase, XXToVec


class ShopToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/shop_features_{}_{}.pkl')
        self.slot = 1
        self.counter = None

    def _counter_index(self, weekday):
        return 1 if weekday >= 6 else 0

    def _do_transform(self, train_data, counter):
        category_id = {i: _id for i, _id in enumerate(sorted(set(counter[0].keys()) | set(counter[1].keys())))}
        indptr = [0]
        indices = []
        data = []
        for _datetime in map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M"), train_data['time_stamp']):
            indices.extend([i for i in range(len(category_id))])
            for i in range(len(category_id)):
                data.append(counter[self._counter_index(_datetime.isoweekday())][category_id[i]].get(
                    _datetime.hour // self.slot, 0))
            indptr.append(len(indices))
        features = csr_matrix((data, indices, indptr))
        return features

    def _fit_transform(self, train_data, mall_id):
        counter = [collections.defaultdict(dict), collections.defaultdict(dict)]
        for _datetime, category_id in zip(train_data['time_stamp'], train_data['category_id']):
            _datetime = datetime.strptime(_datetime, "%Y-%m-%d %H:%M")
            _date = str(_datetime.date())
            h = _datetime.hour // self.slot
            _cid = self._counter_index(_datetime.isoweekday())  # 周末、平时分开
            if h not in counter[_cid][category_id]:
                counter[_cid][category_id][h] = collections.Counter()
            counter[_cid][category_id][h][_date] += 1

        t = copy.deepcopy(counter)
        for i in range(2):
            for category_id in counter[i].keys():
                for h in range(24 // self.slot):
                    if h not in counter[i][category_id]: continue
                    counter[i][category_id][h] = sum(counter[i][category_id][h].values()) \
                                                 / sum(
                        sum(t[i][c_id][h].values()) if h in t[i][c_id] else 0 for c_id in t[i].keys())
                    # 除以所有类别该时间下的总需求
        self.counter = counter
        features = self._do_transform(train_data, counter)
        return features

    def _transform(self, test_data, mall_id):
        counter = self.counter
        features = self._do_transform(test_data, counter)
        return features


def train_test():
    task = ModelBase()
    task.train_test([ShopToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
