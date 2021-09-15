from flask import Flask, render_template, url_for
import os
from Downloder import update

web_client = Flask(__name__)

@web_client.route("/")
def home():
    try:
        stocks_list = os.listdir("Data/RawData")
        return render_template('main.html',stock_list=stocks_list)
    except:
        return render_template('update.html')

@web_client.route('/update')
def update_call():
    update.update_data()
    return "Data Downloaded/Updated"

if __name__ == "__main__":
    web_client.run(debug=True)