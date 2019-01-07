from P_2 import *

from scipy import sparse

#Convert the NumPy array to a SciPy sparse matrix in CSR format
#Only the nonzero entries are stored
sparse_matrix = sparse.csr_matrix(eye)
print("\nSciPy sparce CSR matrix:\n{}".format(sparse_matrix))
input()
