from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from datetime import date
from common_helper import ModelBase, XXToVec
import numpy as np
import pandas as pd
import datetime
class TimeToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/time_features_{}_{}.pkl', './feature_save/time_features_{}_{}.pkl')

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
            train_data['day_of_week']=train_data['time_stamp'].astype('str').apply(lambda x:date(int(x[0:4]),int(x[5:7]),int(x[8:10])).weekday()+1)
            #train_data['hour']=train_data['time_stamp'].astype('str').apply(lambda x:int(x[11:13]))
            #train_data['minute']=train_data['time_stamp'].astype('str').apply(lambda x:int(x[14:16]))
            train_data['is_weekend']=train_data['day_of_week'].apply(lambda x:1 if x in (6,7) else 0)
            train_data=pd.concat([train_data['is_weekend'],train_data['day_of_week'],train_data['longitude'],train_data['latitude']],axis=1)
            features = csr_matrix(train_data)
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('train', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data_time_stamp = []
            test_dat_day_of_week = []
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            for time_stamp in test_data['time_stamp']:
                time_stamp = time_stamp.split(' ')
                time_stamp = time_stamp[0]
                year,month,day = time_stamp.split('/')
                dt_obj = datetime.datetime(int(year), int(month), int(day))
                day_of_week = date(int(year), int(month), int(day)).weekday() + 1
                test_data_time_stamp.append(dt_obj.strftime("%Y-%m-%d"))
                test_dat_day_of_week.append(day_of_week)
            test_data['day_of_week'] = test_dat_day_of_week
            print (test_data['day_of_week'])
            #test_data['day_of_week']=test_data['time_stamp'].astype('str').apply(lambda x:date(int(x[0:4]),int(x[5:7]),int(x[8:10])).weekday()+1)
            #test_data['hour']=test_data['time_stamp'].astype('str').apply(lambda x:int(x[11:13]))
            #test_data['minute']=test_data['time_stamp'].astype('str').apply(lambda x:int(x[14:16]))
            test_data['is_weekend']=test_data['day_of_week'].apply(lambda x:1 if x in (6,7) else 0)
            test_data=pd.concat([test_data['is_weekend'],test_data['day_of_week'],test_data['longitude'],test_data['latitude']],axis=1)
            features = csr_matrix(test_data)
            if should_save:
                joblib.dump(features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return features


class UseTime(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=100, random_state=self._random_state),
        }


def train_test():
    task = UseTime()
    task.train_test([TimeToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
