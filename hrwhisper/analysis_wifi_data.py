# -*- coding: utf-8 -*-
# @Date    : 2017/10/21
# @Author  : hrwhisper
"""
    wifi feature analysis
"""
import collections
import time
from datetime import datetime

from sklearn.externals import joblib

from parse_data import read_train_join_mall, read_test_data
from visulization_wifi_data import draw_wifi


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
        能收到的wifi条数也不是很影响结果的样子
    """
    train_data = train_data[train_data['mall_id'] == mall_id]

    print('---------{}-------'.format(mall_id))
    print('shape: {}'.format(train_data.shape))
    wifi_bssid = set()
    _id_cnt = 0
    strong_cnt = collections.Counter()
    receive_cnt = []
    for wifi_infos in train_data['wifi_infos']:
        receive_cnt.append(len(wifi_infos.split(';')))
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            wifi_bssid.add(_id)
            strong_cnt[int(_strong)] += 1
            _id_cnt += 1

    with open('./analysis_data/mall_wifi_{}.csv'.format(mall_id), 'w') as f:
        f.write('strong,cnt\n')
        f.writelines(
            '\n'.join('{},{}'.format(strong, cnt) for strong, cnt in sorted(strong_cnt.items(), key=lambda x: x[0])))

    print('number of bssid: {}, cnt: {}, mean receive:{}'.format(len(wifi_bssid), _id_cnt,
                                                                 sum(receive_cnt) / len(receive_cnt)))
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


def _wifi_co_occurrence(train_data, mall_id='m_7168'):
    train_data = train_data.loc[train_data['mall_id'] == mall_id]
    wifi_and_date = collections.defaultdict(set)
    for wifi_infos, _time in zip(train_data['wifi_infos'], train_data['time_stamp']):
        _time = datetime.strptime(_time, "%Y-%m-%d %H:%M")
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            wifi_and_date[_id].add(str(_time.date()))

    wifi_association = collections.defaultdict(set)
    for wifi_infos in train_data['wifi_infos'].values:
        wifi_ids = set()
        for wifi in wifi_infos.split(';'):
            _id, _strong, _connect = wifi.split('|')
            if len(wifi_and_date[_id]) < 5:
                continue
            wifi_ids.add(_id)

        wifi_ids = list(wifi_ids)

        for i in range(len(wifi_ids)):
            for j in range(i + 1, len(wifi_ids)):
                wifi_association[wifi_ids[i]].add(wifi_ids[j])
                wifi_association[wifi_ids[j]].add(wifi_ids[i])

    draw_wifi(wifi_association, mall_id)
    res = []
    total = len(wifi_association)
    print(total)
    for _id, l in wifi_association.items():
        # print(_id, len(l))
        if len(l) > total // 4:
            res.append([mall_id, _id])
    return res


def wifi_co_occurrence_analysis():
    train_data = read_train_join_mall()
    res = []
    for mall_id in train_data['mall_id'].unique():
        res.extend(_wifi_co_occurrence(train_data, mall_id))
    with open('./feature_save/wifi_co_occurrence.csv', 'w') as f:
        f.write('mall_id,bssid\n')
        for mall_id, bssid in res:
            f.write('{},{}\n'.format(mall_id, bssid))


def wifi_empty_statics():
    """
    Wifi那一栏没有为空的
    """
    train_data = read_test_data()  # read_train_join_mall()
    counter = collections.Counter()
    for mall_id in train_data['mall_id'].unique():
        data = train_data[train_data['mall_id'] == mall_id]
        for wifi_infos in data['wifi_infos']:
            cur_wifi_len = len(wifi_infos.split(';'))
            if cur_wifi_len == 0:
                counter[mall_id] += 1

    for mall_id, cnt in counter.items():
        print(mall_id, cnt)


def wifi_apperance_days(mall_id='m_1621'):
    import pandas as pd
    import numpy as np
    _train_data = read_train_join_mall()
    train_data = _train_data.loc[_train_data['mall_id'] == mall_id]
    train_data = train_data.assign(time_stamp=pd.to_datetime(train_data['time_stamp']))
    train_data['time_stamp'] = train_data['time_stamp'].dt.day
    total_count = [collections.defaultdict(set) for _ in range(31)]
    bssids = set()
    for shop_id, day, wifi_infos in zip(train_data['shop_id'], train_data['time_stamp'], train_data['wifi_infos']):
        for wifi_info in wifi_infos.split(';'):
            bssid, _, _ = wifi_info.split('|')
            bssids.add(bssid)
            total_count[day - 1][bssid].add(shop_id)

    cnt = 0
    for bssid in sorted(bssids):
        t = np.array([len(total_count[i][bssid]) for i in range(31)])
        if np.count_nonzero(t) > 7:
            print(t)
            cnt += 1
    print(cnt, len(bssids))


if __name__ == '__main__':
    many_mall_has_same_bssid()
    check_low()
    wifi_co_occurrence_analysis()
    _wifi_co_occurrence(read_train_join_mall())
    wifi_empty_statics()
    wifi_apperance_days()
