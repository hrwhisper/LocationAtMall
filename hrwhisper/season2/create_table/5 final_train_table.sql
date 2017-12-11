--连接wifi bssid和strong，方便KV2table
DROP TABLE IF EXISTS hr_train_wifi2;
CREATE TABLE hr_train_wifi2
AS
SELECT a.row_id
	, concat_ws(';', collect_set(concat(a.wifi_bssid, ':', a.strong))) AS wifi
FROM hr_train_wifi_temp a
JOIN hr_train_wifi_count_top b
ON a.mall_id = b.mall_id
	AND a.wifi_bssid = b.wifi_bssid
GROUP BY a.row_id;

-- 创建训练表
DROP TABLE IF EXISTS hr_train3;
CREATE TABLE hr_train3
AS
SELECT a.row_id, a.user_id, a.mall_id, a.shop_id, a.time_stamp
	, a.longitude, a.latitude, b.wifi
FROM hr_train a
JOIN hr_train_wifi2 b
ON a.row_id = b.row_id;