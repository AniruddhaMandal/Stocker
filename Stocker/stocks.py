import os
import csv
from urllib import request
from string import Template

import numpy as np

from Stocker import config 
from Catalog import catalog

url = Template(config.URL)
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

    def download(self):
        with request.urlopen(self.source) as response:
            data = response.read()
        with open(self.raw_data,'w') as f:
            f.write(data.decode('utf-8'))
            
    def clean(self):
        if f'{self.name}.csv' not in os.listdir(config.RAW_OUT_DIR):
            self.download()
        with open(self.raw_data, 'r') as f:
            data = csv.reader(f)
            data = list(data)
            data = self._get_avg_column(data[1:])
            data = self._replace_null(data)
            data.reverse()
        with open(self.clean_data_file, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerows(data)

    def config(self):
        data = list(csv.reader(open(self.clean_data_file,'r')))
        self.dates = np.array([row[0] for row in data], dtype=np.datetime64)
        self.value = np.array([row[1] for row in data], dtype=np.float64)

    def moving_avg(self, period: int, avg_type: str = "sma"):
        try:
            with open(self.clean_data_file) as clean_data_buffer:
                clean_data_csv = csv.reader(clean_data_buffer)
                clean_data = list(clean_data_csv)
                dates = [i[0] for i in clean_data]
                dates.reverse()
                prices = np.array([i[1] for i in clean_data],dtype=np.float64)
                prices = np.flip(prices)

            os.makedirs(config.MOVING_AVG_DIR,exist_ok=True)

            # operation for simple moving average
            if( avg_type == "sma"):
                with open(config.MOVING_AVG_DIR+self.name+".csv",'w') as moving_avg_file_buffer:
                    current_avg = prices[:period].sum()/period
                    moving_avg_file_buffer.write(f"Date, {period} Day Moving Average\n")
                    for i in range(len(dates[period:])):
                        moving_avg_file_buffer.write(f"{dates[i+period]},{current_avg}\n")
                        try:
                            current_avg = current_avg + (prices[i+period]-prices[i])/period
                        except:
                            break

            if(avg_type == "ema"):
                smoothing_factor = 2/(period+1)
                with open(config.MOVING_AVG_DIR+self.name+".csv","w") as moving_avg_file_buffer:
                    current_ema = prices[:period].sum()/period
                    moving_avg_file_buffer.write(f"Date, {period} Day Exp. Moving Average\n")
                    for i in range(len(dates[period:])):
                        moving_avg_file_buffer.write(f"{dates[i+period]},{current_ema}\n")
                        try:
                            current_ema = smoothing_factor*prices[i+period] + (1-smoothing_factor)*current_ema
                        except:
                            break
            return ""

        except Exception as e:
            print(e)
            return f"Data not present for {self.name} !\n"

    #---Following methods are not for users------

    def _day_avg(self,row):
        if 'null' in row:
            return 'null'
        else:
            sum = 0
            for i in range(1,5):
                sum += float(row[i])
            return sum/4

    def _replace_null(self, dataset):
        non_null = 0
        buffer = dataset 
        for i in range(len(dataset)):
            if 'null' in dataset[i]:
                buffer[i][1] = non_null
            else:
                non_null = dataset[i][1]
        return buffer 

    def _get_avg_column(self,dataset):
        out_data = [[row[0], self._day_avg(row)] for row in dataset]
        return out_data