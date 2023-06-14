import pandas as pd
from operator import itemgetter
import numpy as np

"""
最大产出模式
"""

data_Product = pd.read_csv(r"Data/new_data_Product2.csv")
data_Line = pd.read_csv(r"Data/new_data_Line.csv")
data_CT = pd.read_csv(r"Data/new_data_CT.csv")

month = list(data_Product.columns.values)[5:]
data_Product = data_Product.T.to_dict('dict')
data_Line = data_Line.T.to_dict('dict')
data_CT = data_CT.T.to_dict('dict')

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
# 存储12个月的需求量

#month = ['202301', '202302', '202303', '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311', '202312']
Line_Para_SWD = ['202301-SWD', '202302-SWD', '202303-SWD', '202304-SWD', '202305-SWD', '202306-SWD', '202307-SWD', '202308-SWD', '202309-SWD', '202310-SWD', '202311-SWD', '202312-SWD']
Line_Para_POT = ['202301-POT', '202302-POT', '202303-POT', '202304-POT', '202305-POT', '202306-POT', '202307-POT', '202308-POT', '202309-POT', '202310-POT', '202311-POT', '202312-POT']
Line_Para_OEE = ['202301-OEE', '202302-OEE', '202303-OEE', '202304-OEE', '202305-OEE', '202306-OEE', '202307-OEE', '202308-OEE', '202309-OEE', '202310-OEE', '202311-OEE', '202312-OEE']
Line_Para_DT = ['202301-DT', '202302-DT', '202303-DT', '202304-DT', '202305-DT', '202306-DT', '202307-DT', '202308-DT', '202309-DT', '202310-DT', '202311-DT', '202312-DT']

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
                    # 产能是否满足要求
                    # 将月分从12月倒序输出（11-0）
                    for cap_cal_month in range(11,-1,-1):
                        # 找出最大产能
                        # 将每个月的产能提取出来并按照从大到小将其对应的索引给出
                        Line_month_cap = [i[cap_cal_month] for i in Line_Eps_final['Cap']]
                        MAX_index = np.argsort(Line_month_cap)
                        # 这里MAX_index的值可以对应产线的索引
                        #MAX_index = Line_Eps_final['Cap'].index(max(Line_Eps_final['Cap']))
                        all_month_need = sum(Project_month_need[cap_cal_month])
                        for line_idx in MAX_index:
                            if all_month_need <= Line_Eps_final['Cap'][MAX_index[line_idx]][cap_cal_month]:
                                vindex = [index for (index, value) in enumerate(data_Out['Line-ID']) if ((value == Line_Eps_final['Id'][MAX_index[line_idx]]) & (data_Out['Plant'][index] == Line_Eps_final['Plant'][MAX_index[line_idx]]) & (data_Out['产品通用代号'][index] == Product_Eps_Final_last))]
                                if len(vindex) == 0:
                                    data_Out['Plant'].append(Line_Eps_final['Plant'][MAX_index[line_idx]])
                                    data_Out['Product'].append(Product_Product_last)
                                    data_Out['Process'].append(Product_Product_last+'-Final')
                                    data_Out['Line-ID'].append(Line_Eps_final['Id'][MAX_index[line_idx]])
                                    data_Out['产品通用代号'].append(Product_Eps_Final_last)
                                    for temp_month0 in range(12):
                                        temp_month_str0 = str(202301 + temp_month0)
                                        data_Out[temp_month_str0].append(0)
                                    temp_month_str = str(202301+cap_cal_month)
                                    data_Out[temp_month_str][-1] = all_month_need
                                    #data_Out[temp_month_str][-1] = Line_Eps_final['Cap'][MAX_index[line_idx]][cap_cal_month]
                                else:
                                    temp_month_str = str(202301 + cap_cal_month)
                                    data_Out[temp_month_str][vindex[0]] = all_month_need
                                    #data_Out[temp_month_str][vindex[0]] = Line_Eps_final['Cap'][MAX_index[line_idx]][cap_cal_month]
                                all_month_need = 0
                                break
                            else:
                                vindex = [index for (index, value) in enumerate(data_Out['Line-ID']) if ((value == Line_Eps_final['Id'][MAX_index[line_idx]]) & (data_Out['Plant'][index] == Line_Eps_final['Plant'][MAX_index[line_idx]]) & (data_Out['产品通用代号'][index] == Product_Eps_Final_last))]
                                if len(vindex) == 0:
                                    data_Out['Plant'].append(Line_Eps_final['Plant'][MAX_index[line_idx]])
                                    data_Out['Product'].append(Product_Product_last)
                                    data_Out['Process'].append(Product_Product_last + '-Final')
                                    data_Out['Line-ID'].append(Line_Eps_final['Id'][MAX_index[line_idx]])
                                    data_Out['产品通用代号'].append(Product_Eps_Final_last)
                                    for temp_month0 in range(12):
                                        temp_month_str0 = str(202301 + temp_month0)
                                        data_Out[temp_month_str0].append(0)
                                    temp_month_str = str(202301 + cap_cal_month)
                                    data_Out[temp_month_str][-1] = Line_Eps_final['Cap'][MAX_index[line_idx]][cap_cal_month]
                                else:
                                    temp_month_str = str(202301 + cap_cal_month)
                                    data_Out[temp_month_str][vindex[0]] = Line_Eps_final['Cap'][MAX_index[line_idx]][cap_cal_month]
                                all_month_need = all_month_need - Line_Eps_final['Cap'][MAX_index[line_idx]][cap_cal_month]

                                #print('-----------------------------------------------不可生产',Product_Eps_Final_last,Line_Eps_final['Id'],'产能：', Line_Eps_final['Cap'][0][cap_cal_month],'需求：',Project_month_need[cap_cal_month])
                        if all_month_need == 0:
                            print('可生产完成')
                        else:
                            print('-------------------------------------------------需求量过多不可完成')

        Product_Eps_Final_last = Product_value['EPS-Final']
        Product_Plant_last = Product_value['Plant']
        Product_Product_last = Product_value['Product']
        Project_month_need = [[] for _ in range(12)]
        i_month = 0
        for Data_month in itemgetter(*month)(Product_value):
            Project_month_need[i_month].append(round(float(Data_month)))
            i_month += 1
#print(data_Out)
df = pd.DataFrame(data_Out)
outputpath = 'result_test_Model_1_2.csv'
df.to_csv(outputpath, sep=',', index=False, header=True)
print(df)
if __name__ == '__main__':
    print('PyCharm')
"""
            Product_value[
        '202301', '202302', '202303', '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311', '202312']:
"""