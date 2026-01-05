# Data API Descriptions
## Routes
- Root: `/api`
- Futures: `/api/futures`
- Options: `/api/options`
- Stocks: `/api/stocks`
  
## Requests & Responses
* All request methods are **POST**.

**Common Request Body Formats:**  

Request:  
```json
{
    "token": "<Your Token>",
    "api": "<API Name>",
    "param": {
        ..."parameter": "value"
    },
    "want": [...(Wanted Fields to Get)]
}
```
* **About Wanted Fields**: 
  `Default` fields (*"Default: Y"*) will always be returned if *`want`* is empty;   
  On the other hand, only listed fields will be returned.
  
Response:  
```json
{
    "ok": "< true | false >",
    "msg": "[Error Information]",
    "fields": [...(Field Names)],
    "count": (number of response data lines),
    "data": [
        [...(Data)]...
    ]
}
```
* **About returned data**:  
  The returned JSON message contains 3 important fields named `"fields"`, `"count"` and `"data"`.  
  Field `"data"` is an *array* contains several *array* items;  
  Field `"fields"` is and *array* of *string* which describes the arrangement of field arrays in `"data"`. For example, if `"fields"` = `["a","b","c"]`, the `"data"` will have 3 array items corresponding the `"fields"`, like `[[...], [...], [...]]`;  
  Field `"count"` is a number describing the length of items in `"data"`. For example, if `"data"` = `[['a'], [1], [true]]`, `"count"` equals to `1`.


----------------------
### **Futures**
**0. Trading Calendar** 

Name: `"calendar"`;  

Parameters:  
| Name | Type | Required? | Description | Comment |
|:----:|:----:|:---------:|:------------|:--------|
|`"exchange"`|string|N|Exchange Code ("CFFEX","CZCE","DCE","GFEX","INE","SHFE")(in **upper case**)||
|`"begin"`|string|N|Beginning Date|In 'YYYY-MM-DD'|
|`"end"`|string|N|Ending Date|In 'YYYY-MM-DD'|

Fields:  
| Name | Type | Default? | Description | Comment |
|:----:|:----:|:--------:|:------------|:--------|
|`"exchange"`|string|Y|Exchange Code ("CFFEX","CZCE","DCE","GFEX","INE","SHFE")||
|`"date"`|string|Y|Nature Day|In 'YYYY-MM-DD'|
|`"open"`|bool|Y|Is Trading Day or Not||
|`"last_open"`|string|Y|Last Trading Day|In 'YYYY-MM-DD'|

**Example**  
* Request: 
  * URI: https://data.tabxx.net/api/futures
  * Method: POST
  * Body: 
    ```json
    {
      "api": "calendar",
      "token": "xxx",
      "param": {
        "exchange": "DCE"
      },
      "want": []
    }
    ```
  * Response:  
    ```json
    {
      "ok": true,
      "msg": "success",
      "fields": ["exchange", "date", "open", "last_open"],
      "count": 1,
      "data": [
        ["DCE"], ["2025-10-01"], [false], ["2025-09-30"]
      ]
    }
    ```
----------------
**1. Contract Information**  

Name: `"info"`;  

Parameters:  
| Name | Type | Required? | Description | Comment |
|:----:|:----:|:---------:|:------------|:--------|
|`"code"`|string|N|Contract Code (like "FG2601", formatted in XX+YYMM, in **upper case**)|The server returns **all** contracts **if not provided**.|
|`"object"`|string|N|Object Code (like "AG""AU""JM", in **upper case**)|Used as a **filter** condition.|
|`"exchange"`|string|N|Exchange Code ("CFFEX","CZCE","DCE","GFEX","INE","SHFE")(in **upper case**)|Used as a **filter** condition|

Fields:  
| Name | Type | Default? | Description | Comment |
|:----:|:----:|:--------:|:------------|:--------|
|`"name"`|string|Y|Contract Name|Like "玻璃2601"|
|`"code"`|string|Y|Contract Code|Like "FG2601", formatted in XX+YYMM|
|`"object"`|string|Y|Object Code|Like "FG", in upper case|
|`"exchange"`|string|Y|Exchange Code|Like "CZCE", in upper case|
|`"unit"`|string|Y|Trading Unit||
|`"quotation_unit"`|string|Y|Quotation Unit|In CNY|
|`"minimum_variation"`|number|Y|Minimum Price Variation|In CNY|
|`"minimum_margin"`|number|Y|Minimum Margin Rate|Percentage|
|`"limit_band"`|number|Y|Maximum Rising/Falling Rate|Percentage|
|`"last_trading_day"`|string|Y|The Last Trading Day|In 'YYYY-MM-DD'|
|`"delivery_date"`|string|N|The Delivery Date|In 'YYYY-MM-DD'|
|`"listing_date"`|string|N|The Listing Date|In 'YYYY-MM-DD'|

**Example**  
* Request: 
  * URI: https://data.tabxx.net/api/futures
  * Method: POST
  * Body: 
    ```json
    {
      "api": "info",
      "token": "xxx",
      "param": {
        "code": "AG2512"
      },
      "want": ["name", "object", "exchange"]
    }
    ```
  * Response:  
    ```json
    {
      "ok": true,
      "msg": "success",
      "fields": ["name", "object", "exchange"],
      "count": 1,
      "data": [
        ["沪银2512"], ["AG"], ["SHFE"]
      ]
    }
    ```
