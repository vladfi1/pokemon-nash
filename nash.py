import numpy as np
import scipy.optimize as opt


def nash(matrix: np.ndarray):
  n, m = matrix.shape
  assert n == m
  assert n > 1

  # assert antisymmetric
  assert np.allclose(matrix, -matrix.T)

  # probabilities must be in [0, 1]
  bounds = (0, 1)

  # probilities must sum to 1
  A_eq = np.ones((1, n))
  b_eq = 1

  # Nash must beat every pure strategy.
  A_ub = matrix
  b_ub = np.zeros(n)

  # objective doesn't matter
  c = np.zeros(n)

  res = opt.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
  return res.x

RPS = np.array([
  [ 0, -1,  1],
  [ 1,  0, -1],
  [-1,  1,  0],
])

print(nash(RPS))
