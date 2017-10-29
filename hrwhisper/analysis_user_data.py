# -*- coding: utf-8 -*-
# @Date    : 2017/10/26
# @Author  : hrwhisper
from datetime import datetime
import collections

from parse_data import read_mall_data, read_train_join_mall


def mall_category_time(mall_id='m_7168', _date='2017-08-04'):
    """
    计算某商场某天类别随时间变化
    """
    data = read_train_join_mall()
    data = data[data['mall_id'] == mall_id]
    data = data.sort_values(by='time_stamp')
    first_date = datetime.strptime(_date, "%Y-%m-%d").date()

    counter = collections.defaultdict(lambda: [0] * 24)
    for _datetime, category_id in zip(data['time_stamp'], data['category_id']):
        _datetime = datetime.strptime(_datetime, "%Y-%m-%d %H:%M")
        if _datetime.date() != first_date: continue
        counter[category_id][_datetime.hour] += 1

    with open('./analysis_data/mall_counter_{}.csv'.format(_date), 'w') as f:
        f.write(',{}\n'.format(','.join([str(i) for i in range(24)])))
        for category_id, cnt in sorted(counter.items()):
            f.write('{},{}\n'.format(category_id, ','.join([str(c) for c in cnt])))


if __name__ == '__main__':
    mall_category_time()
