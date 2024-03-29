import os
import requests
import json

from flask import Flask, render_template, request,redirect
from flask.helpers import url_for


from Catalog import catalog
from Downloader import update
from Stocker import config
from Stocker import stocks
from webapi.add_stock import add_client
from webapi.plot_request import plot_client
from webapi.merge_api import merge_client
from webapi.avg_api import avg_client
from webapi.download_api import download_client
from webapi.simulation_api import simulation_interface

_log = catalog.CataLog()

web_client = Flask(__name__)
web_client.register_blueprint(add_client)
web_client.register_blueprint(plot_client)
web_client.register_blueprint(merge_client)
web_client.register_blueprint(avg_client)
web_client.register_blueprint(download_client)
web_client.register_blueprint(simulation_interface)

@web_client.route("/")
def home():
    try:
        stocks_list = os.listdir(config.RAW_OUT_DIR)
        return render_template('main.html',stock_list=stocks_list)
    except:
        return render_template('main.html',stock_list=" ")

@web_client.route("/update")
def update_call():
    update.update_data()
    return render_template('/update.html')

@web_client.route("/plot", methods=['GET', 'POST'])
def plot_interface():
    if request.method == 'GET':
        return render_template('select_plot.html')
    if request.method == 'POST':
        plot_stock = request.form
        return redirect(url_for('plot_interface')+'/'+plot_stock['stock_name']+'/'+plot_stock['stock_id'])

@web_client.route("/ops", methods=['GET','POST'])
def operations_interface():
    try:
        # inport names from config.json
        stock_json_buffer = open(config.SAVED_STOCK_NAMES_JSON_FILE,'r')
        stock_names_json = json.load(stock_json_buffer)['stock_list']
        stock_names_list = [i['name'] for i in stock_names_json]
        stock_json_buffer.close()
    except:
        stock_names_list = ""
        os.makedirs("Data/", exist_ok=True)
        f = open(config.SAVED_STOCK_NAMES_JSON_FILE,'w')
        stock_names = {"stock_list":[]}
        json.dump(stock_names,f)
        f.close()
    if request.method == "GET":
        return render_template("operations.html",stock_list=stock_names_list)
    
    if request.method == "POST":
        
        operation_dict = {
            "Download" : "download_stock_list",
            "Moving Average" : "moving_avg_url",
            "Merge" : "merge_stock_list"
        }
        
        responses_dictionary = {
            "stock_name": [],
            "operation": None,
            "moving_avg_type": None,
            "text_input": None,
            "output_type": "avg",
            "interval": "1d",
            "range": "1y" 
        }

        r = request.form
        for key in r.keys():
            for value in r.getlist(key):
                if key == "stock_name":
                    responses_dictionary[key].append(value)
                elif key == "operation":
                    responses_dictionary[key] = operation_dict[value]
                else:
                    responses_dictionary[key] = value


        message = requests.post(f"http://127.0.0.1:5000/{responses_dictionary['operation']}",json=responses_dictionary).text
        message = message.split("\n")
        return render_template("operations.html",stock_list=stock_names_list,message=message)

if __name__ == "__main__":
    web_client.run(debug=True)