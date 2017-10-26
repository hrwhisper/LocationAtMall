# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    使用了wifi特征，类似BOW (本地：0.8942214814065961    提交：0.8951)
    update: 同一个用户可能检测多个bssid，取最高 (本地：0.8943369306918623    提交：0.8954)
"""

from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from common_helper import ModelBase, XXToVec


class WifiToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl', './feature_save/wifi_bssid_{}_{}.pkl')
        self.min_strong = -300

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
            wifi_bssid = set()
            wifi_rows = []
            # 去除同一条记录中多个bssid
            for wifi_infos in train_data['wifi_infos']:
                row = {}
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    _strong = int(_strong) - self.min_strong
                    if _id not in row:
                        row[_id] = [_strong, _connect == 'true']
                    else:
                        row[_id] = [max(row[_id][0], _strong), _connect == 'true' or row[_id][0]]
                    wifi_bssid.add(_id)
                wifi_rows.append(row)

            wifi_bssid = {_id: i for i, _id in enumerate(sorted(wifi_bssid))}
            indptr = [0]
            indices = []
            data = []
            for row in wifi_rows:
                for _id, (_strong, _connect) in row.items():
                    _id = wifi_bssid[_id]
                    indices.append(_id)
                    data.append(_strong)
                indptr.append(len(indices))

            wifi_features = csr_matrix((data, indices, indptr))  # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))
            joblib.dump(wifi_bssid, self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            wifi_bssid = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            wifi_rows = []
            not_in = set()
            for wifi_infos in test_data['wifi_infos']:
                row = {}
                for wifi in wifi_infos.split(';'):
                    _id, _strong, _connect = wifi.split('|')
                    if _id not in wifi_bssid:
                        not_in.add(_id)
                        continue
                    _strong = int(_strong) - self.min_strong
                    if _id not in row:
                        row[_id] = [_strong, _connect == 'true']
                    else:
                        row[_id] = [max(row[_id][0], _strong), _connect == 'true' or row[_id][0]]
                wifi_rows.append(row)

            indptr = [0]
            indices = []
            data = []
            for row in wifi_rows:
                for _id, (_strong, _connect) in row.items():
                    _id = wifi_bssid[_id]
                    indices.append(_id)
                    data.append(_strong)
                indptr.append(len(indices))

            print('total: {} ,not_in :{}'.format(len(wifi_bssid), len(not_in)))
            wifi_features = csr_matrix((data, indices, indptr), shape=(len(test_data), len(wifi_bssid)))
            # TODO normalize
            if should_save:
                joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('test', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('test', mall_id))
        return wifi_features


class UseWifi(ModelBase):
    def __init__(self):
        super().__init__()

    def _get_classifiers(self):
        return {
            'random forest': RandomForestClassifier(n_jobs=4, n_estimators=100, random_state=self._random_state),
        }


def train_test():
    task = UseWifi()
    task.train_test([WifiToVec()])
    # task.train_and_on_test_data([WifiToVec()])


if __name__ == '__main__':
    train_test()
