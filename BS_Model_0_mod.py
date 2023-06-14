import pandas as pd
from operator import itemgetter
"""
产能利用率平均分配模式
"""

data_Product = pd.read_csv(r"Data/new_data_Product.csv")
data_Line = pd.read_csv(r"Data/new_data_Line.csv")
data_CT = pd.read_csv(r"Data/new_data_CT.csv")

month = list(data_Product.columns.values)[5:]
Line_Para = list(data_Line.columns.values)
Line_Para_SWD = []
Line_Para_POT = []
Line_Para_OEE = []
Line_Para_DT = []

for i_para in Line_Para:
    if i_para[-3:] == 'SWD':
        Line_Para_SWD.append(i_para)
    elif i_para[-3:] == 'POT':
        Line_Para_POT.append(i_para)
    elif i_para[-3:] == 'OEE':
        Line_Para_OEE.append(i_para)
    elif i_para[-2:] == 'DT':
        Line_Para_DT.append(i_para)
    else:
        continue


data_Product = data_Product.T.to_dict('dict')
data_Line = data_Line.T.to_dict('dict')
data_CT = data_CT.T.to_dict('dict')

'''
#输出数据
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
#输出数据，月份按照表中内容进行导入
data_Out = {
    'Plant': [],
    'Product': [],
    'Process': [],
    'Line_ID': [],
    '产品通用代号': []
}
for i in range(len(month)):
    data_Out[month[i]] = []

data_Out_None = {
    'Plant': [],
    'Product': [],
    'Process': [],
    'Line_ID': [],
    '产品通用代号': []
}
# 存储12个月的需求量
'''
month = ['202301', '202302', '202303', '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311', '202312']
Line_Para_SWD = ['202301-SWD', '202302-SWD', '202303-SWD', '202304-SWD', '202305-SWD', '202306-SWD', '202307-SWD', '202308-SWD', '202309-SWD', '202310-SWD', '202311-SWD', '202312-SWD']
Line_Para_POT = ['202301-POT', '202302-POT', '202303-POT', '202304-POT', '202305-POT', '202306-POT', '202307-POT', '202308-POT', '202309-POT', '202310-POT', '202311-POT', '202312-POT']
Line_Para_OEE = ['202301-OEE', '202302-OEE', '202303-OEE', '202304-OEE', '202305-OEE', '202306-OEE', '202307-OEE', '202308-OEE', '202309-OEE', '202310-OEE', '202311-OEE', '202312-OEE']
Line_Para_DT = ['202301-DT', '202302-DT', '202303-DT', '202304-DT', '202305-DT', '202306-DT', '202307-DT', '202308-DT', '202309-DT', '202310-DT', '202311-DT', '202312-DT']
'''
#记录月份的长度
len_month = len(month)

Project_month_need = [[] for _ in range(12)]
Project_need = []

Product_Eps_Final_last = ''
Product_Plant_last = ''
Product_Product_last = ''



for Product_value in data_Product.values():
    if (Product_Eps_Final_last == '') & (Product_Plant_last == ''):
        Product_Eps_Final_last = Product_value['EPS-Final']
        Product_Plant_last = Product_value['Plant']
        Product_Product_last = Product_value['Product']

    if (Product_value['EPS-Final'] == Product_Eps_Final_last) & (Product_value['Plant'] == Product_Plant_last):
        # 存入12个月的数据
        i_month = 0
        for Data_month in itemgetter(*month)(Product_value):
            Project_month_need[i_month].append(round(float(Data_month)))
            i_month += 1

    else:
        # 对该类型的的product进行计算
        # 1.通过 Product(Product)、Eps-Final((Product)) 确定 Line(CT)
        Line_Eps_final = {'Id':[], 'Plant':[], 'SWD':[], 'POT':[], 'OEE':[], 'DT':[], 'CT':[], 'Cap':[]}
        for line_id in data_CT.values():
            if (Product_Product_last == line_id['Product']) & (Product_Eps_Final_last == line_id['Key']):
                Line_Eps_final['Id'].append(line_id['Line'])
                Line_Eps_final['Plant'].append([])
                Line_Eps_final['CT'].append([])
                for Data_CT_month in itemgetter(*month)(line_id):
                    Line_Eps_final['CT'][-1].append(round(float(Data_CT_month)))
                Line_Eps_final['SWD'].append([])
                Line_Eps_final['POT'].append([])
                Line_Eps_final['OEE'].append([])
                Line_Eps_final['DT'].append([])
                Line_Eps_final['Cap'].append([])
        if len(Line_Eps_final['Id']) == 0:
            data_Out_None['Plant'].append(Product_Plant_last)
            data_Out_None['Product'].append(Product_Product_last)
            data_Out_None['Process'].append(Product_Product_last + '-Final')
            data_Out_None['Line-ID'].append('None')
            data_Out_None['产品通用代号'].append(Product_Eps_Final_last)
            print('没有找到：', Line_Eps_final['Id'], '---', Product_Plant_last,Product_Eps_Final_last)
        goon = 1
        # 2.通过 Line、Plant 找到对应的参数 Line(SWD、POT、OEE、DT)
        for line_para in data_Line.values():
            if line_para['Line'] in Line_Eps_final['Id']:
                # 将产线名称的索引找出
                index = Line_Eps_final['Id'].index(line_para['Line'])
                # 将产线的地址存入
                Line_Eps_final['Plant'][index].append(line_para['Plant'])
                # 将产线的参数传入SWD、POT、OEE、DT
                for para in itemgetter(*Line_Para_SWD)(line_para):
                    Line_Eps_final['SWD'][index].append(float(para))

                for para in itemgetter(*Line_Para_POT)(line_para):
                    Line_Eps_final['POT'][index].append(float(para))

                for para in itemgetter(*Line_Para_OEE)(line_para):
                    Line_Eps_final['OEE'][index].append(float(para))

                for para in itemgetter(*Line_Para_DT)(line_para):
                    Line_Eps_final['DT'][index].append(float(para))

        if len(Line_Eps_final['SWD']) == 0:
            print('没有找到对应产线参数：',Line_Eps_final['Id'],'---',Product_Plant_last)
            goon = 0
        else:
            for i in range(len(Line_Eps_final['Id'])):
                if len(Line_Eps_final['SWD'][i]) == 0:
                    print('没有找到对应产线参数：', Line_Eps_final['Id'], '---', Product_Plant_last)
                    goon = 0


        # 3.计算当前产线的最大产能（or理论产能）
        # 产能计算：
        # 单个生产线的产量 = 【（工作天数day-停机天数day）*工作时长h*开动率】h/节拍s   ---   [ (SWD - DT) * POT * OEE ] / CT
        if goon == 1:
            for cap_cal_num in range(len(Line_Eps_final['Id'])):
                for cap_cal_month in range(12):
                    # print(cap_cal_num,len(Line_Eps_final['SWD']),len(Line_Eps_final['SWD'][cap_cal_num]))
                    cap_cal_SWD = Line_Eps_final['SWD'][cap_cal_num][cap_cal_month]
                    cap_cal_DT = Line_Eps_final['DT'][cap_cal_num][cap_cal_month]
                    cap_cal_POT = Line_Eps_final['POT'][cap_cal_num][cap_cal_month]
                    cap_cal_OEE = Line_Eps_final['OEE'][cap_cal_num][cap_cal_month]
                    cap_cal_CT = Line_Eps_final['CT'][cap_cal_num][cap_cal_month]
                    if cap_cal_CT == 0:
                        cap_cal_res = 0
                    else:
                        cap_cal_res = ((cap_cal_SWD - cap_cal_DT) * cap_cal_POT * cap_cal_OEE) * 3600 / cap_cal_CT
                    Line_Eps_final['Cap'][cap_cal_num].append(int(cap_cal_res))
                # 进行判断与模式分配
                if cap_cal_num == (len(Line_Eps_final['Id']) - 1):
                    # 产能排序(暂定)
                    # 产能是否满足要求
                    for cap_cal_month in range(len_month):
                        # 每条产线当月的产能比例
                        # 总产能
                        Line_Cap_All = 0
                        for line_no in range(len(Line_Eps_final['Id'])):
                            Line_Cap_All = Line_Cap_All + Line_Eps_final['Cap'][line_no][cap_cal_month]

                        if sum(Project_month_need[cap_cal_month]) <= Line_Cap_All:
                            for line_no in range(len(Line_Eps_final['Id'])):
                                vindex = [index for (index, value) in enumerate(data_Out['Line-ID']) if ((value == Line_Eps_final['Id'][line_no]) & (data_Out['Plant'][index] == Line_Eps_final['Plant'][line_no]) & (data_Out['产品通用代号'][index] == Product_Eps_Final_last))]
                                if len(vindex) == 0:
                                    data_Out['Plant'].append(Line_Eps_final['Plant'][line_no])
                                    data_Out['Product'].append(Product_Product_last)
                                    data_Out['Process'].append(Product_Product_last+'-Final')
                                    data_Out['Line-ID'].append(Line_Eps_final['Id'][line_no])
                                    data_Out['产品通用代号'].append(Product_Eps_Final_last)

                                    for temp_month0 in range(len_month):
                                        temp_month_str0 = month[temp_month0]
                                        data_Out[temp_month_str0].append(0)
                                    temp_month_str = month[cap_cal_month]
                                    '''
                                    for temp_month0 in range(len_month):
                                        temp_month_str0 = str(202301 + temp_month0)
                                        data_Out[temp_month_str0].append(0)
                                    temp_month_str = str(202301+cap_cal_month)
                                    '''
                                    data_Out[temp_month_str][-1] = round(sum(Project_month_need[cap_cal_month]) * (Line_Eps_final['Cap'][line_no][cap_cal_month] / Line_Cap_All))
                                    # data_Out[temp_month_str][-1] = round(Line_Eps_final['Cap'][line_no][cap_cal_month] * (Line_Eps_final['Cap'][line_no][cap_cal_month]/Line_Cap_All))
                                else:
                                    temp_month_str = month[cap_cal_month]
                                    #temp_month_str = str(202301 + cap_cal_month)
                                    data_Out[temp_month_str][vindex[0]] = round(sum(Project_month_need[cap_cal_month]) * (Line_Eps_final['Cap'][line_no][cap_cal_month]/Line_Cap_All))
                            print('可生产')
                        else:
                            print('-----------------------------------------------不可生产', Product_Eps_Final_last,Line_Eps_final['Id'], '产能：', Line_Eps_final['Cap'][0][cap_cal_month], '需求：',Project_month_need[cap_cal_month])

        Product_Eps_Final_last = Product_value['EPS-Final']
        Product_Plant_last = Product_value['Plant']
        Product_Product_last = Product_value['Product']
        Project_month_need = [[] for _ in range(12)]
        i_month = 0
        for Data_month in itemgetter(*month)(Product_value):
            Project_month_need[i_month].append(round(float(Data_month)))
            i_month += 1
print(data_Out)
df = pd.DataFrame(data_Out)
outputpath = 'result_test_Model_0.csv'
df.to_csv(outputpath, sep=',', index=False, header=True)
print(df)
if __name__ == '__main__':
    print('PyCharm')
"""
            Product_value[
        '202301', '202302', '202303', '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311', '202312']:
"""