# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 20:12:51 2017

@author: Song
"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error   
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

dir='C:\\Users\\Administrator\\Desktop\\sub\\song\\data\\'   #运行代码请更改此路径

df=pd.read_csv(dir+'dfDay_all.csv')
submission=pd.read_csv(dir+'submission_all.csv')

#默认填充25
submission['RT']=25
submission['LEASE']=25

#log化处理
'''
fig, axes = plt.subplots(nrows=2, ncols=1)
df['RT'].hist(bins=30, ax=axes[0])
df['RT'] = np.log1p(df['RT'])
df['RT'].hist(bins=30, ax=axes[1])
plt.show()
df['LEASE'] = np.log1p(df['LEASE'])

'''


id_shed=df['SHEDID'].drop_duplicates().values


df['date1']=df['time'].map(lambda x:datetime.strptime(x,'%Y-%m-%d'))
df['week_day'] = df['date1'].map(lambda x: x.weekday() + 1)
df['date1']=df['date1'].map(lambda x:x.strftime('%Y-%m-%d'))
submission['date1']=submission['time'].map(lambda x:datetime.strptime(x,'%Y/%m/%d'))
submission['week_day'] = submission['date1'].map(lambda x: x.weekday() + 1)
submission['date1']=submission['date1'].map(lambda x:x.strftime('%Y-%m-%d'))

#各个站点开始时间，除此之外的都是从2015-01-01 开始
dc ={1:'01-14',11:'05-14',23:'03-04',46:'03-19',52:'05-14',59:'06-30',61:'07-31',62:'02-20',67:'03-10',71:'01-09',
76:'02-01',80:'02-15',81:'02-02',85:'01-07',89:'02-08',90:'02-11',91:'02-11',92:'07-04',93:'06-30',95:'07-03',
96:'08-04',97:'07-03',98:'07-05',99:'07-05',100:'07-05',102:'05-09',103:'05-10',106:'05-12',107:'05-10',108:'05-10',
109:'05-10',110:'05-10',111:'05-10',114:'05-10',115:'05-10',122:'02-02',134:'06-26',147:'07-27',151:'01-08',154:'07-02',
163:'07-09',164:'07-09',166:'07-09',167:'07-09',168:'07-15',171:'08-18',174:'07-09',178:'01-13',185:'01-06',187:'01-09',
191:'02-25',192:'08-03',193:'07-09',195:'07-02',197:'02-25',198:'07-08',200:'08-13',218:'01-09',237:'07-25',238:'08-26',
239:'07-09',240:'07-09',241:'07-09',242:'07-26',243:'07-09',244:'07-11',245:'08-06',246:'08-16',247:'07-29',248:'08-02',
249:'08-30',250:'08-05',251:'02-02',252:'01-07',253:'01-09',254:'01-07',255:'08-06',256:'02-10',258:'02-10',259:'06-07',
260:'01-16',261:'01-07',262:'01-09',264:'02-03',266:'01-06',268:'08-16',269:'02-10',270:'02-02',271:'03-06',272:'02-11',
273:'02-11',274:'02-15',275:'02-11',276:'02-11',277:'07-11',278:'08-12',280:'07-31',281:'07-31',282:'07-07',283:'07-11',
284:'07-06',285:'07-11',286:'07-10',287:'07-10',288:'08-19',289:'08-18',290:'07-24',291:'07-23',292:'08-13',293:'08-16',
294:'08-22',295:'07-29',296:'07-14',297:'06-30',298:'06-30',299:'07-16',300:'02-25',307:'07-27',312:'02-06',315:'01-09',
320:'02-11',321:'02-11',322:'02-11',323:'05-10',324:'08-19',325:'08-12',326:'08-14',327:'08-15',328:'07-29',329:'07-16',
330:'08-12',331:'08-19',332:'08-09',333:'08-09',334:'08-09',335:'07-09',337:'08-13',338:'07-31',339:'07-31',340:'07-31',
341:'07-24',342:'08-12',343:'08-06',344:'08-24',345:'08-10',346:'08-09',347:'08-10',348:'08-05',349:'08-15',350:'08-13',
351:'08-15',352:'08-03',353:'08-07',354:'08-11',355:'08-05',357:'08-27',358:'08-08',359:'08-12',360:'08-16',361:'08-16',
363:'08-07',364:'06-30',365:'08-08',366:'08-07',367:'08-16',368:'08-04',369:'07-16',370:'08-07',371:'08-04',372:'08-13',
373:'08-05',374:'08-16',375:'08-08',376:'08-15',377:'08-12',378:'08-14',379:'07-24',380:'08-12',381:'07-30',382:'08-14',
383:'08-20',384:'08-12',385:'07-31',386:'08-18',387:'07-24',388:'08-16',390:'08-25',391:'08-09',392:'08-27',393:'08-27',
394:'08-27',398:'08-30',399:'08-30'}

