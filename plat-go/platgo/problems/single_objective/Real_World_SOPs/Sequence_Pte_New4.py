import copy

import numpy as np
import pandas as pd
import platgo as pg


class Sequence_Pte_New3(pg.Problem):
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
        self.name = "Sequence_Pte_New3"
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
        data.insert(data.shape[1], 'Finish', False)
        data.insert(data.shape[1], 'P_ing', '')
        data = data.T.to_dict('dict')

        Num_Trash = 10
        trash = []
        for i in range(Num_Trash):
            trash.append(self.Trash)

        P = []
        for i in range(self.People_Num):
            P.append(self.People())

        for i in range(len(seq)):
            if len(P[i % self.People_Num].No_over) > 0:
                data[seq[i]]['前序No'] = str(P[i % self.People_Num].No_over[-1])
            else:
                data[seq[i]]['前序No'] = ''
            P[i % self.People_Num].No_over.append(seq[i])
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
        data0.insert(data0.shape[1], 'SeqNo', '')
        data0 = data0.T.to_dict('dict')

        for i in range(len(seq)):
            data0[seq[i]]['SeqNo'] = str(i)

        data0[1380]['SeqNo'] = '-2'
        data0[1381]['SeqNo'] = '-1'
        data0[1382]['SeqNo'] = '1380'
        data0[1383]['SeqNo'] = '1381'

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

        return df