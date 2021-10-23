from flask import Blueprint,render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from Catalog import catalog
from plotapi import single_plot
from Stocker import stocks

_log = catalog.CataLog()
plot_client = Blueprint("plot_client", __name__, template_folder='templates')

@plot_client.route("/plot/<stock_name>/<stock_id>")
def plot(stock_name='TITAN', stock_id='TITAN.NS'):
    try:
        itc = stocks.Stock(stock_name,stock_id)
        itc.clean()
        html = single_plot._plot(itc)
        return html
    except:
        _log.fail(f"[{stock_id}]is not a valid Stock Id or it has not been downloaded. Download [{stock_id}] before plot.")
        return redirect(url_for("plot_interface"))