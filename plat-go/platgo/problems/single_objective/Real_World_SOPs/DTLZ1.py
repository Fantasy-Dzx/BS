import numpy as np
import platgo as pg

class DTLZ1(pg.Problem):
    
    def __init__(self, M: int = 3) -> None:
        self.name = 'DTLZ1'
        self.type['multi'], self.type['many'], self.type['real'], self.type['large'], self.type['expensive'] = [True]*5
        self.M = M
        self.D = M + 4
        lb = [0] * self.D
        ub = [1] * self.D
        self.borders = np.array([lb, ub])
        super().__init__()
    
    def cal_obj(self, pop: pg.Population) -> None:
        decs = pop.decs
        pop.cv = np.zeros((pop.N, self.D))
        XM = decs[:, (self.M - 1):]
        g = 100 * (self.D - self.M + 1 + np.sum(((XM - 0.5) ** 2 - np.cos(20 * np.pi * (XM - 0.5))), axis=1, keepdims=True))
        ones_matrix = np.ones((pop.N, 1))
        f = 0.5 * np.fliplr(np.cumprod(np.hstack([ones_matrix, decs[:, :self.M - 1]]), axis=1)) * np.hstack(
            [ones_matrix, 1 - decs[:, range(self.M - 2, -1, -1)]]) * np.tile(1 + g, (1, self.M))
        pop.objv = f  # 把求得的目标函数值赋值给种群pop的ObjV

    def get_optimal(self) -> np.ndarray:
        # 均匀采样函数还未完成
        raise NotImplementedError("get optimal has not been implemented")
    

if __name__ == '__main__':
    d = DTLZ1()
    pop = pg.Population(decs=np.random.uniform(0,1, (10, 7)))
    print(d.borders)
    print(pop.decs)
    d.cal_obj(pop)  # 计算目标函数值
    print(pop.objv)