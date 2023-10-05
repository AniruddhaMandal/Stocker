from flask import Blueprint, request, render_template
from Stocker import stocks
from Catalog import catalog
from Operations import merge

logger = catalog.CataLog()
merge_client = Blueprint("merge_client", __name__,template_folder="templates")

@merge_client.route("/merge",methods=["GET"])
def merge_database():
    """
        It is a depricated function
    """
    if request.method == "GET":
        merge.merge_stockes()
        return  render_template('merge.html')

@merge_client.route("/merge_stock_list", methods=["POST"])
def merge_stock_objects():
    requested_stock_names = request.json["stock_name"] 
    message = merge.merge_stock_object_list(requested_stock_names)
    return message
