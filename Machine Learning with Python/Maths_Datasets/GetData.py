from imports import *

from sklearn.datasets import load_boston
boston = load_boston()
print("Data shape: {}".format(boston.data.shape))
df = pd.DataFrame(boston.data, columns=boston.feature_names)
df['target'] = boston.target
display(df)
input()
