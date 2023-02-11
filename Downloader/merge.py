import os
import pandas

from Stocker import config


def merge_stockes():
   stock_files_list = os.listdir(config.CLEAN_OUT_DIR)
   dataframe_list = [pandas.read_csv(config.CLEAN_OUT_DIR + name) for name in stock_files_list]
   for dataframe, name in zip(dataframe_list,stock_files_list):
      dataframe.columns = ["Date", name ]

   merged_data = dataframe_list[0]
   for df in dataframe_list[1:]:
      merged_data = merged_data.merge(df,on="Date",how="outer")
   
   merged_data.to_csv("Data/Merge.csv")

