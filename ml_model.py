import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression

# Load data set and read info about the data set
data_path = 'data.csv'
housing_data = pd.read_csv(data_path)
print(housing_data.info())
print(housing_data.head())

# Visualize data
housing_data.plot(kind="scatter", x="Longitude", y="Latitude",s= (housing_data["Bedrooms"]+housing_data["Bathrooms"])*4, label="Rooms" , c='Price', alpha=0.4, figsize=(10,7),  cmap=plt.get_cmap("jet"), colorbar=True)
plt.legend()
plt.show()