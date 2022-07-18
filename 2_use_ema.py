
import MetaTrader5 as mt5
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import sys
import pytz
import scipy.signal as signal
import seaborn as sns
import csv
from datetime import datetime
import datetime as dttime
import matplotlib.pyplot as plt
import numpy
import talib as ta
import MetaTrader5 as mt5
import time
from datetime import datetime
import datetime as dttime
import talib as ta
import sys
import logging
glot = 0.01
gsymbol = "EURUSD"
gprofit = 5

def close_buy(symbol, lot, position_id):
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position_id,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # 发送交易请求
    result=mt5.order_send(request)
    # 检查执行结果
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)

def close_sell(symbol, lot, position_id):
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "position": position_id,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_IOC,
    }
    # 发送交易请求
    result=mt5.order_send(request)
    # 检查执行结果
    print("3. close position #{}: buy {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)

def p(data):
    print(data)
    sys.stdout.flush()
 
def get_all_data(sb):
    usd_positions=mt5.positions_get(symbol=sb)
    if usd_positions == None:
        return 0
    if len(usd_positions) == 0:
        return []
    if len(usd_positions)>0:
        df=pd.DataFrame(list(usd_positions),columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        return df

def close_buy(symbol, lot, position_id):
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position_id,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # 发送交易请求
    result=mt5.order_send(request)
    # 检查执行结果
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)

def close_sell(symbol, lot, position_id):
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "position": position_id,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_IOC,
    }
    # 发送交易请求
    result=mt5.order_send(request)
    # 检查执行结果
    print("3. close position #{}: buy {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)
def sell(symbol, op_time):
    if op_time == "daytime":
        ups = 150
        downs = 50
    if op_time == "evening":
        ups = 250
        downs = 60
    # 显示有关MetaTrader 5程序包的数据
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)
     
     
    # 准备买入请求结构
    #symbol = gsymbol
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
     
    lot = glot
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    #deviation = 0
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + downs* point,
        "tp": price - ups* point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
     
    # 发送交易请求
    result = mt5.order_send(request)
    print(result)
    # 检查执行结果
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
       # 请求词典结果并逐个元素显示
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
     
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))
    
    
    
    
def buy(symbol, op_time):
    if op_time == "daytime":
        ups = 250
        downs = 55
    if op_time == "evening":
        ups = 250
        downs = 89
    # 显示有关MetaTrader 5程序包的数据
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)
     
    # 建立与MetaTrader 5程序端的连接
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
     
    # 准备买入请求结构
    #symbol = gsymbol
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
     
    # 如果市场报价中没有此交易品种，请添加
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    
    lot = glot
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    p(price)
    p(price + ups* point)
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price -  downs* point,
        "tp": price + ups* point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
     
    # 发送交易请求
    result = mt5.order_send(request)
    # 检查执行结果
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
       # 请求词典结果并逐个元素显示
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
     
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))


