import numpy as np


def tournament_selection(K: int, N: int, *args) -> np.ndarray:
    """
    TournamentSelection returns the indices
    of N solutions by K-tournament selection based on their fitness values.
    In each selection, the candidate having the MINIMUM fitness1 value will
    be selected; if more than one candidates have the same minimum value of
    fitness1, then compare their fitness2 values, and so on.
    """
    for i in range(len(args)):
        args[i].reshape(1, -1)
    fitness = np.vstack(args)
    _, rank = np.unique(fitness, return_inverse=True, axis=1)
    parents = np.random.randint(low=0, high=len(rank), size=(N, K))
    best = np.argmin(rank[parents], axis=1)
    index = parents[np.arange(N), best]
    return index


if __name__ == "__main__":
    fit1 = np.array([1, 2, 2, 4, 3, 4, 9])
    fit2 = np.array([2, 3, 2, 4, 5, 7, 1])
    ind = tournament_selection(2, 4, fit1, fit2)
    print(ind)