# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    wifi feature analysis
"""
import collections
import time
from sklearn.externals import joblib
from parse_data import read_train_join_mall


def many_mall_has_same_bssid():
    """
    many mall has same bssid, it may be mobile hotspot
    :return:
    """
    train_data = read_train_join_mall()
    counter = collections.defaultdict(set)
    start = time.time()
    for mall_id, wifi_infos in zip(train_data['mall_id'], train_data['wifi_infos']):
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            counter[_id].add(mall_id)
    print(time.time() - start)
    many_uid = {key for key, l in counter.items() if len(l) > 1}
    joblib.dump(many_uid, './feature_save/many_mall_wifi_bssid.pkl')
    print('total: {} repeat in other mall: {}'.format(len(counter), len(many_uid)))


def check_mall(train_data, mall_id='m_6803'):
    """
        交易的条数貌似不是很影响结果
    """
    train_data = train_data[train_data['mall_id'] == mall_id]

    print('---------{}-------'.format(mall_id))
    print('shape: {}'.format(train_data.shape))
    wifi_bssid = set()
    _id_cnt = 0
    strong_cnt = collections.Counter()
    for wifi_infos in train_data['wifi_infos']:
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            wifi_bssid.add(_id)
            strong_cnt[int(_strong)] += 1
            _id_cnt += 1

    with open('./analysis_data/mall_wifi_{}.csv'.format(mall_id), 'w') as f:
        f.write('strong,cnt\n')
        f.writelines(
            '\n'.join('{},{}'.format(strong, cnt) for strong, cnt in sorted(strong_cnt.items(), key=lambda x: x[0])))

    print('number of bssid: {}, cnt: {}'.format(len(wifi_bssid), _id_cnt))
    print()


def check_low():
    """
        mall_id  wifi_loc         wifi
        m_7168 0.708214760008  0.686966420034
        m_7800 0.721053965037  0.690904484419
        m_1920 0.764782750735  0.7520418164
        m_4422 0.767413834659  0.730537478911
        m_2224 0.790900290416  0.773797999355
        m_4079 0.793646944714  0.777400581959
        m_6803 0.825242718447  0.79854368932
        'm_1950': 0.924817798236,  0.909474491753
        m_5076 0.948070175439  0.938713450292
        m_4495 0.972508591065  0.968499427262
    """
    train_data = read_train_join_mall()
    low_list = {
        'm_7168': 0.708214760008,
        'm_7800': 0.721053965037,
        'm_1920': 0.764782750735,
        'm_4422': 0.767413834659,
        'm_2224': 0.790900290416,
        'm_4079': 0.793646944714,
        'm_6803': 0.825242718447,
        'm_1950': 0.924817798236,
        'm_5076': 0.948070175439,
        'm_4495': 0.972508591065
    }
    for mall_id, score in sorted(low_list.items(), key=lambda x: x[1]):
        check_mall(train_data, mall_id)


if __name__ == '__main__':
    # many_mall_has_same_bssid()
    check_low()
