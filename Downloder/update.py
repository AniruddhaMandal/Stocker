import os


import os
from Downloder import data_downloder
from Downloder import config
from Wrapper import manipulate
import csv

def update_data():
    try:
        os.mkdir("Data")
        os.mkdir("Data/RawData")
        os.mkdir("Data/CleanData")

    except:
        print("Data directory already present in the current folder.")

    data_downloder.download_data(config.LIST_OF_STOCKS)

    for file in os.listdir(f'{config.OUT_DATA_DIR}/RawData'): 
        out_data = manipulate.data_cleaning_pipeline(f'{config.OUT_DATA_DIR}/RawData/{file}')
        with open(f'{config.OUT_DATA_DIR}/CleanData/{file}', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerows(out_data)