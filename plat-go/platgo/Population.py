import numpy as np
from typing import Union


class Population:
    """
    种群类
    """
    
    def __init__(self, N: int = None, decs: np.ndarray = None, cv: np.ndarray = None,
                 objv: np.ndarray = None, vel: np.ndarray = None) -> None:
        """
        种群初始化
        可以传入决策变量矩阵decs初始化或是根据N和problem自动初始化
        :param N:        种群大小
        :param decs:     决策矩阵
        :param cv:       约束违反矩阵
        :param objv:     目标值矩阵
        :param vel:      速度
        """
        # 初始化检查,条件为False时触发异常
        assert decs is None or decs.ndim == 2, "Population initiate error, decs must be 2-D array"
        assert cv is None or cv.ndim == 2, "Population initiate error, cv must be 2-D array"
        assert objv is None or objv.ndim == 2, "Population initiate error, objv must be 2-D array"
        # assert problem is not None or decs is not None, "Population initiate error, at least one of problem and decs is not None"  # problem和decs至少有一个不为None，否则没有办法初始化决策矩阵
        assert N is not None or decs is not None, "Population initiate error, at least one of N and decs is not None"  # N和decs至少有一个不为None， 否则不能确定种群大小
        self.decs:np.ndarray = decs.copy()
        self.cv:np.ndarray = cv.copy() if cv is not None else None
        self.objv:np.ndarray = objv.copy() if objv is not None else None
        # TODO 类中其他方法均没有增加关于vel的代码，需要用到的时候再进行添加
        self.vel:np.ndarray = vel.copy() if vel is not None else None

    @property
    def N(self) -> int:
        #决策变量的个数
        return self.decs.shape[0]
    
    def copy(self):
        """返回对象副本"""
        new_decs = self.decs.copy()
        new_cv = self.cv.copy() if self.cv is not None else None
        new_objv = self.objv.copy() if self.objv is not None else None
        pop = Population(decs=new_decs, cv=new_cv, objv=new_objv)
        return pop
    
    def __getitem__(self, ind: Union[int, list, np.ndarray, slice]):
        """
        种群切片，根据下标选择部分个体生成新的种群
        ndarray索引分为int下标索引和bool索引，计算N的方式不同
        :param ind: 新种群的索引，接受int, list, ndarray, slice
        """
        if self.decs is None:
            raise RuntimeError('The population has not been initialized')
        if type(ind) == int:
            ind = [ind]
        if type(ind) == np.ndarray:
            # 索引的类型只能是int32或bool或int64
            assert ind.dtype in [np.int32, np.int64, np.bool]
            # 索引的维度只能是 (n,) 或是 (1,n)
            assert ind.ndim == 1 or ind.ndim == 2
            if ind.ndim == 2:
                assert 1 in ind.shape
                ind = ind.flatten()
        
        new_decs = self.decs[ind]
        new_cv = self.cv[ind] if self.cv is not None else None
        new_objv = self.objv[ind] if self.objv is not None else None
        new_vel = self.vel[ind] if self.vel is not None else None
        new_pop = Population(decs=new_decs, cv=new_cv, objv=new_objv, vel=new_vel)
        return new_pop
    
    def __setitem__(self, item: Union[int, list, np.ndarray, slice], pop) -> None:
        """
        为种群内的部分个体赋值，支持多对一
        population[[0,1]] = pop
        :param item: 下标
        :param pop: instance of Population
        :return:
        """
        # TODO 两个种群需要进行检查，要么n->1，要么n->n，不允许n->m
        if self.decs is not None:
            self.decs[item] = pop.decs
        if self.cv is not None:
            self.cv[item] = pop.cv
        if self.objv is not None:
            self.objv[item] = pop.objv
    
    def __add__(self, pop):
        """
        合并种群,不更改原来的两种群，而是返回新的种群
        不会重新计算目标函数值和约束
        :param pop:
        :return:
        """
        # TODO cv和objv可以是空，但是两种群必须一致
        new_decs = np.vstack([self.decs, pop.decs])
        new_cv = np.vstack([self.cv, pop.cv]) if self.cv is not None else None
        new_objv = np.vstack([self.objv, pop.objv]) if self.objv is not None else None
        new_pop = Population(decs=new_decs, cv=new_cv, objv=new_objv)
        return new_pop
    
    def __len__(self):
        return self.decs.shape[0]
    
    def __str__(self) -> str:
        """打印种群信息"""
        return (
            """
            population information:
            ----------------------
            decs shape = {},
            best objective = {}
            """.format(
                self.decs.shape,
                np.min(self.objv, axis=0, keepdims=True)
            )
        )