date_null=map((lambda x:'2015-'+x),dc.values())

id_null=dc.keys()  #有缺失的id
id_nonull=[id for id in id_shed if id not in id_null]#没有缺失的id
#id_new=[id for id in id_sub if id not in id_shed ]  #只有测试集才有的id

all=[df]
#添加一列 表示时间戳dade
for dataset in all:
    dataset['date']=pd.to_datetime(dataset['date1'].map(lambda x: x[0:10]))

##特征工程
for dataset in all:
     dataset=pd.get_dummies(dataset, columns=[ 'week_day'])

#去除缺失值
def dropNULL():
    df_f=pd.DataFrame()
    #df2=pd.DataFrame()
    
    #id_shed=[1,2,200,399]
    for id in id_shed:
        df1=df.loc[df['SHEDID']==id]
        startTime ='2015-01-01'
    
        if id in id_null:
            startTime ='2015-'+dc[id]
            
        df2=df1[df1['date1']>=startTime]
        df_f=pd.concat([df_f,df2])
    df_f.to_csv(dir+'df_dorpNULL.csv',index=False)

dropNULL()   
df_dropNULL=pd.read_csv(dir+'df_dorpNULL.csv')
df_dropNULL['RT'] = np.log1p(df_dropNULL['RT'])
df_dropNULL['LEASE'] = np.log1p(df_dropNULL['LEASE'])

#df_dropNULL=df_dropNULL[df_dropNULL['date1']>='2015-08-25']
#去除有下雨天和假期的这周数据
df_dropVR=pd.DataFrame()
def dropVacationaRain():
    drop_day=['2015-01-01','2015-01-02','2015-01-03','2015-02-18','2015-02-19','2015-02-20','2015-02-21','2015-02-22','2015-02-23','2015-02-24','2015-04-04','2015-04-05','2015-04-06',
    '2015-05-01', '2015-05-02', '2015-05-03', '2015-06-20', '2015-06-21','2015-06-22',
    '2015-09-27','2015-10-01','2015-10-02','2015-10-03','2015-10-04','2015-10-05','2015-10-06','2015-10-07',
    
    '2015-03-17','2015-03-18','2015-03-19','2015-04-18''2015-04-19','2015-06-23','2015-06-24','2015-06-25',
    '2015-07-10','2015-07-11','2015-07-12','2015-07-15','2015-07-16','2015-07-17','2015-07-18','2015-07-19',
    '2015-07-20','2015-07-21','2015-08-09','2015-08-10','2015-08-11'
    ]
    df_list=df_dropNULL.loc[df_dropNULL['SHEDID']==2]['date1'].tolist()
    needDay=[x for x in df_list if x not in drop_day]
    drop_day=pd.DataFrame({'date1':needDay})
    return pd.merge(drop_day,df_dropNULL,on='date1',how='left')
    

df_dropVR=dropVacationaRain()   
df_dropVR1=df_dropVR.loc[df_dropVR['SHEDID']==1]  #yong1ceshi
xingqiji =df_dropVR1.groupby(['week_day']).mean()
xingjiqi_weight_rt=[]
xingjiqi_weight_lease=[]
for j in range(1,8):
    xingjiqi_weight_rt.append(xingqiji['RT'][j]/(xingqiji['RT'].sum())/(1/7))
    xingjiqi_weight_lease.append(xingqiji['LEASE'][j]/(xingqiji['LEASE'].sum())/(1/7))
    
