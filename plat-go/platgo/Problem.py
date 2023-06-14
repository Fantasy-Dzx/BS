import random

from abc import ABC, abstractmethod
import numpy as np
import platgo as pg


# noinspection PyPep8Naming,PyPep8Naming
class Problem(ABC):
    """
    问题基类
    属性:
        name: 问题名
        ...
        TODO: 还缺少上下界开闭区间的描述
    
    """
    name: str  # 问题名
    borders: np.ndarray  # 上下界
    # 问题类型，默认全为False
    type: dict = {'single': False, 'multi': False, 'many': False, 'real': False, 'binary': False, 'permutation': False,
                  "large": False, 'expensive': False, 'constrained': False, 'preference': False, 'multimodal': False,
                  'sparse': False, 'two_permutation': False}
    M: int     # 目标数
    D: int     # 决策变量维度
    N: int = 100   # 种群大小
    FE: int = 0
    maxFE: int = 10000

    def __init__(self):
        assert self.name is not None
        assert self.borders is not None
        assert self.type is not None
        assert self.M is not None
        assert self.D is not None
        assert self.N is not None

    def init_pop(self, N: int = None) -> pg.Population:
        """
        根据问题的要求初始化种群染色体
        :param N: 种群大小，即决策矩阵大小
        """
        if N is None:
            N = self.N
        else:
            self.N = N
        if self.type["real"]:
            lb = self.borders[0]  # 获取问题的取值下界
            ub = self.borders[1]  # 获取问题的取值上界
            lb = np.tile(lb, (self.N, 1))  # 将lb矩阵向0维坐标方向重复N次
            ub = np.tile(ub, (self.N, 1))  # 将ub矩阵向0维坐标方向重复N次
            decs = np.random.uniform(lb, ub)  # TODO 这里种群初始化的时候要考虑编码方式
        if self.type["permutation"]:
            decs = np.argsort(np.random.random((self.N, self.D)), axis=1)
        if self.type["two_permutation"]:
            tmp = np.argsort(np.random.random((self.N, int(self.D / 2))), axis=1)
            tmp1 = np.argsort(np.random.random((self.N, int(self.D / 2))), axis=1)
            decs = np.hstack((tmp, tmp1))
        pop = pg.Population(decs=decs)
        return pop

    def fix_decs(self, pop: pg.Population, method: int = 0) -> None:
        """
        修复越界
        :param pop: 需要修复的种群
        :param method: 多种修复方法
        :return: 修复种群，不需要返回值
        """
        # TODO 对border做检查
        if method == 0:  # 截断修复
            pop.decs = np.clip(pop.decs, self.borders[0], self.borders[1])

        # TODO 循环修复 往复修复 随机修复

    @abstractmethod
    def cal_obj(self, pop) -> None:
        pass
    
    def cal_cv(self, pop) -> None:
        pass
    
    @abstractmethod
    def get_optimal(self) -> np.ndarray:
        pass

    def g_fun(self, pop):
        raise NotImplementedError("该问题没有梯度函数，无法求解")
