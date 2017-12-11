--创建临时表，替换null,负值变正
DROP TABLE IF EXISTS hr_test_wifi_temp;
CREATE TABLE hr_test_wifi_temp
AS
SELECT row_id, mall_id,  wifi_bssid
	, CASE
		WHEN strong = 'null' THEN 20
		ELSE strong + 120
	END as strong
FROM hr_test_wifi;