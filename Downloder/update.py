from Stocker import config, stocks
from Catalog import catalog
import os
import json

_log = catalog.CataLog()

def update_data():
    os.makedirs(config.CLEAN_OUT_DIR,exist_ok=True)
    os.makedirs(config.RAW_OUT_DIR,exist_ok=True)
    with open("Downloder/config.json") as f:
        stock_names = json.load(f)
    for i in stock_names['stock_list']:
        stock_object = stocks.Stock(name=i['name'], id=i['id'])
        try:
            stock_object.download()
            stock_object.clean()
        except:
            _log.fail(f"Error occured for [{i['id']}].The id ({i['id']}) for the stock {i['name']} might be wrong. Please make sure the id is correct.")