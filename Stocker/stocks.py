import numpy as np
import csv
from Stocker import config 
from string import Template
from urllib import request
url = Template(config.URL)
import os

class Stock:
    def __init__(
        self, 
        name,
        id, 
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
        with open(self.clean_data_file, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerows(data)

    def config(self):
        data = list(csv.reader(open(self.clean_data_file,'r')))
        self.dates = np.array([row[0] for row in data], dtype=np.datetime64)
        self.value = np.array([row[1] for row in data], dtype=np.float64)

    def moving_avg(self, days):
        pass
    
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