#获取假期权重。。。。样本较少 ，效果不一定好，可自行调参数
df_V=pd.DataFrame()
def VacationData():
    vacation_day=['2015-01-01','2015-01-02','2015-01-03','2015-02-18','2015-02-19','2015-02-20','2015-02-21','2015-02-22','2015-02-23','2015-02-24','2015-04-04','2015-04-05','2015-04-06',
    '2015-05-01', '2015-05-02', '2015-05-03', '2015-06-20', '2015-06-21','2015-06-22',
    '2015-09-27','2015-10-01','2015-10-02','2015-10-03','2015-10-04','2015-10-05','2015-10-06','2015-10-07'
    ]
    #df_list=df_dropNULL.loc[df_dropNULL['SHEDID']==2]['date1'].tolist()
    #needDay=[x for x in df_list if x not in drop_day]
    vacation_day=pd.DataFrame({'date1':vacation_day})
    return pd.merge(vacation_day,df_dropNULL,on='date1',how='left')  

df_V=VacationData()       
  
df_V1=df_V.loc[df_V['SHEDID']==1]
xingqijiV =df_V1.groupby(['week_day']).mean()
xingjiqiV_weight_rt=[]
xingjiqiV_weight_lease=[]
for j in range(1,8):
    xingjiqiV_weight_rt.append(xingqijiV['RT'][j]/xingqiji['RT'][j])
    xingjiqiV_weight_lease.append(xingqijiV['LEASE'][j]/xingqiji['LEASE'][j])   

#获取下雨权重。
df_R=pd.DataFrame()
def RainData():
    rain_day=[ '2015-03-17','2015-03-18','2015-03-19','2015-04-18''2015-04-19','2015-06-23','2015-06-24','2015-06-25',
    '2015-07-10','2015-07-11','2015-07-12','2015-07-15','2015-07-16','2015-07-17','2015-07-18','2015-07-19',
    '2015-07-20','2015-07-21','2015-08-09','2015-08-10','2015-08-11'
    ]
    #df_list=df_dropNULL.loc[df_dropNULL['SHEDID']==2]['date1'].tolist()
    #needDay=[x for x in df_list if x not in drop_day]
    rain_day=pd.DataFrame({'date1':rain_day})
    return pd.merge(rain_day,df_dropNULL,on='date1',how='left')  

df_R=RainData()       
  
df_R1=df_R.loc[df_R['SHEDID']==1]
xingqijiR =df_R1.groupby(['week_day']).mean()
xingjiqiR_weight_rt=[]
xingjiqiR_weight_lease=[]
for j in range(1,8):
    xingjiqiR_weight_rt.append(xingqijiR['RT'][j]/xingqiji['RT'][j])
    xingjiqiR_weight_lease.append(xingqijiR['LEASE'][j]/xingqiji['LEASE'][j])  


##按每周预测     模型预测
   
temp_id=[]
for i in id_null:
    if '2015-'+dc[i]<='2015-08-11':
        temp_id.append(i)
id_nonull.extend(temp_id)######注意这里变了
id_nullbf811=id_nonull
#id_nullbf811=#id_nullbf811.extend(id_nonull)

#以最近一周的数据    5.6 倒数第二周4.736,4.761  4.799（未错位）
def lastweek(i,tt):
    df1=df.loc[df['SHEDID']==i]
    df1=df1[df1['date1']>='2015-08-25']
    #df1=df1[df1['date1']>='2015-08-19']
    #df1=df1[df1['date1']<='2015-08-25']
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow*9
        submission.loc[submission['SHEDID']==i,'RT']=predictons[:-2]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow*9
        submission.loc[submission['SHEDID']==i,'LEASE']=predictons[:-2]

