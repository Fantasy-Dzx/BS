import platgo as pg
import numpy as np
import math
import random


def Operator_GA2(pop, problem: pg.Problem, *args) -> pg.Population:
    if len(args) > 0:
        proC = args[0]
        disC = args[1]
        proM = args[2]
        disM = args[3]
    else:
        proC = 1
        disC = 20
        proM = 1
        disM = 20
    if isinstance(pop, pg.Population):
        calobj = True
        pop = pop.decs
    else:
        calobj = False
    pop1 = pop[0: math.floor(pop.shape[0] / 2), :] # 获取种群的前一半
    pop2 = pop[math.floor(pop.shape[0] / 2): math.floor(pop.shape[0] / 2) * 2, :] # 获取种群的后一半
    N = pop1.shape[0] # 获取种群个数
    D = pop1.shape[1] # 获取问题维数
    if problem.type['binary']:
        pass
    elif problem.type['real']:
        # 随机产生某一位进行交换
        index_num = [random.randint(0, 1379) for _ in range(10)]
        print(index_num)
        # 交换,每5组进行一次随机交换
        i = 0
        while i < pop1.shape[0]:
            R = np.arange(0, 5).tolist()
            random.shuffle(R)
            for j in range(10):
                pop1[i][index_num[j]], pop1[i + 1][index_num[j]], pop1[i + 2][index_num[j]], pop1[i + 3][index_num[j]], pop1[i + 4][index_num[j]] = \
                pop1[i + R[0]][index_num[j]], pop1[i + R[1]][index_num[j]], pop1[i + R[2]][index_num[j]], pop1[i + R[3]][index_num[j]], pop1[i + R[4]][index_num[j]]
            i += 5

        i = 0
        while i < pop2.shape[0]:
            R = np.arange(0, 5).tolist()
            random.shuffle(R)
            for j in range(10):
                pop2[i][index_num[j]], pop2[i + 1][index_num[j]], pop2[i + 2][index_num[j]], pop2[i + 3][index_num[j]], \
                pop2[i + 4][index_num[j]] = \
                    pop2[i + R[0]][index_num[j]], pop2[i + R[1]][index_num[j]], pop2[i + R[2]][index_num[j]], \
                    pop2[i + R[3]][index_num[j]], pop2[i + R[4]][index_num[j]]
            i += 5

        Offspring = np.vstack((pop1, pop2))

        Lower = np.tile(problem.borders[0], (2 * N, 1)) # 取下界
        Upper = np.tile(problem.borders[1], (2 * N, 1)) # 取上界
        Site = np.random.random((2 * N, D)) < proM / D # 取小于proM/D的位置为True，反之为False
        mu = np.random.random((2 * N, D)) # 产生（2N，D）的元素大小为0-1之间的随机数
        temp = np.logical_and(Site, mu <= 0.5) # 将Site与mu<=0.5的真值进行and操作
        Offspring = np.minimum(np.maximum(Offspring, Lower), Upper) # 规范子代的上下界
        # 将temp里为真的位置进行计算得到子代个体
        Offspring[temp] = Offspring[temp] + (Upper[temp] - Lower[temp]) * ((2 * mu[temp] + (1 - 2 * mu[temp]) *
                                                                            (1 - (Offspring[temp] - Lower[temp]) / (
                                                                                    Upper[temp] - Lower[temp])) ** (
                                                                                    disM + 1)) ** (
                                                                                   1 / (disM + 1)) - 1)
        temp = np.logical_and(Site, mu > 0.5) # 将Site与mu>0.5的真值进行and操作
        Offspring[temp] = Offspring[temp] + (Upper[temp] - Lower[temp]) * (
                1 - (2 * (1 - mu[temp]) + 2 * (mu[temp] - 0.5) *
                     (1 - (Upper[temp] - Offspring[temp]) / (Upper[temp] - Lower[temp])) ** (disM + 1)) ** (
                        1 / (disM + 1)))

    if calobj:
        Offspring = pg.Population(decs=Offspring)
    return Offspring


if __name__ == '__main__':
    problem = pg.problems.CEC_2020_F1()
    pop = problem.init_pop(N=100)
    Operator_GA(pop, problem)
