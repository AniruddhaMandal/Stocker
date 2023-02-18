import os
from Stocker import stocks
from Stocker import config

def stock_objs_data_downloder(stock_names_list):
    os.makedirs(config.RAW_OUT_DIR,exist_ok=True)
    os.makedirs(config.CLEAN_OUT_DIR,exist_ok=True)

    stock_obj_list = [stocks.Stock(name, name+".NS") for name in stock_names_list]
    for obj in stock_obj_list:
        obj.download()
        obj.clean()
    
    return "Download Complete!"