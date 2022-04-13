import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer


data_path = 'housing_data.csv'
housing_data = pd.read_csv(data_path)
print(housing_data.head(10))
print(housing_data.info())

# Filling all missing spaces especially in Garage column
# imputer = SimpleImputer(strategy='median');
# housing_data_rooms = housing_data.drop(["Location", "Longitude", "Latitude", "Price"], axis=1)
# transformed_data = imputer.fit_transform(housing_data_rooms)
# new_rooms_data = pd.DataFrame(transformed_data, columns=housing_data_rooms.columns, index=housing_data_rooms.index)
# # New transformed data set after filling all missing spaces
# new_housing_data = pd.concat([housing_data.drop(["Bathrooms", "Garage", "Bedrooms"], axis=1), new_rooms_data], axis=1)    # Concatenating dataframes of transformed data with part of existing dataframe


# # Correlations of features with price feature
# corr_matrix = housing_data.corr()
# print(corr_matrix)
# plt.imshow(corr_matrix, cmap='hot')
# plt.show()
# print(corr_matrix["Price"].sort_values(ascending=False))

#
# # Visualize data
# new_housing_data.plot(kind="scatter", x="Longitude", y="Latitude", s=(new_housing_data["Bedrooms"] + new_housing_data["Bathrooms"] + new_housing_data["Garage"]/10), label="Avg. House Size" , c='Price', alpha=0.4, figsize=(10,7),  cmap=plt.get_cmap("jet"), colorbar=True)
# plt.legend()
# plt.show()