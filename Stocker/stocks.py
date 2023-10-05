from lib2to3.pgen2.token import COLONEQUAL
import os
import sys
import csv
import requests
import json
from datetime import datetime
from string import Template

import numpy as np

from Stocker import config 
from Catalog import catalog

url = Template(config.URL)
user_header = config.USER_HEADER
_log = catalog.CataLog()

class Stock:
    """
        Stock Object: Encapsulates individual stocks, it's data folders
        and operations corresponding to each `Stock` object.
    
    """
    def __init__(
        self, 
        name: str,
        id: str, 
        raw_out_dir=config.RAW_OUT_DIR, 
        clean_out_dir=config.CLEAN_OUT_DIR):
        
        self.name = name
        self.id   = id
        self.source = url.substitute(stock_name=id)
        self.raw_data = f"{raw_out_dir}{self.name}.csv"        
        self.clean_data_file = f"{clean_out_dir}{self.name}.csv"
        self.dates = None
        self.value = None

    def download(self,close="adjusted",range="1y",interval="1h",period1=None,period2=None):
        """
            Downloads the data from Yahoo finance. Saves the data  to the 
            `Data/RawData` directory. 
            Parameters:
                `close`: Valid arguments are `adjusted` and `unadjusted`.
                Default is `adjusted`. If `adjusted` then downloads the 
                adjusted closed data along. It is downloaded only if 
                `interval` is day. 

                `range`: Range of the data from present current market day.
                Valid arguments are "1d", "5d", "1mo", "3mo", "6mo", "1y",
                "2y", "5y", "10y", "ytd", "max". Default value: "max".

                `interval`: Time interval between two data points. Valid
                arguments are "1m", "2m", "5m", "15m", "30m", "60m", "90m", 
                "1h", "1d", "5d", "1wk", "1mo", "3mo".

                `period1`: Start date. Default `None`. Start and End Dates 
                must be provided together. Other wise `range` would be
                provided. 

                `period2`: End date. Default "None". End should be provided
                with start. Otherwise `ranged` would be provided.

        """
        
        #max range returns data with 1 month granularity. So using periods insted. 
        if (range == "max"):
            range = None
            period1 = 0000000000
            period2 = 9999999999

        parameters = {
            "close": close,
            "range": range,
            "interval": interval,
            "period1": period1,
            "period2": period2
        }
        try: 
            response=requests.get(self.source,params=parameters,headers=user_header)
            data = json.loads(response.text)
            if (response.status_code != 200):
                error_code = data['chart']['error']['code']
                error_description = data['chart']['error']['description']
                _log.warning(f"{self.name}>>{error_code}: {error_description}")
                raise Exception("Invalid interval and range combination provided.")

            date   = [datetime.fromtimestamp(x) for x in  data['chart']['result'][0]["timestamp"]]
            high   = data['chart']['result'][0]['indicators']['quote'][0]['high']
            low    = data['chart']['result'][0]['indicators']['quote'][0]['low']
            _open  = data['chart']['result'][0]['indicators']['quote'][0]['open']
            _close = data['chart']['result'][0]['indicators']['quote'][0]['close']
            volume = data['chart']['result'][0]['indicators']['quote'][0]['volume']
            #adjusted close is not present if interval is smaller than 1 day.
            try:
                adj_close = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
            except:
                adj_close = _close
            with open(self.raw_data,'w') as f:
                try:
                    f.write("Date Time, High, Low, Open, Close, Volume, Adjusted Close\n")
                    for d,h,l,o,c,v,a in zip(date,high,low,_open,_close,volume,adj_close):
                        f.write(d.strftime("%d/%m/%Y %H:%M")+',')
                        f.write(f'{h},')
                        f.write(f'{l},')
                        f.write(f'{o},')
                        f.write(f'{c},')
                        f.write(f'{v},')
                        f.write(f'{a}\n')
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    _log.fail(f"{fname} line:{exc_tb.tb_lineno} {exc_type}:{exc_obj}")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _log.fail(f"{fname} line:{exc_tb.tb_lineno} {exc_type}:{exc_obj}")
            
            return -1
            
    def clean(self,output_type="high"):
        """
            Creates a consised version of the raw data. Outputs the 
            data columns as per request of the output data type. 
            Fills the gap if present. 
            Arguments:
            `output_type`: Type of data column. Valid arguments are 
            'avg', 'close', 'open', 'high', 'low', 'adj_close'.
            `volume`: If true includes the volume column. 
            Valid arguments are `True` or `False`.
        """
        if f'{self.name}.csv' not in os.listdir(config.RAW_OUT_DIR):
            if(self.download() == -1):
                return -1
        with open(self.raw_data, 'r') as f:
            # removing the column names first.
            column_names = f.readline()
            data = csv.reader(f)
            data = list(data)
            data.reverse()
            if output_type == "avg":
                # column might contail missing data as `''`(empty string)
                column = self._get_avg_column(data[1:])
            if output_type == 'high':
                column = [row[1] for row in data]
            if output_type == 'low':
                column = [row[2] for row in data]
            if output_type == 'open':
                column = [row[3] for row in data]
            if output_type == 'close':
                column = [row[4] for row in data]
            if output_type == "volume":
                column = [row[5] for row in data]
            if output_type == 'adj_close':
                column = [row[6] for row in data]
            dates = [row[0] for row in data]

        self._replace_null(column)
        with open(self.clean_data_file, 'w', newline='') as f:
            f.write(f"Date Time, {output_type.capitalize()}\n")
            for d,c in zip(dates,column):
                f.write(f"{d},{c}\n")

    def config(self):
        try:
            data = list(csv.reader(open(self.clean_data_file,'r')))
            self.dates = np.array([row[0] for row in data], dtype=np.datetime64)
            self.value = np.array([row[1] for row in data], dtype=np.float64)

        except:
            _log.fail(f"Data not present for: {self.name}")
            return -1

    def moving_avg(self, period: int = 1, avg_type: str = "sma"):
        try:
            with open(self.clean_data_file) as clean_data_buffer:
                # removing the column names first
                column_names = clean_data_buffer.readline()
                clean_data_csv = csv.reader(clean_data_buffer)
                clean_data = list(clean_data_csv)
                dates = [i[0] for i in clean_data]
                prices = [i[1] for i in clean_data]
                for i in range(len(prices)):
                    if prices[i] == 'None':
                        print(f"none present for {i}\n")
                prices = np.array(prices,dtype=np.float64)

            os.makedirs(config.MOVING_AVG_DIR,exist_ok=True)

            # operation for simple moving average
            if( avg_type == "sma"):
                with open(config.MOVING_AVG_DIR+self.name+".csv",'w') as moving_avg_file_buffer:
                    current_avg = prices[:period].sum()/period
                    moving_avg_file_buffer.write(f"Date, {period} Period Moving Average\n")
                    for i in range(len(dates[period:])):
                        moving_avg_file_buffer.write(f"{dates[i]},{current_avg}\n")
                        try:
                            current_avg = current_avg + (prices[i+period]-prices[i])/period
                        except:
                            break

            if(avg_type == "ema"):
                with open(config.MOVING_AVG_DIR+self.name+".csv","w") as moving_avg_file_buffer:
                    ema_array = self._exp_moving_avg(np.flip(prices),period)
                    ema_array = np.flip(ema_array)
                    moving_avg_file_buffer.write(f"Date, {period} Period Exp. Moving Average\n")
                    for i in range(len(dates[period:])+1):
                        moving_avg_file_buffer.write(f"{dates[i]},{ema_array[i]}\n")

            return ""

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _log.fail(f"{fname} line:{exc_tb.tb_lineno} {exc_type}:{exc_obj}")
            return f"Data not present for {self.name} !\n"

    #---Following methods are not for users------

    # There is no such entry as 'null'. Null element would be blank. Try to fix this function.
    # In general we don't need this function. This is just a safty precousion. 
    def _day_avg(self,row):
        if '' in row:
            return ''
        else:
            sum = 0
            for i in range(1,5):
                sum += float(row[i])
            return sum/4

    def _replace_null(self, dataset):
        """
            Input: Array 
            If `None` string present in dataset 
            replaces it with the previous element
        """
        non_null = 0
        buffer = dataset 
        for i in range(len(dataset)):
            if 'None' in dataset[i]:
                buffer[i] = non_null
            else:
                non_null = dataset[i]
        return buffer 

    def _get_avg_column(self,dataset):
        out_data = [self._day_avg(row) for row in dataset]
        return out_data
    
    def _exp_moving_avg(self, array: np.array, period: int):
        smoothing_factor = 2/(period+1)
        ema_array = np.zeros(len(array)-period+1,dtype=np.float64)
        current_ema = array[:period].sum()/period
        ema_array[0] = current_ema
        for i in range(len(array)-period):
            current_ema = current_ema*(1 - smoothing_factor)+array[i+period]*smoothing_factor
            ema_array[i+1] = current_ema
        
        return ema_array