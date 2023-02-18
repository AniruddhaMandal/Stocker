import os
import csv

from Stocker import stocks

def moving_avg_all(period: int):
    present_stocks = os.listdir("Data/CleanData")
    for stock_file_name in present_stocks:
        currnet_stock_obj = stocks.Stock(stock_file_name.replace(".csv",""), stock_file_name.replace(".csv",".NS"))
        currnet_stock_obj.moving_avg(period)