from flask import Flask, render_template, request,redirect
import os
from Catalog import catalog
from flask.helpers import url_for


from Downloader import update
from webapi.add_stock import add_client
from webapi.plot_request import plot_client

_log = catalog.CataLog()

web_client = Flask(__name__)
web_client.register_blueprint(add_client)
web_client.register_blueprint(plot_client)

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

@web_client.route("/plot", methods=['GET', 'POST'])
def plot_interface():
    if request.method == 'GET':
        return render_template('select_plot.html')
    if request.method == 'POST':
        plot_stock = request.form
        print(plot_stock)
        return redirect(url_for('plot_interface')+'/'+plot_stock['stock_name']+'/'+plot_stock['stock_id'])


if __name__ == "__main__":
    web_client.run(debug=True)