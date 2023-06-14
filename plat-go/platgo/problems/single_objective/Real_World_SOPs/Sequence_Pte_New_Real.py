import copy

import numpy as np
import pandas as pd
import platgo as pg


class Sequence_Pte_New_Real(pg.Problem):
    """
    创建People类，可视为并行初始条件，用于获取并行序列
    1.该并行线路中已经完成的工序
    2.该线路是否正在有工序进行
    3.该线路正在进行的工序的层级
    """

    class Trash:
        def __init__(self):
            self.Tout = 2
            self.Tin = 1
            self.Tdoor = 1
            # 层级设定（D1,D2,D3）, D4, D5, D6
            self.D_123 = 71
            self.D_4 = 46
            self.D_5 = 13
            self.D_6 = 8

    class People:
        def __init__(self):
            self.No_over = []
            self.Busy = False


    def __init__(self) -> None:
        self.name = "Sequence_Pte_New_Real"
        self.type['single'], self.type['real'], self.type['large'] = [True] * 3
        self.M = 1
        # 并行数目
        self.People_Num = 24
        # 定义初始维度（即1-148）
        self.D = 1380
        lb = [0] * self.D
        ub = [1] * self.D
        self.borders = np.array([lb, ub])
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
        print(seq)
        seq = sorted(range(len(seq)), key=lambda k: seq[k])  # 将实数改为序列
        for k in range(self.D):
            seq[k] = int(seq[k])
        print(seq)


        data = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence2\plat-go\Data\lianyun_data_0331.csv")
        data.insert(data.shape[1], 'E_time', 0)
        data.insert(data.shape[1], 'Finish', False)
        data.insert(data.shape[1], 'P_ing', '')
        data = data.T.to_dict('dict')

        Num_Trash = 10
        trash = []
        for i in range(Num_Trash):
            trash.append(self.Trash())
        pro_ing = []

        """
        将序列按照前后序关系修复
        """
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
                    i = i + 1
            else:
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
        #1：按照工序层级进行分类
        """
        Segment = [[] for _ in range(4)]
        for i in range(len(seq)):
            # 求出所在层级
            d = data[seq[i]]['工序层级']
            if int(d[-1]) - 1 < 3:
                Segment[0].append(seq[i])
            else:
                Segment[int(d[-1]) - 3].append(seq[i])

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
            for j in range(4):
                k = [x for x in Idx[i] if x in Segment[j]]
                temp = temp + k
            Idx[i] = temp

        # for i in range(Num_Trash):
        #     print(len(Idx[i]), Idx[i])

        for i in range(len(seq)):
            no = data[seq[i]]['No']
            k_a, k_b = self.No_Perno(no)
            seq[i] = Idx[int(k_a) - 1].pop(0)

        print(len(seq), seq)

        for i in range(10):
            print(trash[i].Tin, trash[i].Tout, trash[i].Tdoor)

        T_now = 0
        p_num = self.People_Num
        P = []
        for i in range(self.People_Num):
            P.append(self.People())
        Lable = ''

        def pro_out():
            nonlocal p_num, pro_ing, T_now, data, P, Lable, trash

            temp = pro_ing.pop(0)
            k_a, k_b = self.No_Perno(temp['No'])
            k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
            data[k_num]['Finish'] = True
            # 层级说明
            temp_d = int(temp['工序层级'][-1])
            if (temp_d == 1) | (temp_d == 2) | (temp_d == 3):
                trash[int(k_a) - 1].D_123 -= 1
            elif temp_d == 4:
                trash[int(k_a) - 1].D_4 -= 1
            elif temp_d == 5:
                trash[int(k_a) - 1].D_5 -= 1
            elif temp_d == 6:
                trash[int(k_a) - 1].D_6 -= 1
            pro_peo = data[k_num]['P_ing'].split(',')
            # print('pro_peo:',pro_peo)
            if data[k_num]['工作区'] == data[k_num]['工作区']:
                loca = data[k_num]['工作区']
                if loca == "箱内":
                    trash[int(k_a) - 1].Tin = trash[int(k_a) - 1].Tin + int(data[k_num]['工人(处理阶段)-服务表'])
                elif loca == "箱外":
                    trash[int(k_a) - 1].Tout = trash[int(k_a) - 1].Tout + int(data[k_num]['工人(处理阶段)-服务表'])
                elif loca == "箱门":
                    trash[int(k_a) - 1].Tdoor = trash[int(k_a) - 1].Tdoor + int(data[k_num]['工人(处理阶段)-服务表'])
            for k in pro_peo:
                P[int(k)].Busy = False
                # print(int(k),'号人员',P[int(k)].Busy)
                p_num += 1
            T_now = temp['E_time']
            Lable = k_num
            # print("该工序完成：", k_num, temp['名称'], strftime("%H:%M:%S", gmtime(T_now)))

        # 层级设定（D1,D2,D3）, D4, D5, D6

        seq0 = copy.deepcopy(seq)
        while len(seq0) > 0:
            temp = 0
            temp_peo = int(data[seq0[temp]]['工人(处理阶段)-服务表'])
            if p_num >= temp_peo:
                # 人满足的条件下
                pop_flag = 0
                while temp < len(seq0):
                    # 0.层级约束
                    k_a, k_b = self.No_Perno(data[seq0[temp]]['No'])
                    temp_d = int(data[seq0[temp]]['工序层级'][-1])
                    if (int(temp_d) == 4) & (trash[int(k_a) - 1].D_123 != 0):
                        # print(k_a, int(temp_d), trash[int(k_a) - 1].D_123)
                        break
                    elif (int(temp_d) == 5) & (trash[int(k_a) - 1].D_4 != 0):
                        # print(k_a, int(temp_d), trash[int(k_a) - 1].D_4)
                        break
                    elif (int(temp_d) == 6) & (trash[int(k_a) - 1].D_5 != 0):
                        # print(k_a, int(temp_d), trash[int(k_a) - 1].D_5)
                        break
                    # 1.是否有前序，以及前序是否完成
                    flag_precess = -1
                    if data[seq0[temp]]['前序约束'] == data[seq0[temp]]['前序约束']:
                        temp_flag = 0
                        L_temp = data[seq0[temp]]['前序约束'].split(',')
                        # 先序工序所在位置,id_max,对应元素Idx[i][id_max]
                        for k in L_temp:
                            k_a, k_b = self.No_Perno(k)
                            k_num = 138 * (int(k_a) - 1) + (int(k_b) - 1)
                            # print(temp,data[temp]['No'],i,k,k_a,k_b,k_num)
                            if data[k_num]['Finish'] == False:
                                temp_flag += 1
                                break
                            # print("data[k_num]['Finish']:",k_num,data[k_num]['Finish'])
                        if temp_flag > 0:
                            temp += 1
                            continue
                    else:
                        flag_precess = -1
                    # 2.是否存在空间位置约束
                    flag_space = 0
                    if data[seq0[temp]]['工作区'] == data[seq0[temp]]['工作区']:
                        k_a, k_b = self.No_Perno(data[seq0[temp]]['No'])
                        # print("垃圾箱编号：",k_a)
                        loca = data[seq0[temp]]['工作区']
                        # print(trash[int(k_a) - 1].Tin,trash[int(k_a) - 1].Tout,trash[int(k_a) - 1].Tdoor)
                        if (loca == "箱内") & (trash[int(k_a) - 1].Tin >= int(data[seq0[temp]]['工人(处理阶段)-服务表'])):
                            flag_space += 1
                        elif (loca == "箱外") & (trash[int(k_a) - 1].Tout >= int(data[seq0[temp]]['工人(处理阶段)-服务表'])):
                            flag_space += 1
                        elif (loca == "箱门") & (trash[int(k_a) - 1].Tdoor >= int(data[seq0[temp]]['工人(处理阶段)-服务表'])):
                            flag_space += 1
                        else:
                            temp += 1
                            continue
                    else:
                        flag_space += 1

                    # 3.人员约束,返回所需人数
                    flag_people = 0
                    if p_num >= int(data[seq0[temp]]['工人(处理阶段)-服务表']):
                        flag_people = int(data[seq0[temp]]['工人(处理阶段)-服务表'])
                    else:
                        temp += 1
                        continue
                    # 4.判断条件是否均满足
                    # print(flag_precess,flag_space,flag_people)
                    if (flag_precess == -1) & (flag_space == 1) & (flag_people > 0):
                        n = 0
                        for j in range(self.People_Num):  # 寻找空闲人数
                            if n < flag_people:
                                if P[j].Busy == False:
                                    if n == 0:
                                        if len(P[j].No_over) > 0:
                                            data[seq0[temp]]['前序No'] = str(P[j].No_over[-1])
                                        else:
                                            data[seq0[temp]]['前序No'] = str(Lable)
                                        data[seq0[temp]]['P_ing'] += str(j)
                                        P[j].No_over.append(seq0[temp])
                                        P[j].Busy = True
                                    else:
                                        if len(P[j].No_over) > 0:
                                            data[seq0[temp]]['前序No'] = data[seq0[temp]]['前序No'] + ',' + str(
                                                P[j].No_over[-1])
                                        elif str(Lable) not in data[seq0[temp]]['前序No']:
                                            data[seq0[temp]]['前序No'] += str(Lable)
                                        data[seq0[temp]]['P_ing'] = data[seq0[temp]]['P_ing'] + "," + str(j)
                                        P[j].No_over.append(seq0[temp])
                                        P[j].Busy = True
                                        # print(j,'号人员',P[j].Busy)
                                    n = n + 1
                            else:
                                break
                        if str(Lable) not in data[seq0[temp]]['前序No']:
                            data[seq0[temp]]['前序No'] = data[seq0[temp]]['前序No'] + ',' + str(Lable)

                        if data[seq0[temp]]['工作区'] == data[seq0[temp]]['工作区']:
                            k_a, k_b = self.No_Perno(data[seq0[temp]]['No'])
                            loca = data[seq0[temp]]['工作区']
                            if loca == "箱内":
                                trash[int(k_a) - 1].Tin = trash[int(k_a) - 1].Tin - int(
                                    data[seq0[temp]]['工人(处理阶段)-服务表'])
                            elif loca == "箱外":
                                trash[int(k_a) - 1].Tout = trash[int(k_a) - 1].Tout - int(
                                    data[seq0[temp]]['工人(处理阶段)-服务表'])
                            elif loca == "箱门":
                                trash[int(k_a) - 1].Tdoor = trash[int(k_a) - 1].Tdoor - int(
                                    data[seq0[temp]]['工人(处理阶段)-服务表'])

                        data[seq0[temp]]['E_time'] = T_now + data[seq0[temp]]['时间-处理时间']
                        pro_ing.append(data[seq0[temp]])
                        p_num = p_num - data[seq0[temp]]['工人(处理阶段)-服务表']
                        c = seq0.pop(temp)
                        # print("该工序正在进入：", c, data[c]['名称'], strftime("%H:%M:%S", gmtime(T_now)))
                        pop_flag += 1
                        pro_ing.sort(key=lambda stu: stu['E_time'])
                        break
                # print(pop_flag, '----', len(pro_ing), '----', len(seq0), '----', p_num, '----', temp)
                if pop_flag == 0:
                    pro_out()
            else:
                pro_out()

        while len(pro_ing) > 0:
            pro_out()

        rs = 0
        for i in range(self.People_Num):
            print(i, len(P[i].No_over), P[i].No_over)
            rs = rs + len(P[i].No_over)

        print(rs, len(pro_ing), T_now)

        df = pd.DataFrame(data).T

        data0 = pd.read_csv(r"C:\Users\Administrator\Desktop\Sequence2\plat-go\Data\lianyun_data_0331.csv")
        data0 = data0.T.to_dict('dict')

        temp_seq = np.arange(0, 1380).tolist()
        for i in range(len(seq)):
            temp0 = data[i]['前序No'].split(',')
            if len(data[i]['前序No']) > 0:
                for j in temp0:
                    if temp_seq.count(int(j)) > 0:
                        temp_seq.remove(int(j))
                    if data0[i]['前序No'] == data0[i]['前序No']:
                        data0[i]['前序No'] = data0[i]['前序No'] + ',' + str(j)
                    else:
                        data0[i]['前序No'] = str(j)

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
        outputpath = 'result_test_new.csv'
        df.to_csv(outputpath, sep=',', index=False, header=True)
        #outputpath = 'result_test_new.csv'
        #df.to_csv(outputpath, sep=',', index=False, header=True)
        #print(T_now)

        return T_now, df