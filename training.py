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
from datetime import datetime
import datetime as dttime
import csv
import talib as ta



today=dttime.date.today()
zhonglei = "EURUSD"
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
utc_tz = pytz.timezone('Etc/UTC')
#utc_from = datetime(2021, today.month, today.day, dttime.datetime.now().hour,  dttime.datetime.now().minute, tzinfo=utc_tz)
utc_from = datetime(2021, today.month, today.day, dttime.datetime.now().hour,  dttime.datetime.now().minute, tzinfo=utc_tz)
prd = 1700 * 12
rt = mt5.copy_rates_from(zhonglei, mt5.TIMEFRAME_M5, utc_from, prd)
ret= pd.DataFrame(rt)
## 将时间（以秒为单位）转换为日期时间格式
ret['real_volume']=pd.to_datetime(ret['time'], unit='s')
price = pd.Series(ret.close)
ta_ema_12 = ta.EMA(price, timeperiod=12)
ta_ema_576 = ta.EMA(price, timeperiod=576)
ta_ema_676 = ta.EMA(price, timeperiod=776)
rsi_ret = ta.RSI(price)
macd, signal, macd_ret = ta.MACD(price, fastperiod=89, slowperiod=144, signalperiod=9)
for i in range(prd):
    print(macd_ret[i])




#ret = dttime.datetime.now().hour
#print(ret)

## 建立与MetaTrader 5程序端的连接
##
#
## set time zone to UTC
#timezone = pytz.timezone("Etc/UTC")
## create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
##utc_from = datetime(2021, 4, 8, 16, 15, tzinfo=timezone)
##utc_from = datetime(2021, 4, 8, 16, 15)
#
## request 100 000 EURUSD ticks starting from 10.01.2019 in UTC time zone
##ticks = mt5.copy_ticks_from("AUDJPY", utc_from, 100000, mt5.COPY_TICKS_ALL)
#
#
##time bid ask last volume time_msc flags volume_real
##bid 买方价，人家愿意出多少买
##ask 卖方价，人家愿意出多少卖
#
#
#
#
#timezone = pytz.timezone("Etc/UTC")
#today=dttime.date.today()
#utc_from = datetime(2021, today.month, today.day, dttime.datetime.now().hour,  dttime.datetime.now().minute,tzinfo=timezone )
##utc_from = datetime(2021, today.month, today.day, dttime.datetime.now().hour,  dttime.datetime.now().minute)
##print(utc_from)
#prd = 4000
#rt = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, utc_from, prd)
#ret= pd.DataFrame(rt)
#### 将时间（以秒为单位）转换为日期时间格式
#ret['real_volume']=pd.to_datetime(ret['time'], unit='s')
#print(ret['real_volume'][0].hour)


#zhonglei="EURUSD"
#timezone = pytz.timezone("Etc/UTC")
#dt_from = datetime(2021, 3, 10, 16, 15, tzinfo=timezone)
#ticks = mt5.copy_ticks_from(zhonglei, dt_from, 2000000000, mt5.COPY_TICKS_ALL)
#search_map = {}
#tf = pd.DataFrame(ticks)
#tf['time']=pd.to_datetime(tf['time'], unit='s')
#print(tf)


#price = pd.Series(ret.close)
##macd_ret, signal,c = ta.MACD(price)
#macd_ret, signal, c= ta.MACD(price, fastperiod=89, slowperiod=144, signalperiod=9)
##macd = signal - macd_ret
#print(macd_ret)
#print(signal)
#print(c)
#
#ta_ema = ta.EMA(price, timeperiod=200)
#print(ta_ema[)
#for i in range(9000, 9999, 1):
#    print(macd_ret[i])
#print("\n")
#print(signal)


#utc_from = datetime(2020, 3, 10, 16, 15)
##ticks = mt5.copy_ticks_from("EURUSD", utc_from, 10, mt5.COPY_TICKS_ALL)
#prd = 10
#ticks = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M5, utc_from, prd)
#ret = pd.DataFrame(ticks)
#ret['real_volume']=pd.to_datetime(ret['time'], unit='s')
#print(ret)
#search_map = {}
#tf = pd.DataFrame(ticks)
#tf['time']=pd.to_datetime(tf['time'], unit='s')


