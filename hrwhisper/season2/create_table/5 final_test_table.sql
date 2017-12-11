--连接wifi bssid和strong，方便KV2table
DROP TABLE IF EXISTS hr_test_wifi2;
CREATE TABLE hr_test_wifi2
AS
SELECT row_id
	, concat_ws(';', collect_set(concat(wifi_bssid, ':', strong))) AS wifi
FROM hr_test_wifi_temp3
GROUP BY row_id;

-- 创建测试表
DROP TABLE IF EXISTS hr_test3;
CREATE TABLE hr_test3
AS
SELECT a.row_id, a.user_id, a.mall_id, a.time_stamp, a.longitude
	, a.latitude, b.wifi
FROM hr_test a
JOIN hr_test_wifi2 b
ON a.row_id = b.row_id;