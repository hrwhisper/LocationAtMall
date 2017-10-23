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
        m_6803 0.524705882353
        m_7168 0.686923385479
        m_7800 0.690965092402
        m_4422 0.730686950321
        m_1920 0.730686950321
        m_2224 0.777814029364
        m_4079 0.783164624401
        m_6167 0.792156862745
        m_7374 899690676094
        m_4572 0.923987255348
    """
    train_data = read_train_join_mall()
    low_list = ['m_6803', 'm_7168', 'm_7800', 'm_4422', 'm_1920', 'm_2224', 'm_4079', 'm_6167', 'm_7374', 'm_4572']
    for mall_id in low_list:
        check_mall(train_data, mall_id)


if __name__ == '__main__':
    # many_mall_has_same_bssid()
    check_low()
