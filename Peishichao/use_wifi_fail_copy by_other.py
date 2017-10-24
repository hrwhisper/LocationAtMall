# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    使用了wifi特征，类似BOW (本地：0.8942214814065961    提交：0.8951)
    update: 同一个用户可能检测多个bssid，取最高 (本地：0.8943369306918623    提交：0.8954)
"""
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from common_helper import ModelBase, XXToVec
import numpy as np
import pandas as pd

class WifiToVec(XXToVec):
    def __init__(self):
        super().__init__('./feature_save/wifi_features_{}_{}.pkl', './feature_save/wifi_bssid_{}_{}.pkl')
        self.min_strong = -300

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
            wifis = []
            wifiSet = set()
            for wifiInfo in train_data['wifi_infos']:
                wifi = wifiInfo.split(';')
                splitedEachWifi = []
                for w in wifi:
                    sew = w.split('|')
                    splitedEachWifi.append(sew)
                    # 检测到信号的wifi手动增加100dB能量
                    sew[1] = 10.0 ** ((np.int(sew[1]) + 90) / 10.0)
                    wifiSet.add(sew[0])
                splitedEachWifi = np.array(splitedEachWifi)
                wifis.append(splitedEachWifi)
            fixedWifiSet = sorted(wifiSet)
            fixedWifiDict = {}
            cnt = 0
            for fws in fixedWifiSet:
                fixedWifiDict[fws] = cnt
                cnt += 1
            wifiMat = []
            for wifi in wifis:
                wifiVec = np.zeros(len(fixedWifiSet)).astype('int32')
                for w in wifi:
                    wifiVec[fixedWifiDict[w[0]]] = np.float(w[1])
                wifiMat.append(wifiVec)
            wifiMat = np.array(wifiMat)
            wifiss = StandardScaler()
            wifiMat = wifiss.fit_transform(wifiMat)
            wifiData = pd.DataFrame()
            for wifiCol in range(wifiMat.shape[1]):
                 wifiData[fixedWifiSet[wifiCol]] = wifiMat[:, wifiCol]

            wifi_features = pd.concat([wifiData],axis=1)
            wifi_features  = csr_matrix(wifi_features)
            if should_save:
                 joblib.dump(wifi_features, self.FEATURE_SAVE_PATH.format('train', mall_id))

            joblib.dump(wifiMat, self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
        else:
            wifi_features = joblib.load(self.FEATURE_SAVE_PATH.format('train', mall_id))
        return wifi_features

    def test_data_to_vec(self, test_data, mall_id, renew=True, should_save=False):
        if renew:
            wifiMat_ = joblib.load(self.HOW_TO_VEC_SAVE_PATH.format('train', mall_id))
            test_data = test_data.loc[test_data['mall_id'] == mall_id]
            wifis = []
            wifiSet = set()
            for wifiInfo in test_data['wifi_infos']:
                wifi = wifiInfo.split(';')
                splitedEachWifi = []
                for w in wifi:
                    sew = w.split('|')
                    splitedEachWifi.append(sew)
                    # 检测到信号的wifi手动增加100dB能量
                    sew[1] = 10.0 ** ((np.int(sew[1]) + 90) / 10.0)
                    wifiSet.add(sew[0])
                splitedEachWifi = np.array(splitedEachWifi)
                wifis.append(splitedEachWifi)
            fixedWifiSet = sorted(wifiSet)
            fixedWifiDict = {}
            cnt = 0
            for fws in fixedWifiSet:
                fixedWifiDict[fws] = cnt
                cnt += 1
            wifiMat = []
            for wifi in wifis:
                wifiVec = np.zeros(len(fixedWifiSet)).astype('int32')
                for w in wifi:
                    wifiVec[fixedWifiDict[w[0]]] = np.float(w[1])
                wifiMat.append(wifiVec)
            wifiMat = np.array(wifiMat)
            wifiss = StandardScaler()
            wifiMat = wifiss.fit_transform(wifiMat)
            wifiData = pd.DataFrame()
            for wifiCol in range(wifiMat_.shape[1]):
                 if wifiCol in fixedWifiSet:
                     wifiData[fixedWifiSet[wifiCol]] = wifiMat[:, wifiCol]
                 else:
                     wifiData[wifiCol] = wifiMat[:,wifiMat.shape[1]-1]
            wifi_features = pd.concat([wifiData],axis=1)
            wifi_features  = csr_matrix(wifi_features)
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
