from flask import request, Blueprint, render_template, redirect,url_for

from Catalog import catalog
from Stocker import stocks
from Downloader import download

logger = catalog.CataLog()
download_client = Blueprint("download_client", __name__,template_folder="templates")

@download_client.route("/download_stock_list", methods=["POST"])
def download_stock_objs_data():
    requested_stock_names = request.json["stock_name"]
    message = download.stock_objs_data_downloder(requested_stock_names)
    return message