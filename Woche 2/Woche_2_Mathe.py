import numpy as np
import scipy


def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)

P = np.array([
[490, -390, -1500, 1300],
[-590, 1400, -600, 1300],
[-0.5*np.sqrt(2), -0.3*np.sqrt(2), -0.4*np.sqrt(2), 5],
[0,0,0,1]])

P = np.array([
[490, -390, -1500, 1300],
[-590, 1400, -600, 1300],
[-0.5*np.sqrt(2), -0.3*np.sqrt(2), -0.4*np.sqrt(2), 5]])

U, Sigma, V_transposed = np.linalg.svd(P)

np.set_printoptions(formatter={'float': '{:0.8f}'.format})


p = np.array([1300, 1300, 5])

# MMT = M * M.T

M = np.array([
[490, -390, -1500],
[-590, 1400, -600],
[-0.5*np.sqrt(2), -0.3*np.sqrt(2), -0.4*np.sqrt(2)]
])

Q, R = np.linalg.qr(M.T) # Transponierte der Matrix nehmen
K = R.T
R = Q.T

print("Calibration Matrix (K):\n", K)
K = K / K[-1, -1]

print("Calibration Matrix (K):\n", K)
print("Rotation Matrix (R):\n", R)

# eigenvalues_M = np.linalg.eigvals(M)
# print("Eigenvalues of M:", eigenvalues_M)
#
# eigenvalues_MMT = np.linalg.eigvals(MMT)
# print("Eigenvalues of MMT:", eigenvalues_MMT)


# Check if all eigenvalues are greater than zero (considering numerical precision)
# is_positive_definite = np.all(eigenvalues_MMT > 1e-10)  # Using a small threshold instead of 0
# print("Is MMT positive definite?", is_positive_definite)
#
# print(is_pos_def(MMT))
#
# print(MMT, '\n')
#
# K = scipy.linalg.lu(MMT, permute_l=True)

# K = np.linalg.cholesky(MMT)

# np.dot(K, K.T.conj())

# for array in K:
#     print(array, "\n")

