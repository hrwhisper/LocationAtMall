-- DROP TABLE hr_train;
CREATE TABLE hr_train
AS
SELECT ROW_NUMBER() OVER (ORDER BY time_stamp) AS row_id, user_id, User.longitude, User.latitude, User.time_stamp
	, Mall.longitude AS longitude_mall, Mall.latitude AS latitude_mall, Mall.shop_id, Mall.mall_id
	, split_part(split_part(wifi_infos, ';', 1), '|', 1) AS wifi1
	, split_part(split_part(wifi_infos, ';', 1), '|', 2) AS wifi1_strong
	, split_part(split_part(wifi_infos, ';', 2), '|', 1) AS wifi2
	, split_part(split_part(wifi_infos, ';', 2), '|', 2) AS wifi2_strong
	, split_part(split_part(wifi_infos, ';', 3), '|', 1) AS wifi3
	, split_part(split_part(wifi_infos, ';', 3), '|', 2) AS wifi3_strong
	, split_part(split_part(wifi_infos, ';', 4), '|', 1) AS wifi4
	, split_part(split_part(wifi_infos, ';', 4), '|', 2) AS wifi4_strong
	, split_part(split_part(wifi_infos, ';', 5), '|', 1) AS wifi5
	, split_part(split_part(wifi_infos, ';', 5), '|', 2) AS wifi5_strong
	, split_part(split_part(wifi_infos, ';', 6), '|', 1) AS wifi6
	, split_part(split_part(wifi_infos, ';', 6), '|', 2) AS wifi6_strong
	, split_part(split_part(wifi_infos, ';', 7), '|', 1) AS wifi7
	, split_part(split_part(wifi_infos, ';', 7), '|', 2) AS wifi7_strong
	, split_part(split_part(wifi_infos, ';', 8), '|', 1) AS wifi8
	, split_part(split_part(wifi_infos, ';', 8), '|', 2) AS wifi8_strong
	, split_part(split_part(wifi_infos, ';', 9), '|', 1) AS wifi9
	, split_part(split_part(wifi_infos, ';', 9), '|', 2) AS wifi9_strong
	, split_part(split_part(wifi_infos, ';', 10), '|', 1) AS wifi10
	, split_part(split_part(wifi_infos, ';', 10), '|', 2) AS wifi10_strong
	, split_part(split_part(wifi_infos, ';', 11), '|', 1) AS wifi11
	, split_part(split_part(wifi_infos, ';', 11), '|', 2) AS wifi11_strong
	, split_part(split_part(wifi_infos, ';', 12), '|', 1) AS wifi12
	, split_part(split_part(wifi_infos, ';', 12), '|', 2) AS wifi12_strong
	, split_part(split_part(wifi_infos, ';', 13), '|', 1) AS wifi13
	, split_part(split_part(wifi_infos, ';', 13), '|', 2) AS wifi13_strong
	, split_part(split_part(wifi_infos, ';', 14), '|', 1) AS wifi14
	, split_part(split_part(wifi_infos, ';', 14), '|', 2) AS wifi14_strong
	, split_part(split_part(wifi_infos, ';', 15), '|', 1) AS wifi15
	, split_part(split_part(wifi_infos, ';', 15), '|', 2) AS wifi15_strong
	, split_part(split_part(wifi_infos, ';', 16), '|', 1) AS wifi16
	, split_part(split_part(wifi_infos, ';', 16), '|', 2) AS wifi16_strong
	, split_part(split_part(wifi_infos, ';', 17), '|', 1) AS wifi17
	, split_part(split_part(wifi_infos, ';', 17), '|', 2) AS wifi17_strong
	, split_part(split_part(wifi_infos, ';', 18), '|', 1) AS wifi18
	, split_part(split_part(wifi_infos, ';', 18), '|', 2) AS wifi18_strong
	, split_part(split_part(wifi_infos, ';', 19), '|', 1) AS wifi19
	, split_part(split_part(wifi_infos, ';', 19), '|', 2) AS wifi19_strong
	, split_part(split_part(wifi_infos, ';', 20), '|', 1) AS wifi20
	, split_part(split_part(wifi_infos, ';', 20), '|', 2) AS wifi20_strong
FROM odps_tc_257100_f673506e024.ant_tianchi_ccf_sl_user_shop_behavior User
INNER JOIN odps_tc_257100_f673506e024.ant_tianchi_ccf_sl_shop_info Mall
ON user.shop_id = mall.shop_id;


drop table if exists hr_train_wifi;

CREATE TABLE hr_train_wifi (
	row_id STRING,
	mall_id STRING,
	wifi_bssid STRING,
	strong STRING
);

insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi1, wifi1_strong
            FROM hr_train WHERE wifi1 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi2, wifi2_strong
            FROM hr_train WHERE wifi2 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi3, wifi3_strong
            FROM hr_train WHERE wifi3 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi4, wifi4_strong
            FROM hr_train WHERE wifi4 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi5, wifi5_strong
            FROM hr_train WHERE wifi5 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi6, wifi6_strong
            FROM hr_train WHERE wifi6 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi7, wifi7_strong
            FROM hr_train WHERE wifi7 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi8, wifi8_strong
            FROM hr_train WHERE wifi8 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi9, wifi9_strong
            FROM hr_train WHERE wifi9 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi10, wifi10_strong
            FROM hr_train WHERE wifi10 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi11, wifi11_strong
            FROM hr_train WHERE wifi11 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi12, wifi12_strong
            FROM hr_train WHERE wifi12 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi13, wifi13_strong
            FROM hr_train WHERE wifi13 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi14, wifi14_strong
            FROM hr_train WHERE wifi14 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi15, wifi15_strong
            FROM hr_train WHERE wifi15 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi16, wifi16_strong
            FROM hr_train WHERE wifi16 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi17, wifi17_strong
            FROM hr_train WHERE wifi17 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi18, wifi18_strong
            FROM hr_train WHERE wifi18 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi19, wifi19_strong
            FROM hr_train WHERE wifi19 != '';


            insert into hr_train_wifi(row_id,mall_id,wifi_bssid,strong)
            select row_id, mall_id, wifi20, wifi20_strong
            FROM hr_train WHERE wifi20 != '';




