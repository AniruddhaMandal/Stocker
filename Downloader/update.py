from Stocker import config, stocks
from Catalog import catalog
import os
import json

_log = catalog.CataLog()

STOCK_DATABASE_NAME_FILE = "Data/config.json"

def update_data():
    os.makedirs(config.CLEAN_OUT_DIR,exist_ok=True)
    os.makedirs(config.RAW_OUT_DIR,exist_ok=True)

    # Handeling Error: If the Data folder is newly created 
    # or the json file is deleted, then the config.json file is created. 
    if "config.json" not in os.listdir('Data/'):
        f = open(STOCK_DATABASE_NAME_FILE,'w')
        stock_names = {"stock_list":[]}
        json.dump(stock_names,f)
        f.close()

    with open(STOCK_DATABASE_NAME_FILE) as f:
        stock_names = json.load(f)
    for i in stock_names['stock_list']:
        stock_object = stocks.Stock(name=i['name'], id=i['id'])
        try:
            stock_object.download()
            stock_object.clean()
        except:
            _log.fail(f"Error occured for [{i['id']}].The id ({i['id']}) for the stock {i['name']} might be wrong. Please make sure the id is correct.")

def update_stock_json(new_stock:dict):
    try:
        with open(STOCK_DATABASE_NAME_FILE, 'r') as f:
            stock_names = json.load(f)
    except:
        # Handeling Error: If the json file gets deleted. 
        os.makedirs("Data/",exist_ok=True)
        f = open(STOCK_DATABASE_NAME_FILE,'w')
        stock_names = {"stock_list":[]}
        json.dump(stock_names,f)
        f.close()

    with open(STOCK_DATABASE_NAME_FILE, 'w') as f:
        if new_stock not in stock_names['stock_list']:
            stock_names['stock_list'].append(new_stock)
        json.dump(stock_names,f)