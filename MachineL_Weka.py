import pandas as pd
from scipy.io import arff
from sklearn.linear_model import LinearRegression
from sys import exit

arff_file = arff.loadarff('./house.arff')

house = pd.DataFrame(arff_file[0])

print(house.head(), '\n')

lin_reg_model = LinearRegression()

columns = ['houseSize', 'lotSize', 'bedrooms', 'granite', 'bathroom']

lin_reg_model.fit(house[columns], house['sellingPrice'])

for i in range(len(columns)):
    print(f'{lin_reg_model.coef_[i]:.4f}', '⨯', columns[i], '+')

print(lin_reg_model.intercept_)

exit()

arff.file = arff.loadarff('./myhouse.arff')

myhouse = pd.DataFrame(arff_file[0])

print(myhouse)

print(lin_reg_model.predict(myhouse[columns]))




