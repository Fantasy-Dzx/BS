import numpy as np
import pandas as pd
import platgo as pg


class Sequence_Pte(pg.Problem):
    """
    创建People类，可视为并行初始条件，用于获取并行序列
    1.该并行线路中已经完成的工序
    2.该线路是否正在有工序进行
    3.该线路正在进行的工序的层级
    """
    class People:
        def __init__(self):
            self.No_over = []
            self.Busy = False
            self.Lable = []

    def __init__(self) -> None:
        self.name = "Sequence_Pte"
        self.type['single'], self.type['permutation'], self.type['large'] = [True] * 3
        self.M = 1
        # 并行数目
        self.Para = 1
        self.borders = []
        # 定义初始维度（即1-148）
        self.D = 148
        # 初始序列生成（0-147）
        seq = np.arange(0, 148).tolist()
        np.random.shuffle(seq)
        self.R = seq
        super().__init__()

    def cal_obj(self, pop: pg.Population) -> None:
        pass

    def Get_Time(self, data):
        pass

    def get_optimal(self) -> np.ndarray:
        pass

    # 修复函数:仅考虑实际工序（1-148）,输入为（0-147）
    def Get_Seq(self, seq):
        # 从csv中提取信息
        data = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence\plat-go\Data\data_new.csv",
                            usecols=['No', '工序层级', '前序No'])
        data = data.T.to_dict('dict')

        """
        分层级（D1D2D3-->D4-->D5-->D6）
        【138+139+（0-70）+140，141，142，143】
        【（71-116）】
        【144+（117-129）+145】
        【（130-137）+146+147】
        """
        seq0 = []
        # 源（138）+D0汇总（139）+D1D2D3（0-70）+D1汇总（140）+D2汇总（141）+D3汇总（142）+D1D2D3汇总（143）
        seq0.append(138)
        seq0.append(139)
        for n in range(148):
            if seq[n] in range(0, 71):
                seq0.append(seq[n])
        seq0.append(140)
        seq0.append(141)
        seq0.append(142)
        seq0.append(143)
        # D4（71-166）
        for n in range(148):
            if seq[n] in range(71, 117):
                seq0.append(seq[n])
        # D4汇总（144）+D5+D5汇总（145）
        seq0.append(144)
        for n in range(148):
            if seq[n] in range(117, 130):
                seq0.append(seq[n])
        seq0.append(145)
        # D6（130-137）+D6汇总（146）+终结（147）
        for n in range(148):
            if seq[n] in range(130, 138):
                seq0.append(seq[n])
        seq0.append(146)
        seq0.append(147)
        seq = seq0

        # 按照前序后序调整结点
        for i in range(len(data)):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                id_max = -1
                for n in range(len(L_temp)):
                    begin = seq.index(int(L_temp[n]) - 1)
                    id_max = max(id_max, begin)
                end = seq.index(i)
                temp = seq.pop(end)
                seq.insert(id_max + 1, temp)

        return seq

    # 输入并行线路参数P，生成DataFrame或者csv文件
    def Get_Csv(self, P):
        # 从csv中提取信息（No,D,Pre_No）
        data = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence\plat-go\Data\data_new.csv")
        data = data.T.to_dict('dict')

        """
        遍历每条并行线路
        按照每条线路将各个工序的先序填入
        """
        for i in range(self.Para):
            for n in P[i].No_over:
                # 如果该工序已存在先序，则跳过
                print(n,'nnnnnnnnnnnnnnnnnnnnnn')
                n = int(n)
                if data[n]['前序No'] == data[n]['前序No']:
                    continue
                elif (n >= 0) & (n <= 70):
                    idx = P[i].No_over.index(n)
                    if idx == 0:
                        continue
                    else:
                        data[n]['前序No'] = str(P[i].No_over[idx - 1] + 1)
                elif (n >= 71) & (n <= 116):
                    idx = P[i].No_over.index(n)
                    if idx == 0:
                        continue
                    temp = P[i].No_over[idx - 1]
                    if (temp < 71) | (temp > 116):
                        continue
                    else:
                        data[n]['前序No'] = str(temp + 1)
                elif (n >= 117) & (n <= 129):
                    idx = P[i].No_over.index(n)
                    if idx == 0:
                        continue
                    temp = P[i].No_over[idx - 1]
                    if (temp < 117) | (temp > 129):
                        continue
                    else:
                        data[n]['前序No'] = str(temp + 1)
                elif (n >= 130) & (n <= 137):
                    idx = P[i].No_over.index(n)
                    if idx == 0:
                        continue
                    temp = P[i].No_over[idx - 1]
                    if (temp < 130) | (temp > 137):
                        continue
                    else:
                        data[n]['前序No'] = str(temp + 1)

        # 收集各个层级的前序，用于后续查找没有先序的工序
        D1 = []
        D2 = []
        D3 = []
        D4 = []
        D5 = []
        D6 = []
        for i in range(0, 42):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                D1 = D1 + L_temp
            else:
                data[i]['前序No'] = str(140)
        for i in range(42, 55):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                D2 = D2 + L_temp
            else:
                data[i]['前序No'] = str(140)
        for i in range(55, 71):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                D3 = D3 + L_temp
            else:
                data[i]['前序No'] = str(140)
        for i in range(71, 117):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                D4 = D4 + L_temp
            else:
                data[i]['前序No'] = str(144)
        for i in range(117, 130):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                D5 = D5 + L_temp
            else:
                data[i]['前序No'] = str(145)
        for i in range(130, 138):
            # 找出该工序的已知前序
            if data[i]['前序No'] == data[i]['前序No']:  # 如果该节点有前序
                L_temp = data[i]['前序No'].split(',')
                D6 = D6 + L_temp
            else:
                data[i]['前序No'] = str(146)

        # 查找出没有先序的工序，将汇总节点加入，补全csv
        for i in range(len(data)):
            if i in range(0, 42):
                if D1.count(str(i + 1)) == 0:
                    if data[140]['前序No'] == data[140]['前序No']:
                        data[140]['前序No'] += "," + str(i + 1)
                    else:
                        data[140]['前序No'] = str(i + 1)
                    continue
            elif i in range(42, 55):
                if D2.count(str(i + 1)) == 0:
                    if data[141]['前序No'] == data[141]['前序No']:
                        data[141]['前序No'] += "," + str(i + 1)
                    else:
                        data[141]['前序No'] = str(i + 1)
                    continue
            elif i in range(55, 71):
                if D3.count(str(i + 1)) == 0:
                    if data[142]['前序No'] == data[142]['前序No']:
                        data[142]['前序No'] += "," + str(i + 1)
                    else:
                        data[142]['前序No'] = str(i + 1)
                    continue
            elif i in range(71, 117):
                if D4.count(str(i + 1)) == 0:
                    if data[144]['前序No'] == data[144]['前序No']:
                        data[144]['前序No'] += "," + str(i + 1)
                    else:
                        data[144]['前序No'] = str(i + 1)
                    continue
            elif i in range(117, 130):
                if D5.count(str(i + 1)) == 0:
                    if data[145]['前序No'] == data[145]['前序No']:
                        data[145]['前序No'] += "," + str(i + 1)
                    else:
                        data[145]['前序No'] = str(i + 1)
                    continue
            elif i in range(130, 138):
                if D6.count(str(i + 1)) == 0:
                    if data[146]['前序No'] == data[146]['前序No']:
                        data[146]['前序No'] += "," + str(i + 1)
                    else:
                        data[146]['前序No'] = str(i + 1)
                    continue

        # 手动加入：D5开始节点的先序节点--D4汇总
        data[117]['前序No'] += "," + str(145)

        # 转为dataframe
        df = pd.DataFrame(data).T
        return df

    def Get_Para(self, seq):  # 0开始的
        # 从表中取出数据,并将其转变为dict
        data0 = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence\plat-go\Data\data_new.csv",
                            usecols=['No', '工序层级', '前序No', '时间-处理时间', '工人(处理阶段)-服务表'])
        data = data0.rename(
            columns={'No': 'No', '工序层级': 'D', '前序No': 'Pre_No', '时间-处理时间': 'Time', '工人(处理阶段)-服务表': 'P_Num'}).copy()
        data.insert(data.shape[1], 'E_time', 0)
        data.insert(data.shape[1], 'Finish', False)
        data.insert(data.shape[1], 'P_ing', -1)  # 该工序是由哪个人来做的
        # 构建dict
        data = data.T.to_dict('dict')
        # 人员（并行数目）设置
        People_Num = self.Para
        P = []
        for i in range(People_Num):
            P.append(self.People())
        P[0].Lable = 'D1'
        #P[1].Lable = 'D2'
        #P[2].Lable = 'D3'
        # 开始时间设置
        T_now = 0
        # 现存运行工序,已完成工序
        pro_ing = []

        # 工序完成出列函数
        def pro_out():
            nonlocal People_Num, pro_ing, T_now, data, P
            temp = pro_ing.pop(0)
            data[temp['pc']]['Finish'] = True
            pro_peo = data[temp['pc']]['P_ing']
            P[pro_peo].Busy = False
            P[pro_peo].No_over.append(temp['pc'])
            T_now = temp['E_time']
            People_Num += 1

        # 遍历工序(前置工序在此可以不考虑)
        seq = seq.tolist()
        for pc in seq:
            if seq.index(pc) == 73:
                while len(pro_ing) != 0:
                    pro_out()
                for i in range(self.Para):
                    P[i].Lable = []

            if data[pc]['Time'] == 0:
                continue
            # 是否有前置工序，前置工序是否已经完成(有前置，前置没完成)---等待
            # 存在前置工序
            if data[pc]['Pre_No'] == data[pc]['Pre_No']:
                temp_list = data[pc]['Pre_No'].split(',')
                # 寻找前置工序中所在序列位置靠后的工序
                id_max = -1
                for i in range(len(temp_list)):
                    begin = seq.index(int(temp_list[i]) - 1)
                    id_max = max(id_max, begin)  # 该节点为seq[id_max]
                # 验证其前序是否完成，如果其前序已经完成，则该节点可以进行加工
                # 前序没完成
                while data[seq[id_max]]['Finish'] == False:
                    pro_out()
                # 前序完成
                if data[seq[id_max]]['Finish'] == True:
                    temp_P = data[seq[id_max]]['P_ing']
                    # 查看该任务的前序是谁做的，并且是否空闲
                    while (P[temp_P].Busy) | (People_Num <= 0):
                        pro_out()
                    # 该节点开始进行加工
                    # 该节点需要多少人
                    data[pc]['E_time'] = data[pc]['Time'] + T_now
                    data[pc]['P_ing'] = temp_P
                    P[temp_P].Busy = True
                    P[temp_P].Lable = data[pc]['D']
                    temp = data[pc].copy()
                    temp.update({'pc': pc})
                    pro_ing.append(temp)
                    pro_ing.sort(key=lambda stu: stu['E_time'])
                    People_Num = People_Num - 1

            # 不存在前置工序
            else:
                # 1.人够不够 2.层级上的人够不够
                # 找到层级,以及层级空闲人数
                temp_D = data[pc]['D']
                # 用于查找目前是否有符合层级条件的
                flag = 0
                count = 0
                for i in range(self.Para):
                    if ((P[i].Lable == temp_D) | (P[i].Lable == [])):
                        flag += 1

                if flag == 0:
                    # 没有合适的人进行处理
                    # 判断目前人够不够
                    while People_Num < 1:
                        pro_out()
                    for i in range(self.Para):
                        if P[i].Busy == False:
                            # print("lable1:", P[i].Lable)
                            # 加入
                            data[pc]['E_time'] = data[pc]['Time'] + T_now
                            data[pc]['P_ing'] = i
                            P[i].Busy = True
                            P[i].Lable = data[pc]['D']
                            # print("lable2:", P[i].Lable)
                            temp = data[pc].copy()
                            temp.update({'pc': pc})
                            pro_ing.append(temp)
                            pro_ing.sort(key=lambda stu: stu['E_time'])
                            People_Num = People_Num - 1
                            break
                else:
                    # 有合适的线程进行
                    while count == 0:
                        for i in range(self.Para):
                            if ((P[i].Lable == temp_D) | (P[i].Lable == [])) & (P[i].Busy == False):
                                data[pc]['E_time'] = data[pc]['Time'] + T_now
                                data[pc]['P_ing'] = i
                                P[i].Busy = True
                                P[i].Lable = data[pc]['D']
                                temp = data[pc].copy()
                                temp.update({'pc': pc})
                                pro_ing.append(temp)
                                pro_ing.sort(key=lambda stu: stu['E_time'])
                                People_Num = People_Num - 1
                                count += 1
                                break
                        if count == 0:
                            pro_out()

        # 如果遍历结束，则输出现存pro_ing里最大的E_time
        while len(pro_ing) != 0:
            pro_out()

        print(P[0].No_over)

        return P,T_now