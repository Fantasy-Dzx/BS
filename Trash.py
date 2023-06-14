import pandas as pd

data_Product = pd.read_csv(r"Data/new_data_Product.csv")
data_Line = pd.read_csv(r"Data/new_data_Line.csv")
data_CT = pd.read_csv(r"Data/new_data_CT.csv")

month = list(data_Product.columns.values)[5:]


data_Product = data_Product.T.to_dict('dict')
data_Line = data_Line.T.to_dict('dict')
data_CT = data_CT.T.to_dict('dict')
'''
data_Out = {
    'Plant': [],
    'Product': [],
    'Process': [],
    'Line-ID': [],
    '产品通用代号': [],
    '202301': [],
    '202302': [],
    '202303': [],
    '202304': [],
    '202305': [],
    '202306': [],
    '202307': [],
    '202308': [],
    '202309': [],
    '202310': [],
    '202311': [],
    '202312': []
}
'''
data_Out = {
    'Plant': [],
    'Product': [],
    'Process': [],
    'Line-ID': [],
    '产品通用代号': []
}
for i in range(len(month)):
    data_Out[month[i]] = []

print(data_Out)
