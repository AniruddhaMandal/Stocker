from flask import request, Blueprint, render_template, redirect,url_for

from Catalog import catalog
from Stocker import stocks

logger = catalog.CataLog()

simulation_interface = Blueprint("simulation_interface",__name__,template_folder="templaces")
@simulation_interface.route("/simul",methods=['GET','POST'])
def simul_cal_interface():
    if request.method == 'GET':
        return render_template("simulation_interface.html")