URL = "https://query1.finance.yahoo.com/v7/finance/download/$stock_name?period1=0000000000&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true"
URL = "https://query2.finance.yahoo.com/v8/finance/chart/$stock_name"
RAW_OUT_DIR = 'Data/RawData/'
CLEAN_OUT_DIR = 'Data/CleanData/'
MOVING_AVG_DIR = 'Data/MovingAvg/'
SAVED_STOCK_NAMES_JSON_FILE = "Data/config.json"
USER_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