def get_all_data(sb):
    usd_positions=mt5.positions_get(symbol=sb)
    if usd_positions == None:
        return 0
    if len(usd_positions) == 0:
        return []
    if len(usd_positions)>0:
        df=pd.DataFrame(list(usd_positions),columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        return df

def close_buy_all(symbol):
    df = get_all_data(symbol)
    for itr in range(len(df)):
        if df.iloc[itr].type == 0:
            close_buy(symbol, float(df.iloc[itr].volume), int(df.iloc[itr].ticket))

def close_sell_all(symbol):
    df = get_all_data(symbol)
    for itr in range(len(df)):
        if df.iloc[itr].type == 1:
            print("here")
            close_sell(symbol, float(df.iloc[itr].volume), int(df.iloc[itr].ticket))


def ver0_buy(ta12, ta676,i ):
    return ta12[i-1] > ta676[i-1] and ta12[i-2] < ta676[i-2] 

def ver0_sell(ta12, ta676,i ):
    return ta12[i-1] < ta676[i-1] and ta12[i-2] > ta676[i-2] 


def modify_sell(pos,sb,ticket,tp):
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    symbol = sb
    symbol_info = mt5.symbol_info(symbol)
    point = mt5.symbol_info(symbol).point
    lot = glot
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "sl": pos,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "position" : int(ticket),
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
     
    # 发送交易请求
    result = mt5.order_send(request)
    return result

def modify_buy(pos, sb, ticket, tp):
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
     
    symbol = sb
    symbol_info = mt5.symbol_info(symbol)
    point = mt5.symbol_info(symbol).point
    lot = glot
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "sl": pos,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "position" : int(ticket),
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    return result

def set_sl(pos, num, sb):
    num = num * 100
    symbol = sb
    symbol_info = mt5.symbol_info(symbol)
    point = mt5.symbol_info(symbol).point
    print(num*point, flush=True)
    # buy
    if int(pos.type) == 0:
        if (pos.price_current - num*point > pos.sl) or float(pos.sl) == 0.0:
            modify_buy(pos.price_current - num*point , sb, int(pos.ticket), pos.tp)
            print("buy no ok", flush=True)
        else:
            print("buy sl already ok")

    # sell
    if int(pos.type) == 1:
        if (pos.price_current + num*point < pos.sl) or float(pos.sl) == 0:
            modify_sell(pos.price_current+num*point, sb, int(pos.ticket), pos.tp)
            print("sell no ok", flush=True)
        else:
            p("sell sl already ok")


def set_sl_real(pos, sb, profit):
    global gprofit
    if gprofit < profit:
        gprofit = profit
    else:
        profit = gprofit
    symbol = sb
    symbol_info = mt5.symbol_info(symbol)
    point = mt5.symbol_info(symbol).point
    if int(pos.type) == 0:
        if (pos.price_open + profit*point > pos.sl) or float(pos.sl) == 0.0:
            modify_buy(pos.price_open + profit*point , sb, int(pos.ticket), pos.tp)
            print(pos.price_open + profit*point )
            print("original sl" + str(pos.sl))
            print("buy no ok real", flush=True)

    # sell
    if int(pos.type) == 1:
        print(pos.price_open - profit*point, flush=True)
        if (pos.price_open - profit*point < pos.sl) or float(pos.sl) == 0:
            ret = modify_sell(pos.price_open - profit*point, sb, int(pos.ticket), pos.tp)
            print(ret)
            print("sell no ok real", flush=True)


def daytime_modify(df):
    symbol="EURUSD"
    for itr in range(len(df)):
        profit =  df.iloc[itr].profit * 100
        print(profit, flush=True)
        #if profit >= 34 and profit < 55:
        #    set_sl_real(df.iloc[itr], symbol, 34) 
        if profit >= 56 and profit < 89:
            set_sl_real(df.iloc[itr], symbol, 55) 
        if profit >= 89 and profit < 144:
            set_sl_real(df.iloc[itr], symbol, 87) 
        if profit >= 144 and profit < 233:
            set_sl_real(df.iloc[itr], symbol, 142) 
        if profit >= 233 and profit < 377:
            set_sl_real(df.iloc[itr], symbol, 230) 

def evening_modify(df):
    symbol="EURUSD"
    for itr in range(len(df)):
        profit =  df.iloc[itr].profit * 100
        if profit >= 56 and profit < 89:
            set_sl_real(df.iloc[itr], symbol, 55) 
        if profit >= 89 and profit < 144:
            set_sl_real(df.iloc[itr], symbol, 87) 
        if profit >= 144 and profit < 233:
            set_sl_real(df.iloc[itr], symbol, 142) 
        if profit >= 233 and profit < 377:
            set_sl_real(df.iloc[itr], symbol, 230) 

def check_status(symbol, close_buy_flag, close_sell_flag, op_time):
    total_profit = 0
    df = get_all_data(symbol)
    if len(df) == 0:
        return 0

    if op_time == "evening":
        evening_modify(df)

    if op_time == "daytime":
        daytime_modify(df)

    #if close_buy_flag == True or close_sell_flag == True:
    #    set_sl(df.iloc[itr], (profit/2), symbol)

symbol_dic = {"EURUSD":0,"GBPUSD":0,"USDJPY":0, "AUDUSD":0, "USDCAD":0, "NZDUSD":0}
def start(symbol, tag, op_time):
    close_buy_flag = False
    close_sell_flag = False
    today=dttime.date.today()
    utc_tz = pytz.timezone('Etc/UTC')
    utc_from = datetime(2021, today.month, today.day, dttime.datetime.now().hour,  dttime.datetime.now().minute,tzinfo=utc_tz)
    prd = 4000
    rt = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, utc_from, prd)
    ret= pd.DataFrame(rt)
    # 将时间（以秒为单位）转换为日期时间格式
    ret['time']=pd.to_datetime(ret['time'], unit='s')
    price = pd.Series(ret.close)
    macd, signal, macd_ret= ta.MACD(price, fastperiod=89, slowperiod=144, signalperiod=9)
    rsi_ret = ta.RSI(price)
    ta_ema_12 = ta.EMA(price, timeperiod=12)
    ta_ema_676 = ta.EMA(price, timeperiod=776)
    #删除NaN所在的行
    rsi_ret.dropna(axis=0, how='any', inplace=True)
    macd_ret.dropna(axis=0, how='any', inplace=True)
    #if op_time == "evening":
    #prd = prd - 1

    if ver0_sell(ta_ema_12, ta_ema_676, prd) == True:
        if tag == True:
            sell(symbol, op_time)
            symbol_dic[symbol] = 90 * 2

    if ver0_buy(ta_ema_12, ta_ema_676, prd) == True:
        if tag == True:
            buy(symbol, op_time)
            symbol_dic[symbol] = 90 * 2


    #close
    #if macd[prd-1] < 0  and macd[prd-2] > 0:
    #    close_buy_all(symbol)

    #if macd[prd-1] > 0 and macd[prd-2] < 0:
    #    close_sell_all(symbol)

    #if macd_ret[prd-1] < 0 and macd_ret[prd-2] > 0:
    #    close_buy_flag = True

    #if macd_ret[prd-1] > 0 and macd_ret[prd-2] < 0:
    #    close_sell_flag = True

    #if ta_ema_12[prd-1] < ta_ema_676[prd-1] and ta_ema_12[prd-2] > ta_ema_676[prd-2]:
    #    close_buy_all(symbol)

    #if ta_ema_12[prd-1] > ta_ema_676[prd-1] and ta_ema_12[prd-2] < ta_ema_676[prd-2]:
    #    close_sell_all(symbol)

    return close_buy_flag, close_sell_flag


if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()


while True:
    hour = dttime.datetime.now().hour
    if symbol_dic["EURUSD"] > 0 :
        symbol_dic["EURUSD"] = symbol_dic["EURUSD"]  - 1
    tag = (symbol_dic["EURUSD"] == 0)

    op_time = "daytime"
    if hour > 16  and hour < 24:
        op_time = "evening"
    if hour < 6:
        op_time = "evening"
    close_buy_flag,close_sell_flag = start("EURUSD", tag, op_time)
    check_status("EURUSD", close_buy_flag, close_sell_flag, op_time)
    time.sleep(1)
