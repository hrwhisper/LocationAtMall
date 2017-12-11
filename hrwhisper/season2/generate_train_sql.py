# -*- coding: utf-8 -*-
# @Date    : 2017/12/4
# @Author  : hrwhisper
"""
    生成各个mall的训练代码, 调用PAI的一些模型。
"""
from math import ceil


class SqlGenerator(object):
    def __init__(self, mall_id):
        self.mall_id = mall_id
        self.train_bool_to_str = {
            True: 'train',
            False: 'test'
        }

    def _create_mall_table(self, is_train):
        new_table_name = 'temp_{}_hr_{}'.format(self.mall_id, self.train_bool_to_str[is_train])
        from_table_name = 'hr_{}3'.format(self.train_bool_to_str[is_train])
        mall_id = self.mall_id
        return """
DROP TABLE IF EXISTS {new_table_name};
CREATE TABLE {new_table_name} AS SELECT * FROM {from_table_name} WHERE mall_id = '{mall_id}'; \n""".format(**locals())

    def _wifi_table_to_vec(self, is_train):
        input_table = 'temp_{}_hr_{}'.format(self.mall_id, self.train_bool_to_str[is_train])
        mall_id = self.mall_id
        out_table = 'temp_{}_wifi_table_{}_vec'.format(mall_id, self.train_bool_to_str[is_train])
        out_map = 'temp_{}_wifi_table_{}_map_vec'.format(mall_id, self.train_bool_to_str[is_train])
        append_name = 'row_id,longitude,latitude' + (',shop_id' if is_train else '')

        res = """
DROP TABLE IF EXISTS {out_table};
DROP TABLE IF EXISTS {out_map};
PAI -name KVToTable 
    -project algo_public 
    -Dlifecycle="28"
    -DappendColName="{append_name}" 
    -DoutputTableName="{out_table}" 
    -DkvColName="wifi" 
    -DoutputKeyMapTableName="{out_map}" 
    -DkvDelimiter=":" 
    -Dtop1200="true" 
    -DitemDelimiter=";" 
    -DinputTableName="{input_table}" """.format(**locals())
        if is_train:
            res += ";"
        else:
            res += '\n    -DinputKeyMapTableName="temp_{}_wifi_table_train_map_vec";'.format(mall_id)
        return res + '\n'

    def train(self):
        mall_id = self.mall_id
        table_name = 'temp_{}_wifi_table_train_vec'.format(mall_id)
        return """
-- DROP OFFLINEMODEL IF EXISTS hr_random_forests_{mall_id}_400_sqrt;
PAI -name randomforests 
    -project algo_public 
    -DlabelColName="shop_id" 
    -DminNumPer="0" 
    -DtreeNum="400" 
    -DrandomColNum="30"
    -DmodelName="hr_random_forests_{mall_id}_400_sqrt" 
    -DexcludedColNames="row_id"
    -DminNumObj="2" 
    -DmaxRecordSize="100000" 
    -DinputTableName="{table_name}";
        """.format(**locals())

    def predict(self):
        mall_id = self.mall_id
        table_name = 'temp_{}_wifi_table_test_vec'.format(mall_id)
        return """
-- DROP TABLE IF EXISTS {mall_id}_result_400_sqrt;
PAI -name prediction 
    -project algo_public 
    -Dlifecycle="28" 
    -DmodelName="hr_random_forests_{mall_id}_400_sqrt"
    -DscoreColName="prediction_score" 
    -DenableSparse="false" 
    -DoutputTableName="{mall_id}_result_400_sqrt" 
    -DdetailColName="prediction_detail" 
    -DkvDelimiter=":" 
    -DresultColName="shop_id" 
    -DitemDelimiter="," 
    -DinputTableName="{table_name}" 
    -DappendColNames="row_id";""".format(**locals())

    def run(self):
        res = [
            '-------------------------- {} begin --------------------------'.format(self.mall_id),
            self._create_mall_table(is_train=True),
            self._create_mall_table(is_train=False),

            self._wifi_table_to_vec(is_train=True),
            self._wifi_table_to_vec(is_train=False),

            self.train(),
            self.predict(),
            '\n-------------------------- {} end--------------------------\n\n\n\n'.format(self.mall_id),
        ]
        return res


def main():
    with open('./mall_id') as f:
        mall_ids = f.read().splitlines()

    split_num = 5
    each_num = ceil(len(mall_ids) / split_num)
    for i in range(split_num):
        print(i * each_num, (i + 1) * each_num)
        print(mall_ids[i * each_num:(i + 1) * each_num])
        res = []
        for mall_id in mall_ids[i * each_num:(i + 1) * each_num]:
            res.extend(SqlGenerator(mall_id).run())
        with open('./sql/train_and_predict_{}.sql'.format(i), 'w') as f:
            f.writelines(res)


if __name__ == '__main__':
    main()
