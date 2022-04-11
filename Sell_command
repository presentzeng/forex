import time 
import sys 
import MetaTrader5 as mt5 
ups = 1500 
downs = 800 
 
def sell(): 
    # 显示有关MetaTrader 5程序包的数据 
    print("MetaTrader5 package author: ", mt5.__author__) 
    print("MetaTrader5 package version: ", mt5.__version__) 
 
    # 建立与MetaTrader 5程序端的连接 
    if not mt5.initialize(): 
        print("initialize() failed, error code =",mt5.last_error()) 
        quit() 
 
    # 准备买入请求结构 
    symbol = "EURUSD" 
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
 
    lot = 0.01 
    point = mt5.symbol_info(symbol).point 
    price = mt5.symbol_info_tick(symbol).bid 
    print(price+downs*point) 
    print(price-ups*point) 
    deviation = 20 
    request = { 
        "action": mt5.TRADE_ACTION_SLTP, 
        "volume": lot, 
        "type": mt5.ORDER_TYPE_SELL, 
        #"price": price, 
        "sl": price + downs* point, 
        "tp": price - ups* point, 
        "deviation": deviation, 
        "magic": 234000, 
        "comment": "python script open", 
        "type_time": mt5.ORDER_TIME_GTC, 
        "position" :  3806495622, 
        "type_filling": mt5.ORDER_FILLING_RETURN, 
    } 
 
    # 发送交易请求 
    result = mt5.order_send(request) 
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
