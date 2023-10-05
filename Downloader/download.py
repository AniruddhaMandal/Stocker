import os
import sys
from Catalog import catalog
from Stocker import stocks
from Stocker import config

_log = catalog.CataLog()

def stock_objs_data_downloder(stock_names_list,output_type,range,interval):
    os.makedirs(config.RAW_OUT_DIR,exist_ok=True)
    os.makedirs(config.CLEAN_OUT_DIR,exist_ok=True)

    stock_obj_list = [stocks.Stock(name, name+".NS") for name in stock_names_list]
    message = ""
    for obj in stock_obj_list:
        try:
            obj.download(range=range,interval=interval)
            obj.clean(output_type=output_type)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            _log.fail(f"{fname} line:{exc_tb.tb_lineno} {exc_type}:{exc_obj}")
            message +=f"Failed to download: {obj.name}\n"
    return message+"Download Complete!"