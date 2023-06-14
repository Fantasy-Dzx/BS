import platgo as pg
import numpy as np
from shapely.geometry import Polygon, MultiPoint  # 多边形
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
from platgo.problems.single_objective.Real_World_SOPs import Sequence_Pte


class GA(pg.Algorithm):
    flag = True
    """
    应用于单目标的遗传算法
    流程：1，初始化
         2，模拟二进制交叉
         3，多项式变异
         4，环境选择
    """

    type: dict = {'single': True, 'multi': False, 'many': False, 'real': True, 'binary': True, 'permutation': True,
                  "large": True, 'expensive': False, 'constrained': False, 'preference': False, 'multimodal': False,
                  'sparse': False, 'gradient': False}

    def __init__(self, maxgen: int, problem: pg.Problem) -> None:
        # TODO 未考虑约束
        super().__init__(problem=problem, maxgen=maxgen)
        self.name = 'GA'

    def go(self, N: int = None, population: pg.Population = None) -> pg.Population:
        """
         main function for Genetic Algorithm
         if population is None, generate a new population with population size
        :param N: population size
        :param population: population to be optimized
        :return:
        """
        assert N or population, "N and population can't be both None"
        if population is None:
            pop = self.problem.init_pop(N=N)
        else:
            pop = population
            self.problem.N = pop.decs.shape[0]
        self.problem.cal_obj(pop)  # 计算目标函数值
        while self.not_terminal(pop):
            Flag = GA.flag
            if not Flag:
                break
            MatingPool = pg.utils.tournament_selection(2, self.problem.N, fitness_single(pop))
            Offspring = pg.operators.Operator_GA(pop[MatingPool], self.problem)
            self.problem.cal_obj(Offspring)
            pop = pop + Offspring

            #temp = sorted(range(len(fitness_single(pop))), key=lambda k: fitness_single(pop)[k])

            rank = np.argsort(fitness_single(pop), kind='mergesort')
            pop = pop[rank[0: self.problem.N]]

        GA.flag = True
        return pop, np.min(self.best_objv), Flag


def fitness_single(pop):
    PopCon = np.sum(np.maximum(0, pop.cv), axis=1)
    feasible = PopCon <= 0
    fitness = feasible * pop.objv.flatten() + ~feasible * (PopCon + 1e10)
    return fitness


if __name__ == '__main__':
    problem = pg.problems.Sequence_Pte()
    N = 50
    maxgen = 100
    Algorithm = pg.algorithms.GA(maxgen=maxgen, problem=problem)
    pop, best, _ = Algorithm.go(N)

    print(pop.decs[0].tolist())
    print(pop)
    print(np.min(best))

