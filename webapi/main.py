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

_log = catalog.CataLog()

web_client = Flask(__name__)
web_client.register_blueprint(add_client)
web_client.register_blueprint(plot_client)
web_client.register_blueprint(merge_client)
web_client.register_blueprint(avg_client)

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
        stock_list = os.listdir(config.RAW_OUT_DIR)
        stock_list = [i.replace(".csv","") for i in stock_list]
    except:
        stock_list = " "
    if request.method == "GET":
        return render_template("operations.html",stock_list=stock_list)
    
    if request.method == "POST":
        operation_requested = list(request.form.keys())[-1]
        requested_stocks = request.form 
        message = requests.post(f"http://127.0.0.1:5000/{operation_requested}",json=requested_stocks).text

        message = message.split("\n")
        return render_template("operations.html",stock_list=stock_list,message=message)

if __name__ == "__main__":
    web_client.run(debug=True)