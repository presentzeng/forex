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
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import datetime as dttime
import matplotlib.pyplot as plt
import numpy
import talib as ta
up =  100
down = 90
#zhonglei="USDCHF"
zhonglei="EURUSD"
#zhonglei="GBPUSD"

# 建立与MetaTrader 5程序端的连接
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

def ver0_buy(ta12, ta676,i ):
    return ta12[i+2] > ta676[i+2] and ta12[i+1] < ta676[i+1] and ta676[i+2] > ta676[i+1]

def ver0_sell(ta12, ta676,i ):
    return ta12[i+2] < ta676[i+2] and ta12[i+1] > ta676[i+1] and ta676[i+2] < ta676[i+1]

def start(sl, tp, action):
    today=dttime.date.today()
    
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
    #macd, signal, macd_ret = ta.MACD(price)
    #macd = signal - macd_ret
    rsi_ret = ta.RSI(price)
    ##删除NaN所在的行
    rsi_ret.dropna(axis=0, how='any', inplace=True)
    macd.dropna(axis=0, how='any', inplace=True)

    l = 0
    w = 0
    for i in range(prd-6):
        if i in rsi_ret and i in macd:
            hour = ret.real_volume[i+2].hour 
            if ver0_sell(ta_ema_12, ta_ema_676, i) == True and hour > 11 and hour < 23:
                print("action time" + str(ret.real_volume[i+3]))
                r = predict_loop(ret.time[i+3], "sell", sl, tp)       
                if r == 1:
                    w += 1
                if r == -1:
                    l += 1
            if ver0_buy(ta_ema_12, ta_ema_676, i) == True and hour > 11 and hour < 23:
                print("action time" + str(ret.real_volume[i+3]))
                #print(ret.real_volume[i+4])
                r = predict_loop(ret.time[i+3], "buy", sl, tp)       
                if r == 1:
                    w += 1
                if r == -1:
                    l += 1

    print("sl " + str(sl))
    print("tp" + str(tp))
    print("lost " + str(l), flush=True)
    print("win " + str(w), flush=True)
    rate = w/(l+w)
    print("win rate " + str(rate))
    exp = rate*(tp-4) - (1-rate)*(sl+4)
    print("exp " + str(exp))
    tt = exp*(w+l)*0.01
    print("total get" + str(tt), flush=True)
    return exp, rate, tt


timezone = pytz.timezone("Etc/UTC")
dt_from = datetime(2021, 3, 10, 16, 15, tzinfo=timezone)
ticks = mt5.copy_ticks_from(zhonglei, dt_from, 2000000000, mt5.COPY_TICKS_ALL)
search_map = {}
tf = pd.DataFrame(ticks)
tf['time']=pd.to_datetime(tf['time'], unit='s')

#print(tf.time[0], flush=True)
for itr in range(len(tf)):
    search_map[tf.time_msc[itr]] = itr

def predict(timesp, action, stop_loss, take_profit):
    start = search_map[timesp]
    price_buy = tf.ask[start]
    price_sell = tf.bid[start]
    sell_time = tf.time[start]
    if action == "sell":
        print("sell price" + str(price_sell))
    if action == "buy":
        print("buy price" + str(price_buy))

    if action == "buy":
        #print(price_buy)
        for index in range(start, len(tf.bid)):
            #止损
            if tf.bid[index] < price_buy - stop_loss:
                print("buy lost")
                print("done time" + str(tf.time[index]))
                print("done price" + str(tf.bid[index]))
                return -1
            #止盈
            if tf.bid[index] > price_buy + take_profit:
                print("buy win")
                print("done time" + str(tf.time[index]))
                print("done price" + str(tf.bid[index]))
                return 1
    
    if action == "sell":
        for index in range(start, len(tf.bid)):
            #止损
            if tf.ask[index] > price_sell + stop_loss:
                print("sell lost")
                print("done time" + str(tf.time[index]))
                print("done price" + str(tf.ask[index]))
                return -1
            #止盈
            if  tf.ask[index] < price_sell - take_profit:
                print("sell win")
                print("done time" + str(tf.time[index]))
                print("done price" + str(tf.ask[index]))
                return 1

def predict_loop(i, action, sl, tp):
    i = i*1000
    while True:
        if i in search_map:
            r = predict(i, action, sl/100000, tp/100000)
            print("\n")
            return r
        else:
            i = i + 1


def find_best_parameter():
    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for tp in range(40, 400, 10):
            for sl in range(40, 400, 10):
                exp, rate, tt = start(sl, tp, "sell")
                spamwriter.writerow(["zhiying", tp])
                spamwriter.writerow(["zhisun", sl])
                spamwriter.writerow(["shenglv",rate])
                spamwriter.writerow(["exp", exp])
                spamwriter.writerow(["total", tt])
                spamwriter.writerow([" ", " "])

find_best_parameter()
#start(100, 180, "sell")
#start(170, 270, "sell")
