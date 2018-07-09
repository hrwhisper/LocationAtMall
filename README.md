# 天池 商场中精确定位用户所在店铺
- B榜 0.92115 
- Rank 13



- run `analysis_mall_location_data.py` for `./feature_save/mall_center_and_area.csv`
- run `analysis_wifi_data.py` for some wifi table.



| 文件名(.py)                    | 说明                                |
| ------------------------------ | ----------------------------------- |
| analysis_mall_location_data.py | 分析mall的信息                      |
| analysis_user_data             | 分析用户信息                        |
| analysis_wifi_data             | 分析wifi信息                        |
| common_helper                  | 一些通用的函数                      |
| grid_search                    | 参数搜索，调参用的                  |
| model_stacking                 | 集成学习-stacking方法               |
| **model_test**                 | 单模型入口，定义使用的特征等        |
| **model_voting**               | 模型融合-投票方法，最后的时候上分用 |
| parse_data                     | 读取数据                            |
| predict_category_pro           | 预测类别的概率                      |
| predict_price                  | 预测价格                            |
| **use_xxx.py**                 | xxx特征的文件                       |
| visualization_mall_data        | 可视化mall数据                      |
| visulization_wifi_data         | 可视化wifi信息                      |

