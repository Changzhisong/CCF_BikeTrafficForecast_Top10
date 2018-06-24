# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:50:59 2017

@author: Song
"""
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

dir='C:\\Users\\Administrator\\Desktop\\sub\\song\\data\\' #运行代码请更改此路径

train =pd.read_csv(dir+'train.csv',encoding='gbk')
del train['OPNAME']

#读取外部天气数据
weather=pd.read_csv(dir+'weather1.csv')

#获取上下午的数据
def toTrain_AMPM():
    test_ab = ['201501','201502','201503','201504','201505','201506','201507','201508']
    test_ab_csv = train[train.yearmonth.isin(test_ab)]
    test_ab_csv['LEASEDATE'] = pd.to_datetime(test_ab_csv.LEASEDATE)
    del test_ab_csv['yearmonth']
    test_ab_csv.LEASETIME = test_ab_csv.LEASETIME.str.split(':').map(lambda x:x[0]).astype(int)>=12#是否为上午还是下午
    test_ab_csv['time'] = test_ab_csv.LEASEDATE.dt.date.astype(str) + '-'+test_ab_csv.LEASETIME.astype(int).astype(str)  #time的格式为2015-07-01-0
    test_comit_jieche = test_ab_csv.groupby(['SHEDID','time'])['USETIME'].count().unstack().fillna(0).stack().reset_index()
    test_comit_jieche.columns = ['SHEDID','time','LEASE']
    test_comit_huanche = test_ab_csv.groupby(['RTSHEDID','time'])['USETIME'].count().unstack().fillna(0).stack().reset_index()
    test_comit_huanche.columns = ['SHEDID','time','RT']
    df = pd.merge(test_comit_huanche,test_comit_jieche,on = ['SHEDID','time'],how = 'outer').fillna(0)

    
    df.to_csv(dir+"df.csv",index=False)
    
def toTrain_day():
    test_ab = ['201501','201502','201503','201504','201505','201506','201507','201508']
    test_ab_csv = train[train.yearmonth.isin(test_ab)]
    test_ab_csv['LEASEDATE'] = pd.to_datetime(test_ab_csv.LEASEDATE)
    del test_ab_csv['yearmonth']    
    test_ab_csv['time'] = test_ab_csv.LEASEDATE.dt.date.astype(str)
    test_comit_jieche = test_ab_csv.groupby(['SHEDID','time'])['USETIME'].count().unstack().fillna(0).stack().reset_index()
    test_comit_jieche.columns = ['SHEDID','time','LEASE']
    test_comit_huanche = test_ab_csv.groupby(['RTSHEDID','time'])['USETIME'].count().unstack().fillna(0).stack().reset_index()
    test_comit_huanche.columns = ['SHEDID','time','RT']
    df = pd.merge(test_comit_huanche,test_comit_jieche,on = ['SHEDID','time'],how = 'outer').fillna(0)
    
    df.to_csv(dir+"dfDay_all.csv",index=False)


#toTrain_AMPM()
toTrain_day()

df=pd.read_csv(dir+'dfDay_all.csv')
id_shed=df['SHEDID'].drop_duplicates().values

def creatResultFile():
    tempp=pd.date_range('9/1/2015','10/31/2015')
    #tempp=tempp.map(lambda x:x.strftime('%Y/%m/%d'))#月份和日中有先导0
    tempp=tempp.map(lambda x:str(x.timetuple().tm_year) + '/' + str(x.timetuple().tm_mon) + '/' + str(x.timetuple().tm_mday))
    submission=pd.DataFrame({'SHEDID':np.ones(61),'time':tempp,'RT':1,'LEASE':1})
    submission['SHEDID']=submission['SHEDID'].astype(int)
    s=submission.copy()   
    for id in id_shed:
        if id==1:continue
        s['SHEDID']=id
        submission=pd.concat([submission,s])
    submission=submission[['SHEDID','time','RT','LEASE']]
    submission.to_csv(dir+'submission_all.csv',index=False)
    
creatResultFile()


