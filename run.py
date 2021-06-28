from Downloder import data_downloder
from Downloder import config
import os

try:
    os.mkdir("Data")
except:
    print("Data directory already present in the current folder.")


data_downloder.download_data(config.LIST_OF_STOCKS)
