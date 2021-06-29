import csv

def get_data(data_path):
    with open(data_path) as f:
        f.readline()
        data = list(csv.reader(f))
    return data


def day_avg(row):
    if 'null' in row:
        return 'null'
    else:
        sum = 0
        for i in range(1,5):
            sum += float(row[i])
        return sum/4
    
    
def get_avg_column(dataset):
    out_data = [[row[0], day_avg(row)] for row in dataset]
    return out_data

def replace_null(dataset):
    non_null = 0
    buffer = dataset 
    for i in range(len(dataset)):
        if 'null' in dataset[i]:
            buffer[i][1] = non_null
        else:
            non_null = dataset[i][1]
    return buffer 

def data_cleaning_pipeline(data):
    out_data = get_avg_column(data)
    out_data = replace_null(out_data)
    return out_data
        