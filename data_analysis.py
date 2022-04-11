import MetaTrader5 as mt5
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import sys
import pytz
import scipy.signal as signal
import seaborn as sns
#数据分析 方差 标准差 平均 以及画图

# 建立与MetaTrader 5程序端的连接
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()


symbol_list = {"EURUSD","GBPUSD","USDJPY", "AUDUSD", "USDCAD", "NZDUSD"}
# set time zone to UTC    
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2021, 6, 30, 16, 15, tzinfo=timezone)
# request 100 000 EURUSD ticks starting from 10.01.2019 in UTC time zone
#ticks = mt5.copy_ticks_from("USDJPY", utc_from, 100000, mt5.COPY_TICKS_ALL)
#ticks = mt5.copy_ticks_from("EURUSD", utc_from, 10000000, mt5.COPY_TICKS_ALL)

#mean hour/min
def ptmean(symbol):
    prd = 4000
    rt = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, utc_from, prd)
    ret = pd.DataFrame(rt)
    print("one", flush=True)
    total = ret.high- ret.low
    print("two", flush=True)
    a = np.mean(total)
    b = np.std(total)
    print("three", flush=True)
    print("mean" + str(a))
    print("std" + str(b))

ptmean("EURUSD")
for i in symbol_list:
    print(i)
    ptmean(i)
    print("\n")
for i in range(length):
    total += ret.high - ret.low
print(total)

 将时间（以秒为单位）转换为日期时间格式
ret['time']=pd.to_datetime(ret['time'], unit='s')
ticks = mt5.copy_ticks_from("EURUSD", utc_from, 10000000, mt5.COPY_TICKS_ALL)




#采样
ret = []
index = 0
for itr in ticks:
    index = index + 1
    if index % 200 == 0:
        ret.append(itr)
ticks = np.array(ret)

tf = pd.DataFrame(ticks)
tf['time']=pd.to_datetime(tf['time'], unit='s')

#计算所有的最值的平均值和平方差
a = np.mean(tf.bid)
b = np.std(tf.bid)
print(a)
print(b)

x = np.array(tf.bid)
gt = x[signal.argrelextrema(x, np.greater)]
ls = x[signal.argrelextrema(x, np.less)]


total = []
for itr in range(min(len(ls), len(gt))):
    #tmp = gt[itr] - ls[itr]
    tmp = ls[itr] - gt[itr]
    total.append(tmp)

#一维密度分布图
sns.displot(total)
plt.show()

#平均值和方差
a = np.mean(total)
b = np.std(total)
#c = np.argmax(total)
print(a)
print(b)
#print(c)

#最值出现的位置
print (signal.argrelextrema(x, np.greater))
print (signal.argrelextrema(x, np.less))

#画出最值
plt.plot(np.arange(len(x)) , x)
plt.plot(signal.argrelextrema(x,np.greater)[0],x[signal.argrelextrema(x, np.greater)],'o')
plt.plot(signal.argrelextrema(-x,np.greater)[0],x[signal.argrelextrema(-x, np.greater)],'+')
plt.show()