def lastTwoWeek(i,tt):
    df1=df.loc[df['SHEDID']==i]
   # df1=df1[df1['date1']>='2015-08-25']
    df1=df1[df1['date1']>='2015-08-18']
    df1=df1[df1['date1']<='2015-08-24']
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow*9
        submission.loc[submission['SHEDID']==i,'RT']=predictons[:-2]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow*9
        submission.loc[submission['SHEDID']==i,'LEASE']=predictons[:-2]
        
def chunjiefill(i,tt):
    df1=df.loc[df['SHEDID']==i]
    df1=df1[df1['date1']>='2015-01-19']
    df1=df1[df1['date1']<='2015-03-20']
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[submission['SHEDID']==i,'RT']=predictons
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[submission['SHEDID']==i,'LEASE']=predictons

def lastweek_1week(i,tt):#最后一周填充最初的一周
    df1=df.loc[df['SHEDID']==i]
    df1=df1[df1['date1']>='2015-08-25']
    #df1=df1[df1['date1']>='2015-08-19']
    #df1=df1[df1['date1']<='2015-08-25']
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow*2
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-01')&(submission['date1']<='2015-09-14'),'RT']=[x for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow*2
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-01')&(submission['date1']<='2015-09-14'),'LEASE']=[x for x in predictons]

def siyue21_2week(i,tt,a,b):#获取4-21-4-27的数据
    startTime='2015-01-01'
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>'2015-08-25':
        
        df1=df.loc[df['SHEDID']==i]
        df1=df1[df1['date1']>='2015-08-25']
        #df1=df1[df1['date1']>='2015-08-19']
        #df1=df1[df1['date1']<='2015-08-25']
        flow=[]
        if tt==0:
            flow = df1['RT'].tolist()
            predictons = flow
            submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-08')&(submission['date1']<='2015-09-14'),'RT']=[x+1 for x in predictons]
        else:
            flow = df1['LEASE'].tolist()
            predictons = flow
            submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-08')&(submission['date1']<='2015-09-14'),'LEASE']=[x+1 for x in predictons]
    else:
    
        df1=df.loc[df['SHEDID']==i]
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
        flow=[]
        if tt==0:
            flow = df1['RT'].tolist()
            #print(flow)
            predictons = flow
            submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-08')&(submission['date1']<='2015-09-14'),'RT']=[x for x in predictons]
        else:
            flow = df1['LEASE'].tolist()
            predictons = flow
            submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-08')&(submission['date1']<='2015-09-14'),'LEASE']=[x for x in predictons]

def siyue21_3week(i,tt,a,b):#获取4-21-4-27的数据
    
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
   
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-15')&(submission['date1']<='2015-09-21'),'RT']=[x+2 for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-15')&(submission['date1']<='2015-09-21'),'LEASE']=[x+2 for x in predictons]
def siyue21_4week(i,tt,a,b):#获取4-21-4-27的数据
          
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]

    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-22')&(submission['date1']<='2015-09-28'),'RT']=[4 for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-22')&(submission['date1']<='2015-09-28'),'LEASE']=[4 for x in predictons]
def siyue21_5week(i,tt,a,b):#获取4-21-4-27的数据
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-29')&(submission['date1']<='2015-10-05'),'RT']=[x+6 for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-29')&(submission['date1']<='2015-10-05'),'LEASE']=[x+6 for x in predictons]
def siyue21_6week(i,tt,a,b):#获取4-21-4-27的数据
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-06')&(submission['date1']<='2015-10-12'),'RT']=[x+7 for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-06')&(submission['date1']<='2015-10-12'),'LEASE']=[x+7 for x in predictons]
def siyue21_7week(i,tt,a,b):#获取4-21-4-27的数据
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-13')&(submission['date1']<='2015-10-19'),'RT']=[x+7 for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-13')&(submission['date1']<='2015-10-19'),'LEASE']=[x+7 for x in predictons]

def siyue21_8week(i,tt,a,b):#获取4-21-4-27的数据
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-20')&(submission['date1']<='2015-10-26'),'RT']=[x+7 for x in predictons]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-20')&(submission['date1']<='2015-10-26'),'LEASE']=[x+7 for x in predictons]


