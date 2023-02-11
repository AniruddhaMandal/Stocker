from flask import Blueprint, request, render_template

from Downloader import merge

merge_client = Blueprint("merge_client", __name__,template_folder="templates")

@merge_client.route("/merge",methods=["GET"])
def merge_database():
    if request.method == "GET":
        merge.merge_stockes()
        return  render_template('merge.html')