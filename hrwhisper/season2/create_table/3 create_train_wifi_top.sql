--创建临时表，替换null,负值变正
DROP TABLE IF EXISTS hr_train_wifi_temp;
CREATE TABLE hr_train_wifi_temp
AS
SELECT row_id, mall_id, wifi_bssid
	, CASE
		WHEN strong = 'null' THEN 20
		ELSE strong + 120
	END as strong
FROM hr_train_wifi;

-- wifi计数
DROP TABLE IF EXISTS hr_train_wifi_count;
CREATE TABLE hr_train_wifi_count
AS
SELECT mall_id, wifi_bssid, COUNT(wifi_bssid) as wifi_count
	FROM hr_train_wifi_temp
	GROUP BY mall_id, wifi_bssid;

-- 分mall各个mall的wifi取top 1000
        DROP TABLE IF EXISTS hr_train_wifi_count_top;
        CREATE TABLE hr_train_wifi_count_top(
            mall_id STRING,
            wifi_bssid STRING ,
            wifi_count BIGINT
        );

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1010'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1043'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1071'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1080'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1081'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1082'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1111'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1115'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1164'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1176'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1263'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1291'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1293'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1309'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1366'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1402'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1413'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1442'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1451'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1621'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1657'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1755'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1789'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1807'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1893'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1910'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1913'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1919'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1920'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1928'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1936'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1960'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1962'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1990'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2011'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2030'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2092'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2093'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2097'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2108'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2267'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2270'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2324'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2333'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2334'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2419'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2571'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2715'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3034'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3054'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3092'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3112'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3120'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3197'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3219'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3232'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3268'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3319'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3414'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3434'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3520'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3596'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3601'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3610'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3620'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3695'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3702'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3709'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3732'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3795'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3869'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3916'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3936'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4005'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4064'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4066'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4068'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4098'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4173'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4178'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4181'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4199'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4211'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4216'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4227'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4244'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4312'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4357'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4372'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4384'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4406'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4434'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4548'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4634'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4664'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4680'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4711'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4889'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4983'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4998'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5024'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5076'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5192'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5291'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5337'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5343'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5364'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5369'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5452'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5609'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5641'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5654'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5661'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5772'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5783'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5833'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5845'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5847'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6065'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_613'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_614'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6141'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_623'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_627'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_628'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_629'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_640'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6538'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6596'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6638'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6703'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6714'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6803'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_699'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7225'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7255'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7256'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7283'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7323'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7329'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7346'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7374'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7375'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7501'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7601'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7671'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_768'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7697'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7724'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7778'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7781'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7791'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7792'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7800'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7832'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7833'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7870'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7942'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7953'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7973'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7976'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7994'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8015'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_822'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8222'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_826'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_828'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8327'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8344'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8494'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8550'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8563'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8671'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8960'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8991'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_9047'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_9054'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_919'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1006'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1052'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1057'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1089'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1106'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1175'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1375'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1377'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1381'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1485'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1790'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1791'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1905'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1906'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1968'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1993'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1997'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2005'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2021'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2087'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2123'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2156'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2177'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2182'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2218'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2224'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2257'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2299'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2361'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2369'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2395'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2404'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2413'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2414'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2415'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2431'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2467'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2476'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2578'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2864'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2892'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2907'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3001'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3117'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3143'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3231'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3281'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3425'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3442'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3445'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3467'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3501'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3511'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3591'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3605'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3627'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3730'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3753'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3822'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3832'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3847'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3871'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3882'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3938'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4011'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4033'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4036'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4058'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4079'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4094'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4099'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4121'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4132'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4139'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4157'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4162'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4187'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4224'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4253'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4341'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4358'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4380'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4505'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4515'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4524'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4525'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4585'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4695'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4818'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5014'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5182'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5200'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5214'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5296'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5311'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5319'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5323'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5325'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5326'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5352'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5363'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5382'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5413'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5443'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5446'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5471'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5487'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5516'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5527'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5570'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5600'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5677'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5810'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5825'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5892'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5958'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_615'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_616'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6167'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_617'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_618'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_619'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_625'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_626'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6337'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_648'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6480'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6511'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6516'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6580'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6587'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6590'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6630'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6720'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_689'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6923'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7039'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7168'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7304'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7383'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7410'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7523'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_755'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_760'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7811'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7821'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7867'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7868'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7899'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7997'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7998'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_800'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_802'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8041'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8188'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8200'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8215'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8251'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8282'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8285'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8452'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8974'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8980'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_9051'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_9068'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_911'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_912'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_957'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_976'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_979'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_988'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1021'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1085'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1128'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1129'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1161'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1320'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1389'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1409'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1435'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1553'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1585'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1701'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1943'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_1950'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2009'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2058'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2060'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2230'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2307'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2450'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2514'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2539'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_2878'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3005'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3010'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3019'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3027'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3031'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3313'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3329'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3449'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3517'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3528'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3532'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3534'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3540'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3679'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3690'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3739'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3804'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3839'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3897'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_3899'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4049'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4112'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4160'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4168'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4205'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4206'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4221'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4269'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4347'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4422'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4423'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4459'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4466'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4509'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4543'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4572'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4599'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4637'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4759'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4801'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4834'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4853'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_4923'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5019'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5081'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5085'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5154'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5258'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5331'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5349'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5374'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5424'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5435'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5450'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5473'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5481'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5503'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5519'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5529'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5542'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5583'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5586'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5751'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5752'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5767'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5778'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5785'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5812'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5813'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_5946'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_621'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_622'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6390'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6428'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6429'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_651'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6526'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_6527'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_672'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_690'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7199'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7516'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7520'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7544'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7616'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7701'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7746'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7796'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_786'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7939'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_7954'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_796'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8052'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8063'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8093'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8157'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8275'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8414'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8429'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8430'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_867'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8688'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8835'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8853'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8893'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8907'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8908'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_8910'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_9007'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_909'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_927'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_954'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_966'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_968'
                ORDER BY wifi_count DESC limit 1000;

        INSERT INTO hr_train_wifi_count_top
            SELECT mall_id, wifi_bssid, wifi_count
                FROM hr_train_wifi_count WHERE mall_id = 'm_989'
                ORDER BY wifi_count DESC limit 1000;
