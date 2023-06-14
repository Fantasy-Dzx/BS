from abc import ABC, abstractmethod
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import platgo as pg
#from .gui import draw


class Algorithm(ABC):
    """
    算法模板基类
    """
    type: dict = {'single': False, 'multi': False, 'many': False, 'real': False, 'binary': False, 'permutation': False,
                  "large": False, 'expensive': False, 'constrained': False, 'preference': False, 'multimodal': False,
                  'sparse': False, 'gradient': False}

    def __init__(self, problem: pg.Problem, maxgen: int, draw_gen: int = 1) -> None:
        self.name = 'Algorithm'
        self.problem = problem
        self.maxgen = maxgen  # 最大进化代数
        self.gen = 0  # 当前进化代数
        self.track = pg.Track()  # 进化追踪器
        self._p_bar = tqdm(total=maxgen)  # 进度条
        self.is_bar = True  # 是否显示进度条
        self.draw_gen = draw_gen
        self.best_objv = None
        self.root = None
        if self.draw_gen != 0:
            plt.ion()

    @abstractmethod
    def go(self):
        """算法运行主函数"""
        pass

    def _show_bar(self) -> None:
        """更新进度条"""
        if not self.is_bar:
            return
        if self.gen >= self.maxgen:
            self._p_bar.close()
        else:
            self._p_bar.update(1)

    def not_terminal(self, pop: pg.Population) -> bool:
        """检查算法是否到结束条件"""
        self._show_bar()
        self.track.objv_his.append(pop.objv)
        self.best_objv = []
        for i in range(len(self.track.objv_his)):
            self.best_objv.append(np.min(self.track.objv_his[i]))
        if self.problem.M == 1:
            self.track.soea_median.append(np.median(self.track.objv_his[-1]))
        if self.gen >= self.maxgen:
            if self.draw_gen != 0 and self.problem.M != 1:
                self.track.hv.append(pg.metrics.cal_hv(pop, self.track.refer_array))
            if self.draw_gen != 0:
                self.draw()
                plt.ioff()
                plt.show()
            # draw(data1=np.array(self.track.objv_his), data2=np.array(self.track.soea_median))
            plt.ioff()
            plt.draw()
            return False
        else:
            if self.problem.M != 1 and self.draw_gen != 0 and self.gen % self.draw_gen == 0:
                if self.gen == 0:
                    self.track.refer_array = pop.objv
                # self.track.refer_array = pop.objv
                self.track.hv.append(pg.metrics.cal_hv(pop, self.track.refer_array))
            self.gen += 1
            if self.draw_gen != 0:
                self.draw()
            # draw(data1=np.array(self.track.objv_his), data2=np.array(self.track.soea_median))
            plt.draw()
            if self.root is not None:
                self.root.update()
            return True

    def draw(self, hv: bool = False):
        """
        画图，
        NOTEb 还没想好需要哪些功能
        :return:
        """
        plt.clf()
        if hv is True:
            plt.plot(np.arange(len(self.track.hv))*self.draw_gen, self.track.hv)
            plt.xlim(left=0)
            plt.ylabel("HV value")
            plt.show()
            pass

        if self.problem.M == 1:
            plt.plot(self.track.soea_median, label='median objective')
            best_objv = []
            for i in range(len(self.track.objv_his)):
                best_objv.append(np.min(self.track.objv_his[i]))
            plt.plot(best_objv, label='best objective')
            plt.xlabel('number of generation')
            plt.ylabel('value of objective')
            plt.xlim(left=0)
            plt.legend()

        elif self.problem.M == 2:
            # 取最后一代种群目标值
            data = self.track.objv_his[-1]
            objv1 = data[:, 0]
            objv2 = data[:, 1]
            plt.xlim(min(objv1), max(objv1))
            plt.ylim(min(objv2), max(objv2))
            plt.xlabel('f1')
            plt.ylabel('f2')
            plt.scatter(objv1, objv2)

        elif self.problem.M == 3:
            ax = plt.subplot(projection='3d')
            ax.set_xlabel('f1')
            ax.set_ylabel('f2')
            ax.set_zlabel('f3')
            # ax.grid(False)
            data = self.track.objv_his[-1]
            ax.scatter3D(data[:, 0], data[:, 1], data[:, 2], marker='o', depthshade=False)
            ax.view_init(35, 50)

        else:
            data = self.track.objv_his[-1]
            obj_dim = np.arange(1, data.shape[1] + 1)
            plt.xlabel("dimension on")
            plt.ylabel("f")
            plt.plot(obj_dim, data.T, c='b')
            plt.xlim(1, data.shape[1])

        plt.pause(0.001)
