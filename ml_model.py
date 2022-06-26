import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVR
import sklearn.externals
import warnings
import pickle
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
import seaborn as sns

data_path = 'Data/housing_data.csv'
housing_data = pd.read_csv(data_path)
print(housing_data.head(10))
print(housing_data.info())

# Filling all missing spaces especially in Garage column
imputer = SimpleImputer(strategy='median')
housing_data_rooms = housing_data.drop(["Location", "Longitude", "Latitude", "Price"], axis=1)
transformed_data = imputer.fit_transform(housing_data_rooms)
new_rooms_data = pd.DataFrame(transformed_data, columns=housing_data_rooms.columns, index=housing_data_rooms.index)
# New transformed data set after filling all missing spaces
new_housing_data = pd.concat([housing_data.drop(["Bathrooms", "Garage", "Bedrooms"], axis=1), new_rooms_data],
                             axis=1)  # Concatenating dataframes of transformed data with part of existing dataframe

# Correlations of features with price feature
corr_matrix = new_housing_data.corr()
plt.imshow(corr_matrix, cmap='hot')
print(corr_matrix["Price"].sort_values(ascending=False))
print(corr_matrix)
plt.show()

# Visualize data
new_housing_data.plot(kind="scatter", x="Longitude", y="Latitude", s=(new_housing_data["Bedrooms"] + new_housing_data["Bathrooms"] + new_housing_data["Garage"]/10), label="Avg. House Size" , c='Price', alpha=0.4, figsize=(10,7),  cmap=plt.get_cmap("jet"), colorbar=True)
plt.legend()
plt.show()

# Pairplotting features
sns.pairplot(new_housing_data, hue="Price", diag_kind="hist")

# Handling Location attribute
transformer = OneHotEncoder()
transformed = transformer.fit_transform(new_housing_data[["Location"]]).toarray()
cat_data = pd.DataFrame(transformed, columns=transformer.categories_, index=new_housing_data["Location"].index)
prepared_housing_data = pd.concat([new_housing_data, cat_data], axis=1)    # Concatenating dataframes of transformed data with part of existing dataframe

prepared_housing_data.info()
prepared_housing_data.head(5)


# Splitting data into datasets
housing_data = prepared_housing_data.drop(["Location",  "Price"], axis=1)  # Removes house prices and locations from data
housing_labels = prepared_housing_data['Price']    # Sets house prices to labels in a data frame
train_X, data_X, train_y, label_y = train_test_split(housing_data.values, housing_labels.values, test_size=0.20, random_state=47, shuffle=True)
# Splitting data into test datasets and validation datasets
test_X, validation_X, test_y, validation_y = train_test_split(data_X, label_y, random_state=47, shuffle=True, test_size=0.10)


# Model selection
lr_reg = LinearRegression()
dt_reg = DecisionTreeRegressor()
rf_reg = RandomForestRegressor()
svm_reg = SVR()
etr_reg = ExtraTreesRegressor()
voting_reg = VotingRegressor(estimators=[('rf', rf_reg), ('lr', lr_reg), ('dt', dt_reg), ('svm_reg',svm_reg),('etr_reg', etr_reg)])


print("Analysis of the predictors on the test dataset")
print("Analysis of the predictors on the test dataset")
# print("Labels : {}".format(list(test_y[:5])))
for reg in (lr_reg, dt_reg, rf_reg,svm_reg,etr_reg, voting_reg):
    reg.fit(train_X, train_y)
    y_pred = reg.predict(test_X)
    scores = cross_val_score(reg, train_X, train_y, scoring="neg_mean_squared_error", cv=10)   # Checks for scores in sets of training data
    print("\n" + reg.__class__.__name__)
    print("Accuracy : {}".format(reg.score(test_X, test_y)* 100))
    print("Root Mean Squared Error : {}".format(mean_squared_error(test_y,y_pred, squared=False)))
    print("Mean Squared Error : {}".format(mean_squared_error(test_y,y_pred, squared=True)))
    print("Mean Absolute Error : {}".format(mean_absolute_error(test_y,y_pred)))
    print("Mean Absolute Percentage Error : {}".format(mean_absolute_percentage_error(test_y,y_pred)))
    print("R Squared: {}".format(r2_score(test_y,y_pred)))


print("Accuracy on validation dataset")
print("Accuracy on validation dataset")
# print("Labels : {}".format(list(validation_y[:5])))
for reg in (lr_reg, dt_reg, rf_reg,svm_reg,etr_reg, voting_reg):
    reg.fit(train_X, train_y)
    y_pred = reg.predict(validation_X)
    print("\n" + reg.__class__.__name__)
    print("Accuracy : {}".format(reg.score(validation_X,validation_y)* 100))
    print("Root Mean Squared Error : {}".format(mean_squared_error(validation_y,y_pred, squared=False)))
    print("Mean Squared Error : {}".format(mean_squared_error(validation_y,y_pred, squared=True)))
    print("Mean Absolute Error : {}".format(mean_absolute_error(validation_y,y_pred)))
    print("Mean Absolute Percentage Error : {}".format(mean_absolute_percentage_error(validation_y,y_pred)))
    print("R Squared: {}".format(r2_score(validation_y,y_pred)))


print("Accuracy on train dataset")
# print("Labels : {}".format(list(train_y[:5])))
for reg in (lr_reg, dt_reg, rf_reg,svm_reg,etr_reg, voting_reg):
    reg.fit(train_X, train_y)
    y_pred = reg.predict(train_X)
    print("\n" + reg.__class__.__name__)
    print("Accuracy : {}".format(reg.score(train_X,train_y)* 100))
    print("Root Mean Squared Error : {}".format(mean_squared_error(train_y,y_pred, squared=False)))
    print("Mean Squared Error : {}".format(mean_squared_error(train_y,y_pred, squared=True)))
    print("Mean Absolute Error : {}".format(mean_absolute_error(train_y,y_pred)))
    print("Mean Absolute Percentage Error : {}".format(mean_absolute_percentage_error(train_y,y_pred)))
    print("R Squared: {}".format(r2_score(train_y,y_pred)))

# Model tuning on selected model
n_estimators = [int(x) for x in np.linspace(start=1, stop=20, num=20)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 120, num=12)]
min_samples_split = [2, 6, 10]
min_samples_leaf = [1, 3, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth, 'min_samples_split'
                : min_samples_split, 'min_samples_leaf': min_samples_leaf, 'bootstrap': bootstrap}

rf_random = RandomizedSearchCV(estimator=rf_reg, param_distributions=random_grid, n_iter=100, cv=5, verbose=2, random_state=35, n_jobs=-1)
rf_random.fit(train_X, train_y)
print("Best hyperparameters : ", rf_random.best_params_)


# Saving model
pickle.dump(rf_random, open("model_rf.pkl","wb"))
