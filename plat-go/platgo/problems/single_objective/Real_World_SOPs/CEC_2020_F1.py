import numpy as np
import platgo as pg
import scipy.io as sio


class CEC_2020_F1(pg.Problem):

    def __init__(self, D=None) -> None:
        self.name = 'CEC_2020_F1'
        self.type['single'], self.type['real'] = [True] * 2
        self.M = 1
        load_path = r'C:\Users\Administrator\Desktop\Sequence2\plat-go\platgo\problems\single_objective\Real_World_SOPs\CEC2020.mat'
        load_data = sio.loadmat(load_path)
        mat = []
        self.D = D
        for k in load_data.items():
            mat.append(k)
        self.O = mat[3][1][0][0][0][0][0]
        if self.D is None or self.D < 10:
            self.D = 5
            self.Mat = mat[3][1][0][0][0][0][1]
        elif self.D < 15:
            self.D = 10
            self.Mat = mat[3][1][0][0][0][0][2]
        elif self.D < 20:
            self.D = 15
            self.Mat = mat[3][1][0][0][0][0][3]
        else:
            self.D = 20
            self.Mat = mat[3][1][0][0][0][0][4]
        lb = [-100] * self.D
        ub = [100] * self.D
        self.borders = np.array([lb, ub])
        super().__init__()

    def cal_obj(self, pop: pg.Population) -> None:
        pop.cv = np.zeros((pop.N, self.D))
        Z = pop.decs - np.tile(self.O[0][0: pop.decs.shape[1]], (pop.decs.shape[0], 1))
        Y = np.dot(Z, self.Mat.T)
        pop.objv = 100 + Y[:, 1] ** 2 + (1e+6) * np.sum(Y[:, 1:] ** 2, axis=1)
        pop.objv = pop.objv.reshape(pop.objv.shape[0], 1)

    def get_optimal(self) -> np.ndarray:
        pass


if __name__ == '__main__':
    problem = CEC_2020_F1()
    alg = pg.algorithms.SQP(problem=problem, maxgen=100)
    pop = alg.go(100)
    print(pop)
