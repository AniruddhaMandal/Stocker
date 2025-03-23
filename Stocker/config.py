#URL = "https://query1.finance.yahoo.com/v7/finance/download/$stock_name?period1=0000000000&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true"
URL = "https://query2.finance.yahoo.com/v8/finance/chart/$stock_name?period1=0000000000&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true"
RAW_OUT_DIR = 'Data/RawData/'
CLEAN_OUT_DIR = 'Data/CleanData/'
MOVING_AVG_DIR = 'Data/MovingAvg/'
SAVED_STOCK_NAMES_JSON_FILE = "Data/config.json"
USER_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}