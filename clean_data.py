from Wrapper import manipulate
import os
data_directory = 'Data/'
for file in os.listdir(data_directory):
    data = manipulate.get_data(data_directory+file)
    data = manipulate.data_cleaning_pipeline(data)
    print(data)
    