#for itr in range(len(tf)):
#    search_map[tf.time_msc[itr]] = itr
#
#def predict(timesp, action, stop_loss, take_profit):
#    #action = "sell"
#    #timesp = 1617869700060
#    #stop_loss = 0.001
#    #take_profit = 0.001
#    
#    #0      2021-04-08 16:15:00  1.18899  1.18922  ...  1617898500275    134          0.0
#    start = search_map[timesp]
#
#    price_buy = tf.ask[start]
#    price_sell = tf.bid[start]
#    if action == "buy":
#        #print(price_buy)
#        for index in range(start, len(tf.bid)):
#            #止损
#            if tf.bid[index] < price_buy - stop_loss:
#                #print("buy lost")
#                #print(tf.time_msc[index])
#                #print(tf.bid[index])
#                #print(tf.time[index])
#                return 0
#            #止盈
#            if tf.bid[index] > price_buy + take_profit:
#                #print("buy win")
#                #print(tf.bid[index])
#                #dt_object = datetime.fromtimestamp(tf.time_msc[index]/1000, tz=timezone)
#                #print(dt_object)
#                #print(tf.time[index])
#                return 1
#    
#    if action == "sell":
#        #print(price_sell)
#        for index in range(start, len(tf.bid)):
#            #止损
#            if tf.ask[index] > price_sell + stop_loss:
#                #print("sell lost")
#                #print(tf.time[index])
#                #print(tf.ask[index])
#                return 0
#            #止盈
#            if  tf.ask[index] < price_sell - take_profit:
#                #print("sell win")
#                #print(tf.time[index])
#                #print(tf.ask[index])
#                return 1
#
#predict(0,0,0,0)
#def test_random_buy():
#    total = 0
#    win = 0
#    for itr in range(len(tf.time_msc)):
#        if itr % 1000 == 0:
#            ret = predict(tf.time_msc[itr], "buy", 0.00110, 0.0004)
#            if ret == None:
#                break
#            win = int(ret) + win
#            total = total + 1
#    print("total: "+ str(total))
#    print("win: " + str(win))
#    print("lost: " + str(total-win))
#    t = win/total
#    print(t)
#    print(40*t - (1-t)*110)
    
#def find_best_parameter():
#    total = 0
#    win = 0
#    gb = -50
#    gsl = 0
#    gtp = 0
#    gt = 0
#    flag = 0
#    with open('eggs.csv', 'w', newline='') as csvfile:
#        spamwriter = csv.writer(csvfile)
#        for sl in range(30,100,1):
#            for tp in range(30,100,1):
#                win = 0
#                total = 0
#                for itr in range(len(tf.time_msc)):
#                    if itr % 1000 == 0:
#                        action = ""
#                        if flag % 2 == 0:
#                            action = "buy"
#                        if flag % 2 != 0:
#                            action = "sell"
#                        flag = flag + 1
#                        ret = predict(tf.time_msc[itr], action, sl/100000, tp/100000)
#                        if ret == None:
#                            break
#                        win = int(ret) + win
#                        total = total + 1
#                t = win/total
#                exp = tp*t - (1-t)*sl
#                #spamwriter.writerow(["index","a_name","b_name"])
#                spamwriter.writerow(["zhiying", tp])
#                spamwriter.writerow(["zhisun", sl])
#                spamwriter.writerow(["shenglv",t])
#                spamwriter.writerow(["exp", exp])
#                spamwriter.writerow([" ", " "])
#                print("exp: " + str(exp))
#                print("zhiying: " + str(tp))
#                print("zhisun: " + str(sl))
#                print("shenglv: " + str(t))
#                print("\n")
#                sys.stdout.flush()
#                if exp > gb:
#                    gb = exp
#                    gsl = sl
#                    gtp = tp 
#                    gt = t
#
#        print("final")
#        print(gb)
#        print(gsl)
#        print(gtp)
#        print(gt)

    #print("total: "+ str(total))
    #print("win: " + str(win))
    #print("lost: " + str(total-win))

#find_best_parameter()
