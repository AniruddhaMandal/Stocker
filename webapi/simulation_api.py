from datetime import datetime
from tracemalloc import start
from flask import request, Blueprint, render_template, redirect,url_for
import os
import numpy as np

from Catalog import catalog
from Stocker import stocks, config

logger = catalog.CataLog()

simulation_interface = Blueprint("simulation_interface",__name__,template_folder="templaces")
@simulation_interface.route("/simul",methods=['GET','POST'])
def simul_cal_interface():
    if request.method == 'GET':
        return render_template("simulation_interface.html")
    if request.method == 'POST':
        expected_column_names = ["stock_name", "start_date", "end_date", "flow_line_period", "support_line_period"]
        file = request.files['file']
        if(file.content_type != "text/csv"):
            message = "Upload a CSV file"
            return render_template("simulation_interface.html",message=message)

        column_names = byte_line_to_array(file.stream.readline())        

        # validation of data column names
        for expected_name,name in zip(expected_column_names,column_names):
            if (expected_name != name):
                message = "Not a valid file format!"
                return render_template("simulation_interface.html",message=message)
        
        stock_names = []
        start_dates = []
        end_dates = []
        flow_line_periods = []
        support_line_periods = []

        # parsing names, dates and periods for stocks from input file
        for line in file.stream:
            row = byte_line_to_array(line)
            if len(row) != 5:
                message = f"Missing element in {line}"
                return render_template("simulation_interface.html",message=message)

            stock_names.append(row[0])
            start_dates.append(row[1])
            end_dates.append(row[2])
            flow_line_periods.append(row[3])
            support_line_periods.append(row[4])

        start_dates = np.array(start_dates,dtype=np.datetime64)
        end_dates = np.array(end_dates,dtype=np.datetime64)

        for i in range(len(stock_names)):
            stock_obj = stocks.Stock(stock_names[i],stock_names[i]+".NS")
            profit_calculator(stock_obj,start_dates[i],end_dates[i],flow_line_periods[i],support_line_periods[i])
            
        
        return render_template("simulation_interface.html")

def byte_line_to_array(line):
    row = str(line,"UTF-8").replace("\n","").replace(" ","").split(",")
    return row

def profit_calculator(stock: stocks.Stock, start_date, end_date, flow_line_period,support_line_period):
    if(stock.name+".csv" not in os.listdir(config.CLEAN_OUT_DIR)):
        logger.warning(f"Data Not Present for: {stock.name}")
        logger.info(f"Downloading Data for: {stock.name}")
        if(stock.download() == -1):
            return -1
        stock.clean()
        
    stock.config()

    #logger.warning(f"{None == None}")
    i,j = date_truncate_index(start_date,end_date,stock.dates)
    logger.info(f"Start index: {i}, End index: {j}")

def date_truncate_index(start_date,end_date, datetime_array):
    i = None
    j = None 
    for c in range(len(datetime_array)):
        if ((datetime_array[c]<=start_date) and (i == None)):
            i = c
            logger.info(f"{c}")
        if((datetime_array[c]<=end_date) and (j == None)):
            j = c
            logger.info(f"{c}")
    return (i,j)