import os
from Stocker import stocks
from Stocker import config

def stock_objs_data_downloder(stock_names_list,output_type,range,interval):
    os.makedirs(config.RAW_OUT_DIR,exist_ok=True)
    os.makedirs(config.CLEAN_OUT_DIR,exist_ok=True)

    stock_obj_list = [stocks.Stock(name, name+".NS") for name in stock_names_list]
    message = ""
    for obj in stock_obj_list:
        try:
            obj.download(range=range,interval=interval)
            obj.clean(output_type=output_type)
        except:
            message +=f"Failed to download: {obj.name}\n"
    return message+"Download Complete!"