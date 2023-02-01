from flask import render_template, Blueprint,request
from Downloader import update

add_client = Blueprint("add_client",__name__,template_folder='templates')

@add_client.route("/add", methods=['POST', 'GET'])
def add_stock_form():
    if request.method == 'GET':
        return render_template('/add.html')
    if request.method == 'POST':
        new_stock = request.form
        new_stock = {
            'name': new_stock['stock_name'],
            'id'  : new_stock['stock_id']
        }
        update.update_stock_json(new_stock)
        return render_template('add.html')

@add_client.route("/add_list", methods=['POST', 'GET'])
def add_stock_list():
    if request.method == 'GET':
        return render_template('/add_list.html')
    if request.method == 'POST':
        stock_list = request.form
        stock_list = stock_list['stock_list'].split(",")
        print(stock_list)
        
        for stock_name in stock_list:
            print(stock_name)
            new_stock = {
                'name': stock_name,
                'id' : stock_name+".NS"
            }
            update.update_stock_json(new_stock)
        
        return render_template('add_list.html')