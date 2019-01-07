from P_5 import *

#Create a simple dataset of people
data = {"Name":["John", "Anna", "Peter", "Linda"],
        "Location": ["New York", "Paris", "Berlin", "London"],
        "Age": [24, 13, 53, 33]
        }

data_pandas = pd.DataFrame(data)
#Pretty Print the dataframe
display(data_pandas)
input()
