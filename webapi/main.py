from flask import Flask, render_template, url_for
import os
from Downloader import update
from plotapi import single_plot
from Stocker import stocks
from webapi.add_stock import add_client

web_client = Flask(__name__)
web_client.register_blueprint(add_client)

@web_client.route("/")
def home():
    try:
        stocks_list = os.listdir("Data/RawData")
        return render_template('main.html',stock_list=stocks_list)
    except:
        return render_template('main.html',stock_list="No stock is available, Please Update.")

@web_client.route("/update")
def update_call():
    update.update_data()
    return render_template('/update.html')

@web_client.route("/plot")
def plot():
    itc = stocks.Stock("my_itc","ITC.NS")
    itc.clean()
    html = single_plot._plot(itc)
    return html


if __name__ == "__main__":
    web_client.run(debug=True)