--- 和hr_train_wifi_count_top join就是取wifi的top 1000，生成hr_train_wifi3_temp表
DROP table if exists hr_train_wifi3_temp;
CREATE TABLE hr_train_wifi3_temp
AS
SELECT a.row_id, a.wifi_bssid, a.strong
FROM hr_train_wifi_temp a
JOIN hr_train_wifi_count_top b
ON a.mall_id = b.mall_id
	AND a.wifi_bssid = b.wifi_bssid;

-- 创建所有的每个row_id对应的wifi
DROP TABLE IF EXISTS hr_train_wifi_row_join;
CREATE TABLE hr_train_wifi_row_join
AS
SELECT a.row_id, b.wifi_bssid, -999 AS strong
FROM hr_train a
JOIN hr_train_wifi_count_top b
ON a.mall_id = b.mall_id;

--- 加入row_id 方便等下判断哪一行不存在
PAI -name AppendId
-project algo_public
-DIDColName="append_id"
-DoutputTableName="hr_train_wifi_row_join_with_append_id"
-DinputTableName="hr_train_wifi_row_join"
-DselectedColNames="row_id,wifi_bssid,strong";


---筛选出存在的append_id
DROP TABLE IF EXISTS hr_train_missing_wifi_temp;
CREATE table hr_train_missing_wifi_temp
AS
SELECT a.append_id
  FROM hr_train_wifi_row_join_with_append_id a
  JOIN hr_train_wifi3_temp b
  ON a.row_id = b.row_id
	  AND a.wifi_bssid = b.wifi_bssid;

-- join 原来的列表 append_id2为空说明不存在
DROP TABLE IF EXISTS hr_train_missing_wifi_temp2;
CREATE TABLE hr_train_missing_wifi_temp2
AS
SELECT a.row_id, a.wifi_bssid, a.strong,a.append_id,b.append_id as append_id2
FROM hr_train_wifi_row_join_with_append_id a
LEFT JOIN hr_train_missing_wifi_temp b
ON a.append_id = b.append_id;

---- 选择append_id2为空的，说明为缺失值
DROP TABLE IF EXISTS hr_train_missing_wifi;
CREATE table hr_train_missing_wifi
AS
SELECT row_id,wifi_bssid,strong
FROM hr_train_missing_wifi_temp2
where append_id2 is null;


---- 合并缺失值和存在的值
DROP TABLE IF EXISTS hr_train_wifi_feature;
CREATE TABLE hr_train_wifi_feature
AS
SELECT CAST(row_id AS STRING) as row_id, wifi_bssid, CAST(strong AS STRING) as strong
FROM hr_train_missing_wifi
UNION
SELECT row_id, wifi_bssid, CAST(strong AS STRING) as strong
FROM hr_train_wifi3_temp;


--连接wifi bssid和strong，方便KV2table
DROP TABLE IF EXISTS hr_train_wifi2;
CREATE TABLE hr_train_wifi2
AS
SELECT row_id
	, concat_ws(';', collect_set(concat(wifi_bssid, ':', strong))) AS wifi
FROM hr_train_wifi_feature
GROUP BY row_id;


-- 创建训练表
DROP TABLE IF EXISTS hr_train3;
CREATE TABLE hr_train3
AS
SELECT a.row_id, a.user_id, a.mall_id, a.shop_id, a.time_stamp
	, a.longitude, a.latitude, b.wifi
FROM hr_train a
JOIN hr_train_wifi2 b
ON a.row_id = b.row_id;
