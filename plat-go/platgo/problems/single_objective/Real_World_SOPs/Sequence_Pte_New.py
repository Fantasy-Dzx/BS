import copy

import numpy as np
import pandas as pd
import platgo as pg


class Sequence_Pte_New(pg.Problem):
    """
    创建People类，可视为并行初始条件，用于获取并行序列
    1.该并行线路中已经完成的工序
    2.该线路是否正在有工序进行
    3.该线路正在进行的工序的层级
    """

    class Trash:
        Tout = 2
        Tin = 1
        Tdoor = 1

    class People:
        def __init__(self):
            self.No_over = []
            self.Busy = False


    def __init__(self) -> None:
        self.name = "Sequence_Pte"
        self.type['single'], self.type['permutation'], self.type['large'] = [True] * 3
        self.M = 1
        # 并行数目
        self.People_Num = 24
        self.borders = []
        # 定义初始维度（即1-148）
        self.D = 1380
        # 初始序列生成（0-147）
        seq = np.arange(0, 1380).tolist()
        np.random.shuffle(seq)
        self.R = seq
        super().__init__()

    def No_Perno(self, lit):
        # 返回垃圾箱编号
        no = lit.split('-')[0].split('T')[1]
        # 返回对应的工序
        perno = lit.split('-')[1]
        return no, perno

    def Re_No_Perno(self, number):
        T = ''
        a = number // 138 + 1
        b = number % 138 + 1
        T = 'T' + str(a) + '-' + str(b)
        return T

    def cal_obj(self, pop: pg.Population) -> None:
        pass

    def Get_Time(self, data):
        pass

    def get_optimal(self) -> np.ndarray:
        pass

    # 修复函数:仅考虑实际工序（1-148）,输入为（0-147）
    def Get_Seq(self, seq):
        seq = seq.tolist()
        # 从csv中提取信息
        data = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence2\plat-go\Data\lianyun_data_0331.csv")
        data.insert(data.shape[1], 'E_time', 0)
        data.insert(data.shape[1], 'P_ing', '')  # 该工序是由哪个人来做的
        data = data.T.to_dict('dict')

        Num_Trash = 10
        trash = []
        for i in range(Num_Trash):
            trash.append(self.Trash)
        pro_ing = []

        """
        将每个垃圾桶的先序调好
        入列法
        """
        seq0 = []  # 新列表
        i = 0
        while i < len(seq):
            if data[seq[i]]['前序约束'] == data[seq[i]]['前序约束']:
                L_temp = data[seq[i]]['前序约束'].split(',')
                # 先序工序所在位置
                idx_max = -1
                for k in L_temp:
                    k_a, k_b = self.No_Perno(k)
                    k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
                    begin_seq = seq.index(k_num)
                    idx_max = max(idx_max, begin_seq)

                if idx_max > i:
                    seq[i], seq[idx_max] = seq[idx_max], seq[i]

                else:
                    # print(len(seq), i)
                    # v = seq[i]
                    seq0.insert(seq0.index(seq[idx_max]) + 1, seq[i])
                    i = i + 1
            else:
                seq0.append(seq[i])
                i = i + 1

        seq = seq0
        i = 0
        #print(seq)
        while i < len(seq):
            if data[seq[i]]['前序约束'] == data[seq[i]]['前序约束']:
                L_temp = data[seq[i]]['前序约束'].split(',')
                # 先序工序所在位置
                for k in L_temp:
                    k_a, k_b = self.No_Perno(k)
                    k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
                    begin_seq = seq.index(k_num)
                    if begin_seq > i:
                        seq[i], seq[begin_seq] = seq[begin_seq], seq[i]
            i = i + 1

        i = 0
        while i < len(seq):
            if data[seq[i]]['前序约束'] == data[seq[i]]['前序约束']:
                L_temp = data[seq[i]]['前序约束'].split(',')
                # 先序工序所在位置
                for k in L_temp:
                    k_a, k_b = self.No_Perno(k)
                    k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
                    begin_seq = seq.index(k_num)
                    if begin_seq > i:
                        print("chucuol =--=-=-=-=--=-=-=-=-=-=-=")
            i = i + 1
        """
        ---------------------------------------------------------------------------------------------------------
        """
        """
        #1：按照工序层级进行分类
        """
        Segment = [[] for _ in range(6)]
        for i in range(len(seq)):
            # 求出所在层级
            d = data[seq[i]]['工序层级']
            Segment[int(d[-1]) - 1].append(seq[i])

        """
        #2：按照垃圾桶序号进行分类
        """
        Idx = [[] for _ in range(Num_Trash)]
        for i in range(len(seq)):
            # 求出索引
            no = data[seq[i]]['No']
            # 求出垃圾桶序号
            no = no.split('-')[0].split('T')[1]
            Idx[int(no) - 1].append(seq[i])

        for i in range(Num_Trash):
            temp = []
            for j in range(6):
                k = [x for x in Idx[i] if x in Segment[j]]
                temp = temp + k
            Idx[i] = temp

        """
        for i in range(Num_Trash):
            print(len(Idx[i]), Idx[i])
        
        # ---------------------------------------------------------------------------------------------------------
        """
        Idx0 = copy.deepcopy(Idx)
        p_num = self.People_Num
        P = []
        for i in range(self.People_Num):
            P.append(self.People())

        def pro_out():
            nonlocal p_num, pro_ing, T_now, data, P
            temp = pro_ing.pop(0)
            k_a, k_b = self.No_Perno(temp['No'])
            k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
            pro_peo = data[k_num]['P_ing'].split(',')
            # print('pro_peo:',pro_peo)
            if data[k_num]['工作区'] == data[k_num]['工作区']:
                loca = data[k_num]['工作区']
                if loca == "箱内":
                    trash[i].Tin = trash[i].Tin + int(data[k_num]['工人(处理阶段)-服务表'])
                elif loca == "箱外":
                    trash[i].Tout = trash[i].Tout + int(data[k_num]['工人(处理阶段)-服务表'])
                elif loca == "箱门":
                    trash[i].Tdoor = trash[i].Tdoor + int(data[k_num]['工人(处理阶段)-服务表'])
            for k in pro_peo:
                P[int(k)].Busy = False
                # print(int(k),'号人员',P[int(k)].Busy)
                p_num += 1
            T_now = temp['E_time']

        T_now = 0
        while ((len(Idx0[0]) > 0) | (len(Idx0[1]) > 0) | (len(Idx0[2]) > 0) | (len(Idx0[3]) > 0) | (len(Idx0[4]) > 0) \
               | (len(Idx0[5]) > 0) | (len(Idx0[6]) > 0) | (len(Idx0[7]) > 0) | (len(Idx0[8]) > 0) | (
                       len(Idx0[9]) > 0)):
            flag = 0
            for i in range(Num_Trash):
                if len(Idx0[i]) > 0:
                    temp = Idx0[i][0]
                    if p_num < int(data[temp]['工人(处理阶段)-服务表']):
                        pro_out()

                    # 1.是否有前序，以及前序对应人员约束
                    flag_precess = -1
                    if data[temp]['前序约束'] == data[temp]['前序约束']:
                        L_temp = data[temp]['前序约束'].split(',')
                        # 先序工序所在位置,id_max,对应元素Idx[i][id_max]
                        id_max = -1
                        for k in L_temp:
                            k_a, k_b = self.No_Perno(k)
                            k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
                            # print(temp,data[temp]['No'],i,k,k_a,k_b,k_num)
                            begin_seq = Idx[i].index(k_num)
                            id_max = max(id_max, begin_seq)
                        # 查找其前序所在人的位置
                        qqq = 0
                        for k1 in range(self.People_Num):
                            if P[k1].No_over.count(Idx[i][id_max]) > 0:
                                qqq += 1
                                if P[k1].Busy == False:
                                    # 可加入
                                    flag_precess = k1
                                    break
                                else:
                                    break
                        '''if qqq == 0:
                            print("错了",Idx[i][id_max])
                            #w = 1
                        else:
                            print('qqqqq:',i)'''
                    else:
                        flag_precess = 24

                    # 2.是否存在空间位置约束
                    flag_space = 0
                    if data[temp]['工作区'] == data[temp]['工作区']:
                        loca = data[temp]['工作区']
                        if (loca == "箱内") & (trash[i].Tin >= int(data[temp]['工人(处理阶段)-服务表'])):
                            flag_space += 1
                        elif (loca == "箱外") & (trash[i].Tout >= int(data[temp]['工人(处理阶段)-服务表'])):
                            flag_space += 1
                        elif (loca == "箱门") & (trash[i].Tdoor >= int(data[temp]['工人(处理阶段)-服务表'])):
                            flag_space += 1
                    else:
                        flag_space += 1

                    # 3.人员约束,返回所需人数
                    flag_people = 0
                    if p_num >= int(data[temp]['工人(处理阶段)-服务表']):
                        flag_people = int(data[temp]['工人(处理阶段)-服务表'])

                    # 4.判断条件是否均满足
                    # print(flag_precess,flag_space,flag_people)
                    if (flag_precess >= 0) & (flag_space == 1) & (flag_people > 0):
                        # 统计空闲人数
                        temp_pnum = 0
                        for i0 in range(self.People_Num):
                            if P[i0].Busy == False:
                                temp_pnum += 1

                        if temp_pnum >= flag_people:
                            for n in range(flag_people):
                                if flag_precess == 24:
                                    for j in range(self.People_Num):
                                        if P[j].Busy == False:
                                            if n == 0:
                                                data[temp]['P_ing'] += str(j)
                                                P[j].No_over.append(temp)
                                                P[j].Busy = True
                                            else:
                                                data[temp]['P_ing'] = data[temp]['P_ing'] + "," + str(j)
                                                P[j].No_over.append(temp)
                                                P[j].Busy = True
                                                # print(j,'号人员',P[j].Busy)
                                            break
                                else:
                                    if n == 0:
                                        data[temp]['P_ing'] += str(flag_precess)
                                        P[flag_precess].No_over.append(temp)
                                        P[flag_precess].Busy = True
                                        # print(flag_precess, '号人员', P[j].Busy)
                                    else:
                                        for j in range(self.People_Num):
                                            if P[j].Busy == False:
                                                P[j].No_over.append(temp)
                                                P[j].Busy = True
                                                # print(j, '号人员', P[j].Busy)
                                                data[temp]['P_ing'] = data[temp]['P_ing'] + "," + str(j)
                                                break
                            # data[temp]['E_time'] = T_now + data[temp]['时间-处理时间']
                            # pro_ing.append(data[temp])
                            # print(Idx0[i][0])
                            # Idx0[i].pop(0)
                            # p_num -= 1
                            if data[temp]['工作区'] == data[temp]['工作区']:
                                loca = data[temp]['工作区']
                                if loca == "箱内":
                                    trash[i].Tin = trash[i].Tin - int(data[temp]['工人(处理阶段)-服务表'])
                                elif loca == "箱外":
                                    trash[i].Tout = trash[i].Tout - int(data[temp]['工人(处理阶段)-服务表'])
                                elif loca == "箱门":
                                    trash[i].Tdoor = trash[i].Tdoor - int(data[temp]['工人(处理阶段)-服务表'])
                            data[temp]['E_time'] = T_now + data[temp]['时间-处理时间']
                            pro_ing.append(data[temp])
                            Idx0[i].pop(0)
                            flag += 1
                            pro_ing.sort(key=lambda stu: stu['E_time'])
                        else:
                            continue
                else:
                    continue
            if flag == 0:
                num = 0
                for l in range(self.People_Num):
                    if P[l].Busy == True:
                        num += 1
                # print('正在进行的工序数：',len(pro_ing),',正在忙的人：',num)
                if len(pro_ing) == 0:
                    print("len(pro_ing) == 0")
                    for o in range(10):
                        print(Idx0[o])
                    break
                else:
                    pro_out()
        """rs = 0
        for i in range(People_Num):
            print(i,len(P[i].No_over),P[i].No_over)
            rs = rs + len(P[i].No_over)

        print(rs, len(pro_ing), pro_ing)"""

        """
        ----------------------------------------------------------------------------------------------------------------------------------
        转csv
        """
        """
        遍历每条并行线路
        按照每条线路将各个工序的先序填入
        """
        data0 = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence2\plat-go\Data\lianyun_data_0331.csv")
        data0 = data0.T.to_dict('dict')

        temp_seq = np.arange(0, 1380).tolist()
        for i in range(self.People_Num):
            for n in P[i].No_over:
                n = int(n)
                idx = P[i].No_over.index(n)
                if idx == 0:
                    continue
                else:
                    if temp_seq.count(int(P[i].No_over[idx - 1])) > 0:
                        temp_seq.remove(int(P[i].No_over[idx - 1]))
                    if data0[n]['前序No'] == data0[n]['前序No']:
                        data0[n]['前序No'] = data0[n]['前序No'] + ',' + str(P[i].No_over[idx - 1])
                    else:
                        data0[n]['前序No'] = str(P[i].No_over[idx - 1])

        for i in range(len(temp_seq)):
            if data0[1382]['前序No'] == data0[1382]['前序No']:
                data0[1382]['前序No'] = data0[1382]['前序No'] + ',' + str(temp_seq[i])
            else:
                data0[1382]['前序No'] = str(temp_seq[i])

        for i in range(1380):
            if data0[i]['前序No'] == data0[i]['前序No']:
                temp0 = data0[i]['前序No'].split(',')
                temp1 = []
                for j in temp0:
                    if len(temp1) == 0:
                        temp1 = self.Re_No_Perno(int(j))
                    else:
                        temp1 = temp1 + ',' + self.Re_No_Perno(int(j))
                data0[i]['前序No'] = temp1
            else:
                data0[i]['前序No'] = 'O-2'

        temp0 = data0[1382]['前序No'].split(',')
        temp1 = []
        for j in temp0:
            if len(temp1) == 0:
                temp1 = self.Re_No_Perno(int(j))
            else:
                temp1 = temp1 + ',' + self.Re_No_Perno(int(j))
        data0[1382]['前序No'] = temp1

        df = pd.DataFrame(data0).T
        #outputpath = 'result_test_new.csv'
        #df.to_csv(outputpath, sep=',', index=False, header=True)
        #print(T_now)

        return T_now, df