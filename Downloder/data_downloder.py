import urllib.request as request
from Downloder import config
from string import Template

def get_url(stock_name):
    t = Template(config.URL)
    url = t.substitute(stock_name=stock_name)
    return url

def _single_stock_download_data(stock):
    url = get_url(stock)
    with request.urlopen(url) as response:
        data = response.read()    
    with open(f'{config.OUT_DATA_DIR}/RawData/{stock}.csv', 'w') as f:
        f.write(data.decode('utf-8'))

def download_data(stocks):
    for stock in stocks:
        _single_stock_download_data(stock)

if __name__ == "__main__":
    download_data(config.LIST_OF_STOCKS)
