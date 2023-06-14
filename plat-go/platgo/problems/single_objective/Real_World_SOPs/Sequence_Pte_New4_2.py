import copy

import numpy as np
import pandas as pd
import platgo as pg


class Sequence_Pte_New4_2(pg.Problem):
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
        self.name = "Sequence_Pte_New4_2"
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
        self.seqNoDict = {}
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
        data.insert(data.shape[1], 'SeqNo', '')
        data = data.T.to_dict('dict')

        for i in range(len(seq)):
            data[seq[i]]['SeqNo'] = str(i)

        data[1380]['SeqNo'] = '-2'
        data[1381]['SeqNo'] = '-1'
        data[1382]['SeqNo'] = '1380'
        data[1383]['SeqNo'] = '1381'

        df = pd.DataFrame(data).T
        outputpath = 'result_test_new.csv'
        df.to_csv(outputpath, sep=',', index=False, header=True)
        return df


    def check(self, df):
        for k, row in df.iterrows():
            self.seqNoDict[row['No']] = int(row['SeqNo'] or 0)
        for k, row in df.iterrows():
            if row['前序约束'] == row['前序约束']:
                constraintsSeqNo = [self.seqNoDict[i] for i in row['前序约束'].split(',')]
                thisNodeSeqNo = self.seqNoDict[row['No']]
                for c in constraintsSeqNo:
                    if c > thisNodeSeqNo:
                        return 10
        return 1