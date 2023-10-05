import os
import pandas
from Catalog import catalog

from Stocker import config
from Stocker import stocks

logger = catalog.CataLog()

def merge_stockes():
   stock_files_list = os.listdir(config.CLEAN_OUT_DIR)
   dataframe_list = [pandas.read_csv(config.CLEAN_OUT_DIR + name) for name in stock_files_list]
   for dataframe, name in zip(dataframe_list,stock_files_list):
      dataframe.columns = ["Date", name ]

   merged_data = dataframe_list[0]
   for df in dataframe_list[1:]:
      merged_data = merged_data.merge(df,on="Date",how="outer")
   
   merged_data.to_csv("Data/Merge.csv")

def merge_stock_object_list(stock_names_list):
   message = ""
   dataframe_list = []
   for name in stock_names_list:
      try:
         df = pandas.read_csv(config.MOVING_AVG_DIR+name+".csv")
         df.columns = ["Date", name]
         dataframe_list.append(df)
      except:
         logger.fail(f"Moving Average Data for {name} is missing !")
         message += f"Moving Average Data for {name} is missing !\n"

   if len(dataframe_list) == 0:
      return message+"Failed to Merge"

   merged_data = dataframe_list[0]
   for df in dataframe_list[1:]:
      merged_data = merged_data.merge(df,on="Date",how="outer")

   merged_data.to_csv("Data/Merge.csv")
   return message+"Successfull Merge"