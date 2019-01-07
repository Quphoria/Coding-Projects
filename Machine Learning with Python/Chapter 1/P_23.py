from P_22 import *

#create datafrom from data in X_train
#label the columns using the strings in iris_dataset.feature_names
iris_dataframe = pd.DataFrame(X_train,columns=iris_dataset.feature_names)
#create a scatter matrix from the dataframe, colour by y_train
pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15),
                            marker="o", hist_kwds={"bins": 20}, s=60,
                            alpha=.8, cmap=mglearn.cm3)
plt.show()
input()
