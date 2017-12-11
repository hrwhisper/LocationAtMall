# -*- coding: utf-8 -*-
# @Date    : 2017/12/4
# @Author  : hrwhisper
from math import ceil


def main():
    with open('./mall_id') as f:
        mall_ids = f.read().splitlines()

    split_num = 5
    each_num = ceil(len(mall_ids) / split_num)
    for i in range(split_num):
        print(i * each_num, (i + 1) * each_num)
        # print(mall_ids[i * each_num:(i + 1) * each_num])
        if i == 0:
            res = ["DROP TABLE IF EXISTS hr_result_rf400_sqrt;",
                   "create table hr_result_rf400_sqrt(row_id string, shop_id string);"]
        else:
            res = []
        for mall_id in mall_ids[i * each_num:(i + 1) * each_num]:
            res.append("INSERT INTO hr_result_rf400_sqrt select row_id, shop_id from {}_result_400_sqrt;".format(mall_id))

        with open('./sql/generate_result_{}.sql'.format(i), 'w') as f:
            f.writelines('\n'.join(res))

            #     res.append("""
            # SELECT count(*) FROM hr_result_rf400_sqrt;
            # DROP TABLE IF EXISTS ant_tianchi_ccf_sl_predict;
            # CREATE TABLE ant_tianchi_ccf_sl_predict AS SELECT * FROM hr_result_rf400;""")


if __name__ == '__main__':
    main()
