from flask import request, Blueprint, render_template, redirect,url_for

from Stocker import stocks
from Operations import moving_avg
from Catalog import catalog

logger = catalog.CataLog()

avg_client = Blueprint("avg_client", __name__,template_folder="templates")

@avg_client.route("/moving_avg/moving_avg_single",methods=["GET"])
def moving_avg_single():
    stock_obj = stocks.Stock(name="ABB", id="ABB.NS")
    stock_obj.moving_avg(30)
    return "Pass\n"

@avg_client.route("/moving_avg/avg_all" , methods=["GET","POST"])
def moving_avg_all_api():
    if request.method == "POST":
        period = request.form["days"]
        moving_avg.moving_avg_all(int(period))
        return redirect(url_for("home"))
        
@avg_client.route("/moving_avg_url", methods=["POST"])
def moving_avg_stock_obj_list():
    requested_stock_names = request.json["stock_name"]
    period = int(request.json["text_input"])
    message = ""
    for name in requested_stock_names:
        obj = stocks.Stock(name, name+".NS")
        message += obj.moving_avg(period)
    
    return message+"Moving Average Data Preparation complete !"