from P_4 import *

print("Sample counts per class:\n{}".format(
        {n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
input()