def siyue21_9week(i,tt,a,b):#获取4-21-4-27的数据
    startTime='2015-01-01'
    df1=df.loc[df['SHEDID']==i]
    if i in id_null:
        startTime ='2015-'+dc[i]
    if startTime>a: 
        df1=df1[df1['date1']>='2015-08-25']
    else:
        df1=df1[df1['date1']>=a]
        df1=df1[df1['date1']<=b]
    flow=[]
    if tt==0:
        flow = df1['RT'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-27')&(submission['date1']<='2015-10-31'),'RT']=[x+7 for x in predictons[:-2]]
    else:
        flow = df1['LEASE'].tolist()
        predictons = flow
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-27')&(submission['date1']<='2015-10-31'),'LEASE']=[x+7 for x in predictons[:-2]]


 #按周预测    
for tt in range(2):
    for i in id_shed:
        #print('predicting: %4d'%i)
        #weekly_flow = pd.Series(np.ones(7, dtype=int), [d.strftime('%Y-%m-%d') for d in pd.date_range('10/25/2016', periods=7)])
        df1=df.loc[df['SHEDID']==i]
        
        lastweek_1week(i,tt)#预测最初一个礼拜
        #siyue21_2week(i,tt)
        a='2015-05-19'
        b='2015-05-25'
        siyue21_3week(i,tt,a,b)
        siyue21_4week(i,tt,a,b)
        siyue21_5week(i,tt,a,b)
        siyue21_6week(i,tt,a,b)
        siyue21_7week(i,tt,a,b)
        siyue21_8week(i,tt,a,b)
        siyue21_9week(i,tt,a,b)


test_lastweek=df[df['date1']>='2015-08-25']    #5.8#######---------
#id_nullbf811=[1]
train=df[df['date1']>='2015-08-11']

min_rems=[]
for i in id_nullbf811:
    rems=[]
    b_all=[]
    test_lastweek1=test_lastweek.loc[test_lastweek['SHEDID']==i]
    train1=train.loc[train['SHEDID']==i]
    
    for b in range(0,180):
        rmse=np.sqrt(mean_squared_error(test_lastweek1['RT'],np.ones(test_lastweek1['RT'].shape[0])*b))
        rems.append(rmse)
        b_all.append(b)
    min_rems.append(min(rems))

    submission.loc[submission['SHEDID']==i,'RT']=b_all[rems.index(min(rems))]
    
#print(np.mean(np.array(min_rems)))

min_lease=[]
for i in id_nullbf811:
    rems=[]
    b_all=[]
    test_lastweek1=test_lastweek.loc[test_lastweek['SHEDID']==i]
    train1=train.loc[train['SHEDID']==i]
    
    for b in range(0,180):
        rmse=np.sqrt(mean_squared_error(test_lastweek1['LEASE'],np.ones(test_lastweek1['LEASE'].shape[0])*b))
        rems.append(rmse)
        b_all.append(b)
    min_lease.append(min(rems))
    submission.loc[submission['SHEDID']==i,'LEASE']=b_all[rems.index(min(rems))]
#print(np.mean(np.array(min_lease)))
   
 
id_nonullbf811=[x for x in id_shed if x not in id_nullbf811]
    
for tt in range(2):
    for i in id_nonullbf811:
       # print('predicting: %4d'%i)
        lastweek(i,tt)



subName='result_base.csv'
submission.to_csv(dir+subName,index=False)


def resultToBase():
    result=pd.read_csv(dir+subName)
    base=pd.read_csv(dir+'example.csv')
    base = pd.merge(base[['SHEDID','time']],result,on = ['SHEDID','time'],how = 'left').fillna(25)
    base=base[['SHEDID','time','RT','LEASE']]
    base['RT']=base['RT'].astype(int)
    base['LEASE']=base['LEASE'].astype(int)
    base.to_csv(dir+'base.csv',index=False)
    
resultToBase()    