----------------
### 2. History Market Data (0.5s Snapshot)

Name: `"history_tick"`;  

Parameters:  
| Name | Type | Required? | Description | Comment |
|:----:|:----:|:---------:|:------------|:--------|
|`"code"`|string|Y|Contract Code (like "FG2601", formatted in XX+YYMM, in **upper case**)||
|`"begin"`|string|Y|The first trading day to query|In 'YYYY-MM-DD'|
|`"end"`|string|N|The last trading day to query|In 'YYYY-MM-DD'. Returns the history data in trading day `"begin"` if this option is not set.|

Fields:  

| Name | Type | Default? | Description | Comment |
|:----:|:----:|:--------:|:------------|:--------|
|`"date"`|string|Y|Date|In 'YYYY-MM-DD'|
|`"time"`|string|Y|Update Time|In 'HH:mm:SS'|
|`"ms"`|number|Y|Millisecond of Update Time||
|`"last_price"`|number|Y|The Last Price||
|`"volume"`|number|Y|Volume Traded||
|`"turnover"`|number|Y|Amount of Money||
|`"open_interest"`|number|Y|Open Interest (Total Position)||
|`"average"`|number|Y|Last Average Price of The Trading Day||
|`"bid_price1"`|number|Y|||
|`"bid_volume1"`|number|Y|||
|`"ask_price1"`|number|Y|||
|`"ask_volume1"`|number|Y|||

**Example**  
* Request: 
  * URI: https://data.tabxx.net/api/futures
  * Method: POST
  * Body: 
    ```json
    {
      "api": "history_tick",
      "token": "xxx",
      "param": {
        "code": "AG2512",
        "begin": "2025-10-31"
      },
      "want": []
    }
    ```
  * Response (Not Real Data):  
    ```json
    {
      "ok": true,
      "msg": "success",
      "fields": ["date", "time", "ms", "last_price", "volume", "turnover", "open_interest", "average", "bid_price1", "bid_volume1", "ask_price1", "ask_volume1"],
      "count": 123456,
      "data": [
        ["2025-10-31", "2025-10-31", ...], // date
        ["21:00:00", "21:00:00", ...], // time
        [0, 500, ...], // ms
        [11245, 11245, ...], // last_price
        [100, 123, ...], // volume
        [16867500, 37614525, ...], // turnover
        [279000, 279001, ...], // open_interest
        [11245.00, 11245.00, ...], // average
        [11245, 11245, ...], // bid_price1
        [985, 900, ...], // bid_volume1
        [11246, 11246, ...], // ask_price1
        [211, 300, ...] // ask_volume1
      ]
    }
    ```
---------------------
### 3. History Market Data (Candle Line)

Name: `"history"`;  

Parameters:  
| Name | Type | Required? | Description | Comment |
|:----:|:----:|:---------:|:------------|:--------|
|`"code"`|string|Y|Contract Code (like "FG2601", formatted in XX+YYMM, in **upper case**)||
|`"Period"`|string|Y|Period of Each Candle Line|Options Including: `"1s"`/`"1min"`/`"1h"`/`"1d"`|
|`"begin"`|string|Y|The first trading day to query|In 'YYYY-MM-DD'|
|`"end"`|string|N|The last trading day to query|In 'YYYY-MM-DD'. Returns the history data in trading day `"begin"` if this option is not set.|

Fields:  

| Name | Type | Default? | Description | Comment |
|:----:|:----:|:--------:|:------------|:--------|
|`"trading_day"`|string|Y|Trading Day|In 'YYYY-MM-DD'|
|`"time"`|string|Y|End Time of The Period|In 'HH:mm:SS'|
|`"volume"`|number|Y|Volume Traded||
|`"turnover"`|number|Y|Amount of Money||
|`"open_interest"`|number|Y|Open Interest (Total Position)||
|`"average"`|number|Y|Last Average Price of The Trading Day||
|`"open"`|number|Y|Open Price||
|`"close"`|number|Y|Close Price||
|`"high"`|number|Y|Highest Price||
|`"low"`|number|Y|Lowest Price||

**Example**  
* Request: 
  * URI: https://data.tabxx.net/api/futures
  * Method: POST
  * Body: 
    ```json
    {
      "api": "history",
      "token": "xxx",
      "param": {
        "code": "AG2512",
        "period": "1min",
        "begin": "2025-10-31"
      },
      "want": []
    }
    ```
  * Response (Not Real Data):  
    ```json
    {
      "ok": true,
      "msg": "success",
      "fields": ["trading_day", "time", "volume", "turnover", "open_interest",	"average", "open", "close", "high", "low"],
      "count": 1234,
      "data": [
        ["2025-10-31", "2025-10-31", ...], // trading_day
        ["21:01:00", "21:02:00", ...], // time
        [100, 123, ...], // volume
        [16867500, 37614525, ...], // turnover
        [279000, 279001, ...], // open_interest
        [11245.00, 11245.00, ...], // average
        [11240, 11245, ...], // open
        [11245, 11244, ...], // close
        [11251, 11246, ...], // high
        [11239, 11240, ...] // low
      ]
    }
    ```
    
----------------
### 4. History Broker Position


----------------
### 5. History Warehouse Data 


----------------
### 6. History Spot Commodity 


----------------
...Move