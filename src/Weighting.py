# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 23:46:57 2017

@author: Song
"""
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
dir='C:\\Users\\Administrator\\Desktop\\sub\\song\\data\\' #运行代码请更改此路径

submission=pd.read_csv(dir+'base.csv')

train=submission
train['month']=train['time'].map(lambda x :x.split('/')[1])
train['date1']=train['time'].map(lambda x:datetime.strptime(x,'%Y/%m/%d'))
train['week_day'] = train['date1'].map(lambda x: x.weekday() + 1)
train['date1']=train['date1'].map(lambda x:x.strftime('%Y-%m-%d'))

submission=train
##统计
id_small=[]
id_little=[] 
for id in range(1,401):
    if (train.loc[(train['SHEDID']==id)&(train['RT']==3)]['RT'].count())>40:##0较多的id
        id_small.append(id)
    if (train.loc[(train['SHEDID']==id)]['RT'].count())<35:
        id_little.append(id)
        
pre=['RT','LEASE']

id_shed=[x for x in range(1,401) if x not in id_little]

#趋势系数
trend_param={
        'week1':1,
        'week2':5,
        'week3':7,
        'week4':7,
        'week5':9,
        'week6':9,
        'week7':10,
        'week8':9,
        'week9':8,
        }

for i in id_shed:
    for rl in pre:  
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-01')&(submission['date1']<='2015-09-07'),rl]=submission[rl]+trend_param['week1']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-08')&(submission['date1']<='2015-09-14'),rl]=submission[rl]+trend_param['week2']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-15')&(submission['date1']<='2015-09-21'),rl]=submission[rl]+trend_param['week3']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-22')&(submission['date1']<='2015-09-28'),rl]=submission[rl]+trend_param['week4']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-09-29')&(submission['date1']<='2015-10-05'),rl]=submission[rl]+trend_param['week5']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-06')&(submission['date1']<='2015-10-12'),rl]=submission[rl]+trend_param['week6']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-13')&(submission['date1']<='2015-10-19'),rl]=submission[rl]+trend_param['week7']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-20')&(submission['date1']<='2015-10-26'),rl]=submission[rl]+trend_param['week8']
        submission.loc[(submission['SHEDID']==i)&(submission['date1']>='2015-10-27')&(submission['date1']<='2015-10-31'),rl]=submission[rl]+trend_param['week9']
        
#submission.to_csv(dir+'base_temp.csv',index=False)

#print ('----')
#submission=pd.read_csv(dir+'base_temp.csv')
df=pd.read_csv(dir+'df_dorpNULL.csv')

def dropVacationaRain():
    drop_day=['2015-01-01','2015-01-02','2015-01-03','2015-02-18','2015-02-19','2015-02-20','2015-02-21','2015-02-22','2015-02-23','2015-02-24','2015-04-04','2015-04-05','2015-04-06',
    '2015-05-01', '2015-05-02', '2015-05-03', '2015-06-20', '2015-06-21','2015-06-22',
    '2015-09-27','2015-10-01','2015-10-02','2015-10-03','2015-10-04','2015-10-05','2015-10-06','2015-10-07',
    
    '2015-03-17','2015-03-18','2015-03-19','2015-04-18''2015-04-19','2015-06-23','2015-06-24','2015-06-25',
    '2015-07-10','2015-07-11','2015-07-12','2015-07-15','2015-07-16','2015-07-17','2015-07-18','2015-07-19',
    '2015-07-20','2015-07-21','2015-08-09','2015-08-10','2015-08-11'
    ]
    df_list=df.loc[df['SHEDID']==2]['date1'].tolist()
    needDay=[x for x in df_list if x not in drop_day]
    drop_day=pd.DataFrame({'date1':needDay})
    return pd.merge(drop_day,df,on='date1',how='left')
df=dropVacationaRain()
df=df.sort_index(by='RT')
id_sheid=df['SHEDID'].drop_duplicates().values

df_mean=df.groupby(df['SHEDID']).mean()
df_median=df.groupby(df['SHEDID']).median()
df_median_lastmonth=df.loc[(df['date1']>='2015-08-01')].groupby(df.loc[(df['date1']>='2015-08-01')]['SHEDID']).median()
df_median_4=df.loc[(df['date1']>='2015-04-01')&(df['date1']<='2015-04-30')].groupby(df['SHEDID']).median()

id_4=df_median_4['SHEDID'].tolist()
df_4_8=pd.merge(df_median_4,df_median_lastmonth,on='SHEDID',how='left',suffixes=('_4','_8'))

df_4_8['cha']=df_4_8['RT_4']-df_4_8['RT_8']

big_inc=df_4_8[df_4_8['cha']>=13][['SHEDID','cha']]


big_inc.loc[big_inc['SHEDID']==170,'cha']=30

id_big_inc=big_inc['SHEDID'].tolist()
#plt.figure(figsize=(20,10))
#plt.plot(df_4_8['SHEDID'],df_4_8['cha'])

id_big=[]
id_big=df[-2500:]['SHEDID'].drop_duplicates().values
df['idx']=df['SHEDID']

df_week_mean=df.groupby(df['week_day']).mean()
df_week_median=df.groupby(df['week_day']).median()

df_week_median_4=df.loc[(df['date1']>='2015-04-01')&(df['date1']<='2015-04-30')].groupby(['SHEDID','week_day']).median()
df_week_median_8=df.loc[(df['date1']>='2015-08-01')].groupby(['SHEDID','week_day']).median()
df_week_median_all=df.groupby(['SHEDID','week_day']).median()

df_week_median_4_tj=df_week_median_4.groupby(df_week_median_4['idx']).mean()
df_week_median_8_tj=df_week_median_8.groupby(df_week_median_8['idx']).mean()
df_week_median_all_tj=df_week_median_all.groupby(df_week_median_all['idx']).mean()

week_4=pd.merge(df_week_median_4,df_week_median_4_tj,left_on='idx',right_index=True,how='left').fillna(1)
week_4['bili_rt']=week_4['RT_x']/week_4['RT_y']
week_4['bili_lease']=week_4['LEASE_x']/week_4['LEASE_y']
week_8=pd.merge(df_week_median_8,df_week_median_8_tj,left_on='idx',right_index=True,how='left').fillna(1)
week_8['bili_rt']=week_8['RT_x']/week_8['RT_y']
week_8['bili_lease']=week_8['LEASE_x']/week_8['LEASE_y']
week_all=pd.merge(df_week_median_all,df_week_median_all_tj,left_on='idx',right_index=True,how='left').fillna(1)
week_all['bili_rt']=week_all['RT_x']/week_all['RT_y']
week_all['bili_lease']=week_all['LEASE_x']/week_all['LEASE_y']

df_bili=pd.DataFrame()
df_bili['all_rt']=week_all['bili_rt']
df_bili['all_lease']=week_all['bili_lease']
df_bili['4_rt']=week_4['bili_rt']
df_bili['4_lease']=week_4['bili_lease']
df_bili['8_rt']=week_8['bili_rt']
df_bili['8_lease']=week_8['bili_lease']

df_bili=df_bili.fillna(1)

#异常点处理 
df_bili.replace(to_replace=0, value=1, inplace=True)
df_bili.replace(to_replace=7, value=1, inplace=True)
df_bili.replace(to_replace=5, value=1, inplace=True)
df_bili.replace(to_replace=3.5, value=1, inplace=True)
df_bili.replace(to_replace=4.66667, value=1, inplace=True)
df_bili.replace(to_replace=3.44444, value=1, inplace=True)

df_bili['RT']=(df_bili['all_rt']+df_bili['4_rt']+df_bili['8_rt'])/3
df_bili['LEASE']=(df_bili['all_lease']+df_bili['4_lease']+df_bili['8_lease'])/3
df_bili=df_bili.reset_index()


#98号站点 由于4月份没有该站点，所以需另外考虑。
for rl in pre:
    submission.loc[(submission['SHEDID']==98)&(submission['date1']>='2015-10-06')&(submission['date1']<='2015-10-31'),rl]=submission[rl]+25



#对8月份与4月份 增减幅度较大的站点 处理
for id in id_big_inc:
    for rl in pre:               
        submission.loc[(submission['SHEDID']==id)&(submission['date1']>='2015-09-29')&(submission['date1']<='2015-10-05'),rl]=submission[rl]+(big_inc[(big_inc['SHEDID']==id)]['cha'].tolist()[0]-8)*0.3
        submission.loc[(submission['SHEDID']==id)&(submission['date1']>='2015-10-06')&(submission['date1']<='2015-10-12'),rl]=submission[rl]+(big_inc[(big_inc['SHEDID']==id)]['cha'].tolist()[0]-9)*0.65
        submission.loc[(submission['SHEDID']==id)&(submission['date1']>='2015-10-13')&(submission['date1']<='2015-10-19'),rl]=submission[rl]+(big_inc[(big_inc['SHEDID']==id)]['cha'].tolist()[0]-10)*0.7
        submission.loc[(submission['SHEDID']==id)&(submission['date1']>='2015-10-20')&(submission['date1']<='2015-10-26'),rl]=submission[rl]+(big_inc[(big_inc['SHEDID']==id)]['cha'].tolist()[0]-9)*0.65
        submission.loc[(submission['SHEDID']==id)&(submission['date1']>='2015-10-27')&(submission['date1']<='2015-10-31'),rl]=submission[rl]+(big_inc[(big_inc['SHEDID']==id)]['cha'].tolist()[0]-8)*0.5


##新的id的预测
id_new=[94,279,356,362,389,395,396,397,400]
for id in id_new:
    for rl in pre: 
        submission.loc[submission['SHEDID']==id,rl]=25

#星期几处理，通过统计分析得到一个周几因子
week=[1,2,3,4,5,6,7] 
for id in [x for x in id_sheid if x not in [238,357,392,393,394,249,398,399]]:#这几个站点是异常站点，其拥有的数据没有一周
  #  print(id)
    for wk in week: 
    #    for rl in pre:            
        submission.loc[(submission['SHEDID']==id)&(submission['week_day']==wk),'RT']=submission['RT']*(df_bili[(df_bili['SHEDID']==id)&(df_bili['week_day']==wk)]['RT'].tolist()[0])
        submission.loc[(submission['SHEDID']==id)&(submission['week_day']==wk),'LEASE']=submission['LEASE']*(df_bili[(df_bili['SHEDID']==id)&(df_bili['week_day']==wk)]['LEASE'].tolist()[0])


#节假日处理，通过统计分析得到一个节假日因子
vacation_param={
       '09-27': 0.633,
       '10-01': 0.62,
       '10-02': 0.62,
       '10-03': 0.674,
       '10-04': 0.633,
       '10-05': 0.62,
       '10-06': 0.62,
       '10-07': 0.62
      }
#还车
submission.loc[submission['date1']=='2015-10-01','RT']=submission['RT']*vacation_param['10-01']
submission.loc[submission['date1']=='2015-10-02','RT']=submission['RT']*vacation_param['10-02']
submission.loc[submission['date1']=='2015-10-03','RT']=submission['RT']*vacation_param['10-03']
submission.loc[submission['date1']=='2015-10-04','RT']=submission['RT']*vacation_param['10-04']
submission.loc[submission['date1']=='2015-10-05','RT']=submission['RT']*vacation_param['10-05']
submission.loc[submission['date1']=='2015-10-06','RT']=submission['RT']*vacation_param['10-06']
submission.loc[submission['date1']=='2015-10-07','RT']=submission['RT']*vacation_param['10-07']
submission.loc[submission['date1']=='2015-09-27','RT']=submission['RT']*vacation_param['09-27']
#租车
submission.loc[submission['date1']=='2015-10-01','LEASE']=submission['LEASE']*vacation_param['10-01']
submission.loc[submission['date1']=='2015-10-02','LEASE']=submission['LEASE']*vacation_param['10-02']
submission.loc[submission['date1']=='2015-10-03','LEASE']=submission['LEASE']*vacation_param['10-03']
submission.loc[submission['date1']=='2015-10-04','LEASE']=submission['LEASE']*vacation_param['10-04']
submission.loc[submission['date1']=='2015-10-05','LEASE']=submission['LEASE']*vacation_param['10-05']
submission.loc[submission['date1']=='2015-10-06','LEASE']=submission['LEASE']*vacation_param['10-06']
submission.loc[submission['date1']=='2015-10-07','LEASE']=submission['LEASE']*vacation_param['10-07']
submission.loc[submission['date1']=='2015-09-27','LEASE']=submission['LEASE']*vacation_param['09-27']


#下雨天气处理，通过统计分析得到一个下雨天因子

rain_param={
        '09-04':0.87,
        '09-05':0.88
        }

submission.loc[(submission['date1']=='2015-09-04')|(submission['date1']=='2015-09-05'),'RT']=submission['RT']*0.87
submission.loc[submission['date1']=='2015-09-30','RT']=submission['RT']*0.88

submission.loc[(submission['date1']=='2015-09-04')|(submission['date1']=='2015-09-05'),'LEASE']=submission['LEASE']*0.88
submission.loc[submission['date1']=='2015-09-30','LEASE']=submission['LEASE']*0.88


#所有0的替换为1
submission.replace(to_replace=0, value=1, inplace=True)

submission=submission[['SHEDID','time','RT','LEASE']]
submission['RT']=np.rint(submission['RT'])
submission['LEASE']=np.rint(submission['LEASE'])
submission['RT']=submission['RT'].astype(int)
submission['LEASE']=submission['LEASE'].astype(int)
submission.to_csv(dir+'sub666.csv',index=False)


