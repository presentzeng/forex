import MetaTrader5 as mt5 
import pandas as pd 
import time 
 
pd.set_option('display.max_columns', 500) # number of columns to be displayed 
pd.set_option('display.width', 1500)      # max table width to display 
 
# 建立与MetaTrader 5程序端的连接 
if not mt5.initialize(): 
    print("initialize() failed, error code =",mt5.last_error()) 
    quit() 
 
 
out_price = {} 
 
def deal_position(pos): 
 
 
def main(): 
    # 获取名称包含"*USD*"的交易品种的持仓列表 
    usd_positions=mt5.positions_get(symbol="EURUSD") 
    if usd_positions==None: 
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error())) 
    elif len(usd_positions)>0: 
        print("positions_get(group=\"*USD*\")={}".format(len(usd_positions))) 
        # display these positions as a table using pandas.DataFrame 
        df=pd.DataFrame(list(usd_positions),columns=usd_positions[0]._asdict().keys()) 
        df['time'] = pd.to_datetime(df['time'], unit='s') 
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True) 
        line_n = len(df) 
        for itr in range(line_n): 
            out_price[df.iloc[itr].ticket] = df.iloc[itr].sl 
        deal_position(df.iloc[itr]) 
main() 
