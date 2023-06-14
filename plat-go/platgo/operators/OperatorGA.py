import platgo as pg
import numpy as np
import math


def Operator_GA(pop, problem: pg.Problem, *args) -> pg.Population:
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
    pop1 = pop[0: math.floor(pop.shape[0] / 2), :]
    pop2 = pop[math.floor(pop.shape[0] / 2): math.floor(pop.shape[0] / 2) * 2, :]
    N = pop1.shape[0]
    D = pop1.shape[1]
    if problem.type['binary']:
        pass
    elif problem.type['permutation']:
        # Genetic operators for permutation based encoding
        # Order crossover
        Offspring = np.vstack((pop1, pop2))
        k = np.random.randint(0, high=D, size=2 * N)
        for i in range(N):
            Offspring[i, k[i] + 1:] = np.setdiff1d(pop2[i, :], pop1[i, :k[i] + 1], True)  # noqa
            Offspring[i + N, k[i] + 1:] = np.setdiff1d(pop1[i, :], pop2[i, :k[i] + 1], True)  # noqa
        # Slight mutation
        k = np.random.randint(0, high=D, size=2 * N) + 1
        s = np.random.randint(0, high=D, size=2 * N) + 1
        for i in range(2 * N):
            if s[i] < k[i]:
                # np.hstack(([:s[i]-1], [k[i]], [s[i]-1:k[i]], [k[i]+1:]))
                # Offspring[i, :] = Offspring[i, :]
                Offspring[i, :] = np.hstack((np.hstack(
                    (np.hstack((Offspring[i, : s[i]-1], Offspring[i, k[i]-1])), Offspring[i, s[i]-1: k[i]-1],)),
                                   Offspring[i, k[i]:],))
                # Offspring[i, :] = Offspring[i, np.array([temp1])]
            elif s[i] > k[i]:
                # [:k[i]-1, k[i]:s[i]-1, k[i]-1, s[i]:]
                # Offspring[i, :] = Offspring[i, :]
                Offspring[i, :] = np.hstack((np.hstack(
                    (np.hstack((Offspring[i, : k[i]-1], Offspring[i, k[i]: s[i]-1],)), Offspring[i, k[i]-1],)),
                                   Offspring[i, s[i]-1:],))
                # Offspring[i, :] = Offspring[i, np.array([temp2])]
    elif problem.type['two_permutation']:
        Offspring = np.vstack((pop1, pop2))
        pop1_1 = pop1[:, :int(D / 2)]  # 前段
        pop1_2 = pop1[:, int(D / 2):]  # 后段
        pop2_1 = pop2[:, :int(D / 2)]  # 前段
        pop2_2 = pop2[:, int(D / 2):]  # 后段
        k = np.random.randint(0, high=int(D / 2), size=2 * N)
        k1 = np.random.randint(0, high=int(D / 2), size=2 * N)
        for i in range(N):
            Offspring[i, k[i] + 1: int(D / 2)] = np.setdiff1d(pop2_1[i, :], pop1_1[i, :k[i] + 1], True)  # noqa
            Offspring[i + N, k[i] + 1: int(D / 2)] = np.setdiff1d(pop1_1[i, :], pop2_1[i, :k[i] + 1], True)  # noqa

            Offspring[i, k1[i] + 1 + int(D / 2):] = np.setdiff1d(pop2_2[i, :], pop1_2[i, :k1[i] + 1], True)  # noqa
            Offspring[i + N, k1[i] + 1 + int(D / 2):] = np.setdiff1d(pop1_2[i, :], pop2_2[i, :k1[i] + 1], True)  # noqa

        # Slight mutation
        k = np.random.randint(0, high=int(D/2), size=2 * N) + 1
        k1 = np.random.randint(0, high=int(D/2), size=2 * N) + 1
        s = np.random.randint(0, high=int(D/2), size=2 * N) + 1
        s1 = np.random.randint(0, high=int(D/2), size=2 * N) + 1
        for i in range(2 * N):
            # 前段
            if s[i] < k[i]:
                Offspring[i, :int(D/2)] = np.hstack((np.hstack(
                    (np.hstack((Offspring[i, : s[i] - 1], Offspring[i, k[i] - 1])), Offspring[i, s[i] - 1: k[i] - 1],)),
                                             Offspring[i, k[i]: int(D/2)],))
            elif s[i] > k[i]:
                Offspring[i, :int(D/2)] = np.hstack((np.hstack(
                    (np.hstack((Offspring[i, : k[i] - 1], Offspring[i, k[i]: s[i] - 1],)), Offspring[i, k[i] - 1],)),
                                             Offspring[i, s[i] - 1: int(D/2)],))
             # 后段
            if s1[i] < k1[i]:
                Offspring[i, int(D/2):] = np.hstack((np.hstack(
                    (np.hstack((Offspring[i, int(D/2): s1[i] - 1 + int(D/2)], Offspring[i, k1[i] - 1 + int(D/2)])), Offspring[i, s1[i] - 1 + int(D/2): k1[i] - 1 + int(D/2)],)),
                                             Offspring[i, k1[i] + int(D/2):],))
            elif s1[i] > k1[i]:
                Offspring[i, int(D/2):] = np.hstack((np.hstack(
                    (np.hstack((Offspring[i, int(D/2): k1[i] - 1 + int(D/2)], Offspring[i, k1[i] + int(D/2): s1[i] - 1 + int(D/2)],)), Offspring[i, k1[i] - 1 + int(D/2)],)),
                                             Offspring[i, s1[i] - 1 + int(D/2):],))




    else:
        beta = np.zeros((N, D)) # 产生N行D列的0矩阵
        mu = np.random.random((N, D)) # 产生N行D列的元素大小为0-1之间的随机数
        beta[mu <= 0.5] = (2 * mu[mu <= 0.5]) ** (1 / (disC + 1))
        beta[mu > 0.5] = (2 - 2 * mu[mu > 0.5]) ** (-1 / (disC + 1))
        beta = beta * (-1) ** np.random.randint(0, 2, (N, D)) # 产生N行D列的元素为0，1的随机数np.random.randint(0, 2, (N, D))
        beta[np.random.random((N, D)) < 0.5] = 1
        beta[np.tile(np.random.random((N, 1)) > proC, (1, D))] = 1
        Offspring = np.vstack(
            ((pop1 + pop2) / 2 + beta * (pop1 - pop2) / 2, (pop1 + pop2) / 2 - beta * (pop1 - pop2) / 2))
        Lower = np.tile(problem.borders[0], (2 * N, 1))
        Upper = np.tile(problem.borders[1], (2 * N, 1))
        Site = np.random.random((2 * N, D)) < proM / D
        mu = np.random.random((2 * N, D))
        temp = np.logical_and(Site, mu <= 0.5)
        Offspring = np.minimum(np.maximum(Offspring, Lower), Upper)
        Offspring[temp] = Offspring[temp] + (Upper[temp] - Lower[temp]) * ((2 * mu[temp] + (1 - 2 * mu[temp]) *
                                                                            (1 - (Offspring[temp] - Lower[temp]) / (
                                                                                    Upper[temp] - Lower[temp])) ** (
                                                                                    disM + 1)) ** (
                                                                                   1 / (disM + 1)) - 1)
        temp = np.logical_and(Site, mu > 0.5)
        Offspring[temp] = Offspring[temp] + (Upper[temp] - Lower[temp]) * (
                1 - (2 * (1 - mu[temp]) + 2 * (mu[temp] - 0.5) *
                     (1 - (Upper[temp] - Offspring[temp]) / (Upper[temp] - Lower[temp])) ** (disM + 1)) ** (
                        1 / (disM + 1)))
    if calobj:
        Offspring = pg.Population(decs=Offspring)
    return Offspring


if __name__ == '__main__':
    problem = pg.problems.CEC_2020_F1()
    pop = np.random.randint(0, 10, (76, 7))
    Operator_GA(pop, problem)
