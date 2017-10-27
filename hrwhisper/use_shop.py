# -*- coding: utf-8 -*-
# @Date    : 2017/10/26
# @Author  : hrwhisper
"""
    1. user 在某个时间段对某类别商店的需求 应该有一定的关系。
"""
import collections
from datetime import datetime

from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from common_helper import ModelBase, XXToVec
from use_location3 import LocationToVec3
from use_time import TimeToVec
from use_wifi3 import WifiToVec3


class ShopToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/shop_features_{}_{}.pkl', './feature_save/shop_features_how_to_{}.pkl')
        self.slot = 1

    def _shop_to_vec(self, train_data, counter):
        category_id = {i: _id for i, _id in enumerate(sorted(counter.keys()))}
        indptr = [0]
        indices = []
        data = []
        for _datetime in map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M"), train_data['time_stamp']):
            indices.extend([i for i in range(len(category_id))])
            for i in range(len(category_id)):
                data.append(counter[category_id[i]].get(_datetime.hour // self.slot, 0))
            indptr.append(len(indices))
        features = csr_matrix((data, indices, indptr))
        return features

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
            # TODO 周末分开

            counter = collections.defaultdict(dict)
            for _datetime, category_id in zip(train_data['time_stamp'], train_data['category_id']):
                _datetime = datetime.strptime(_datetime, "%Y-%m-%d %H:%M")
                _date = str(_datetime.date())
                h = _datetime.hour // self.slot
                if h not in counter[category_id]:
                    counter[category_id][h] = collections.Counter()
                counter[category_id][h][_date] += 1

            for category_id in counter.keys():
                for h in range(24 // self.slot):
                    if h not in counter[category_id]: continue
                    counter[category_id][h] = sum(counter[category_id][h].values()) # / len(counter[category_id][h])

            features = self._shop_to_vec(train_data, counter)

            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(counter, self.HOW_TO_VEC_SAVE_PATH.format(mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            counter = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format(mall_id))

            features = self._shop_to_vec(test_data, counter)

            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return features


class UseShop(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=3, n_estimators=200, random_state=self._random_state,
                                                    class_weight='balanced'),
        }


def train_test():
    task = UseShop()
    task.train_test([LocationToVec3(), WifiToVec3(), TimeToVec(), ShopToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
