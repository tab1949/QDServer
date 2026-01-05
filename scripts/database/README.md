# About Database
This database is designed to be maintained by the project owner (tabxx),
so the ETL scripts **may be not available** for your source data. This means that you may need to adjust the scripts to build such a database. (Because the data (files) we use may in different structures)  
By the way, here is no automatic fetching scripts. All data updating is designed to be delayed.
# About Source Data

## For history data:

* Trading Calendar:  
  Assumed in CSV format with names line like: (**Order-Sensitive**)
```CSV
"exchange","cal_date","is_open","pretrade_date"
"CFFEX","20251231","1","20251230"
```

* Contract Information:  
Assumed in CSV format with names line like: (**Order-Sensitive**)   
```CSV
"code","symbol","exchange","name","fut_code","multiplier","trade_unit","per_unit","quote_unit","quote_unit_desc","d_mode_desc","list_date","delist_date","d_month","last_ddate","trade_time_desc"
"JD1907.DCE","JD1907","DCE","鸡蛋1907","JD","","吨","5","人民币元/500千克","1人民币元/500千克","实物交割","20180727","20190726","201907","20190731","上午9:00-11:30，下午13:30-15:00，以及交易所规定的其他时间"
``` 

* Futures Ticks:  
Assumed in CSV format with names line like: (**Order-Sensitive**)
```CSV
TradingDay,InstrumentID,UpdateTime,UpdateMillisec,LastPrice,Volume,BidPrice1,BidVolume1,AskPrice1,AskVolume1,AveragePrice,Turnover,OpenInterest,UpperLimitPrice,LowerLimitPrice
20240131,zn2501,20:59:00,500,20860.0,0,20065.0,1,21290.000000000004,1,0.0,0.0,36.0,22155.0,19650.0
``` 

* Futures Position Rank:  
Assumed in CSV format with names line like: (**Order-Sensitive**)
```CSV
"trading_day","symbol","broker_name","volume","volume_variation","long_position","long_variation","short_position","short_variation"
"2002-08-28","RU0211","上海中期",0,0,197,-11,0,0
``` 

* Options History (*Pending*):  
Assumed in CSV format with names line like: (**Order-Sensitive**)
```
time,current,volume,high,low,money,position,a1_p,b1_p,a1_v,b1_v,contract_code
20251105133000.5,4199.0,1.0,4199.0,4199.0,62985.0,3.0,5845.0,2672.5,1.0,1.0,AG2512C7100.XSGE
``` 
