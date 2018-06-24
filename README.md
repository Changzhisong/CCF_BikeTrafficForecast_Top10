
![赛题logo](https://github.com/Changzhisong/CCF_BikeTrafficForecast_Top10/blob/master/images/logo.png)  

##<center>  2017 CCF 城市自行车的出行行为分析及效率优化赛题解题方案 </center>

**比赛排名：初赛第6名，复赛第8名**  
**队伍名称：scl（个人单独组队）**   
**Author：Song**  
**E-mail：Z.S.Chang@qq.com**  

----------

## 1 赛题概述:
- **赛题网站：** [CCF 大数据与计算智能大赛](http://www.datafountain.cn/projects/2017CCF/)
- **背景：** 城市共享单车体系逐步渗透到各个城市中，给公众出行的“最后一公里”带来极大便利。随着用户使用量增长和频度的增加，如优化运营效率是随之而来的重要课题。同时，站在城市管理的角度上，共享单车的使用状况也投射出城市人口流动特征，对城市规划、城市交通管理有重要参考价值。
- **赛题数据：** 赛题数据为2015年某城市的自行车数据，数据为完整的真实数据，提供的数据中，对车卡信息进行了脱敏。这里以复赛的数据为准，复赛训练集提供2015年1-8月份的真实数据，样本量为2132693条。具体各维度的信息参见官网。  
    除此之外，官方还提供一些各个站点的粗糙的经纬度数据。
- **赛题目标：** 预测未来两个月，即2015年9月和10月各个自行车站点的每天的借车和还车的流量。
- **测评函数：** *score=1/(1+RMSE)*  
- 【备注】：可以使用外部数据，如天气数据等。

----------
## 2.代码运行环境：  
-	python3.6   
-	pandas（0.20.3）  
-	numpy（1.13.3）  
-	scikit-learn（0.19.1）  
-	xgboost    

-------

## 3.核心代码说明：  
- **预处理：**  
	- 对于某些记录数据出现骑行时间小于30秒的骑行时间进行丢弃处理。
	- 对某些站点可能出现某个时间之后流量为0，可能原因是该站点拆除了。如下站点：  
	![站点异常](https://github.com/Changzhisong/CCF_BikeTrafficForecast_Top10/blob/master/images/站点134.png)    
	- 数据分布大量纯在偏小的流量，如下还车的数据分组分布。对数据流量log(1+x)处理  
	![流量分布](https://github.com/Changzhisong/CCF_BikeTrafficForecast_Top10/blob/master/images/train_mean_rt.png)    
	- 异常点处理：以历史过去14天流量的μ±2σ为限制，其中μ为均值，σ为均方根，以排除异常的流量数据   
	![站点异常](https://github.com/Changzhisong/CCF_BikeTrafficForecast_Top10/blob/master/images/站点39.png)  
	
- **特征工程：**
	- 对根据粗糙的经纬度进行聚类处理，因为在市区人口密集的地方的周围的站点的流量数据都会很大，然后相对郊区的站点的流量数据较小。虽然经纬度不够精确，但对最终结果有所提高。
	- 加入天气数据：通过爬虫爬取了盐城市2015年前10个月的天气数据。天气数据来源：https://www.wunderground.com， 提供了世界各地的气象信息，包含气温，露点，湿度，气压，能见度，风速，瞬时风速，降水量，天气状况等信息。对这些信息构建特征。  
	- 生成人体舒适度指数SSD SSD=(1.818t+18.18)(0.88+0.002f)+(t-32)/(45-t)-3.2v+18.2 其中：温度t，湿度f，风速v。  
	- 节假日特征：对节假日数据进行标记为1，非节假日为0。如下图某站点节假日，雨天与流量的关系，其中黑色点代表节假日与非节假日，红色点为下雨天与非下雨天：  
	![节假日](https://github.com/Changzhisong/CCF_BikeTrafficForecast_Top10/blob/master/images/站点18.png)  
	- 星期几特征： 当天为星期几，one-hot处理
	- 周末特征：当天是否周末  
	- 暑假特征：观察数据发现在7，8月份数据普遍偏高，因此应该是暑假到来引发的，后续验证确实有效。  
	- 季节特征：不同的季节对流量是有影响的  
	- 月份特征：因给定的数据一年都不够，于是这里划分是根据认为感知划分的，即认为11,12,1，2为一个组，3,4,9,10为一个组，5,6,7,8为一个组。
	- 距离因子：当天离预测开始日的距离  
	- 站点的静态特征： 每个站点的桩点个数，人数（不同的借车号id算不同的人），从该站点的借车的总骑行时长，从该站点还车的总时长等等
- `preproccess.py`：将训练数据和测试数据生成各个站点每天的流量数据    
- `constantRegression.py`: 将流量训练数据通过排除缺失值，异常点，然后将8月18-8月31两周的数据作为测试数据，剩余的天数作为训练时间段，生成一个常数回归基础值。  
- `Weighting.py`: 对常数回归基础值进行加权，周期，节假日，天气系数处理后，得到目标预测数据  
	- a.线下测试，各个站点的整体趋势得到一个趋势权重值，在常数回归的基础上叠加该权重值；  
	- b.通过统计分析得到每周周几的一个加权值，分别对4月份、8月份及所有月份进行统计；  
	- c.对10-1~10-7日国庆节假期，通过线下历史数据中节假日与常规日的比例得到节假日权重；  
	- d.通过外部数据对9-04,9-05,9-30等下雨天进行雨天系数加权。  
	- e.各个系数加权后得到该模型未来两个月的预测数据。  
- `xgboost_model.py`:xgboost模型训练； 
- `RandomForest.py`:随机森林模型训练；  
- `ModelMerging_submission`:加权时间序列模型、RF、xgboost融合得到最终的预测结果，提交
## 4.文件说明：  
- `src`：为源码文件
- `data`：包括weather等文件
- `images`：展示图

## 5.代码复现步骤：
-	时间序列加权模型复现步骤：  
	-	A.更改代码中文件的路径，该路径为weather.csv所在的路径
	-	B.将train.csv 放置song->data目录下（或者其他目录也行，只需要把代码中读取train.csv和example.csv的路径改下就行）
	-	C.运行preproccess.py文件，即得到每个站点的流量数据
	-	D.运行constantRegression.py文件，对流量数据进行常数回归
	-	E.运行Weighting.py文件，对回归的基础数据加权处理得到目标数据。  
	【备注】：  
		- A.生成的文件存在data文件夹中，其中目标数据为sub666.csv，其余文件为中间数据保存文件可忽略。
		- B.为保证更好的去复现，只提供了可以复现的代码，相关数据统计分析，画图分析代码未加上。
- xgboost模型复现步骤（后续补上）
- RF模型
- 模型融合