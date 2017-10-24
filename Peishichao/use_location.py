# -*- coding: utf-8 -*-
# @Date    : 2017/10/23
# @Author  : hrwhisper
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from common_helper import ModelBase, XXToVec
from use_wifi import WifiToVec
from use_time import TimeToVec
import geohash

class LocationToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/location_features_{}_{}.pkl', './feature_save/location_features_{}_{}.pkl')
    
    def encode_geohash(self,x,y):
        return geohash.encode(x,y)
    def decode_geohash(self,x):
        return list(geohash.decode_exactly(x))
    def train_data_to_vec(self, train_data, mall_id, renew=True, should_save=False):
        """
        :param data: pandas. train_data.join(mall_data.set_index('shop_id'), on='shop_id', rsuffix='_mall')
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
            for log, lat in zip(train_data['longitude'], train_data['latitude']):
                #indices.extend([0, 1, 2, 3])
                indices.extend([0, 1])
                #temp_geohash = self.encode_geohash(log,lat)
                #temp_geohash_list = self.decode_geohash(temp_geohash)
                #data.extend(temp_geohash_list)
                data.extend([log, lat])
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
            for log, lat in zip(test_data['longitude'], test_data['latitude']):
                #indices.extend([0, 1, 2, 3])
                indices.extend([0, 1])
                #temp_geohash = self.encode_geohash(log,lat)
                #temp_geohash_list = self.decode_geohash(temp_geohash)
                #data.extend(temp_geohash_list)
                data.extend([log, lat])
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
            'random forest': RandomForestClassifier(n_jobs=3, n_estimators=200, random_state=self._random_state,class_weight='balanced'),
        }


def train_test():
    task = UseLoc()
    #task.train_test([LocationToVec(),WifiToVec(),TimeToVec()])
    task.train_and_on_test_data([LocationToVec(),WifiToVec(),TimeToVec()])


if __name__ == '__main__':
    train_test()
