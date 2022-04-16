import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.model_selection import RandomizedSearchCV

data_path = 'housing_data.csv'
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
corr_matrix = housing_data.corr()
print(corr_matrix)
plt.imshow(corr_matrix, cmap='hot')
plt.show()
print(corr_matrix["Price"].sort_values(ascending=False))

# Visualize data
new_housing_data.plot(kind="scatter", x="Longitude", y="Latitude", s=(
        new_housing_data["Bedrooms"] + new_housing_data["Bathrooms"] + new_housing_data["Garage"] / 10),
                      label="Avg. House Size", c='Price', alpha=0.4, figsize=(10, 7), cmap=plt.get_cmap("jet"),
                      colorbar=True)
plt.legend()
plt.show()

# Feature scaling
ss = StandardScaler()
housing_data_to_scale = new_housing_data.drop(["Location", "Longitude", "Latitude"], axis=1)
scaled_data = ss.fit_transform(housing_data_to_scale)
new_scaled_data = pd.DataFrame(scaled_data, columns=housing_data_to_scale.columns, index=housing_data_to_scale.index)
prepared_housing_data = pd.concat(
    [new_housing_data.drop(["Bathrooms", "Garage", "Bedrooms", "Price"], axis=1), new_scaled_data],
    axis=1)  # Concatenating dataframes

# Splitting data into datasets
housing_data = prepared_housing_data.drop(["Location", "Price"], axis=1)  # Removes house prices and locations from data
housing_labels = prepared_housing_data['Price']  # Sets house prices to labels in a data frame
train_X, data_X, train_y, label_y = train_test_split(housing_data, housing_labels, test_size=0.20, random_state=47,
                                                     shuffle=True)
# Splitting data into test datasets and validation datasets
test_X, validation_X, test_y, validation_y = train_test_split(data_X, label_y, random_state=47, shuffle=True,
                                                              test_size=0.10)

# Model selection
lr_clf = LinearRegression()
dt_clf = DecisionTreeRegressor()
rf_clf = RandomForestRegressor()
voting_clf = VotingRegressor(estimators=[('rf', rf_clf), ('lr', lr_clf), ('dt', dt_clf)])


def display_scores(scores):
    print("Scores: {}".format(scores))
    print("Mean: {}".format(scores.mean()))
    print("Standard deviation: {}".format(scores.std()))


# Analysis of the predictors on test set
print("Analysis of the predictors on the test dataset")
print("Labels : {}".format(list(test_y[:5])))
for clf in (lr_clf, dt_clf, rf_clf, voting_clf):
    clf.fit(train_X, train_y)
    y_pred = clf.predict(test_X)
    scores = cross_val_score(clf, train_X, train_y, scoring="neg_mean_squared_error", cv=10)   # Checks for scores in sets of training data
    model_rmse_scores = np.sqrt(-scores)                                                       # Calculates the performance metric using root mean square method
    print("\n" + clf.__class__.__name__)
    print("Predictions : {}".format(y_pred[:5]))
    print("Accuracy : {}".format(clf.score(test_X, test_y)))
    display_scores(model_rmse_scores)


# Analysis of the predictors on validation set
print("Accuracy on validation dataset")
print("Labels : {}".format(list(validation_y[:5])))
for clf in (lr_clf, dt_clf, rf_clf, voting_clf):
    clf.fit(train_X, train_y)
    y_pred = clf.predict(validation_X)
    print("\n" + clf.__class__.__name__)
    print("Accuracy : {}".format(clf.score(validation_X, validation_y) * 100))
    print("Predictions : {}".format(y_pred[:5]))

# Model tuning on selected model
n_estimators = [int(x) for x in np.linspace(start=1, stop=20, num=20)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 120, num=12)]
min_samples_split = [2, 6, 10]
min_samples_leaf = [1, 3, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth, 'min_samples_split'
                : min_samples_split, 'min_samples_leaf': min_samples_leaf, 'bootstrap': bootstrap}

rf_random = RandomizedSearchCV(estimator=rf_clf, param_distributions=random_grid, n_iter=100, cv=5, verbose=2, random_state=35, n_jobs=-1)
rf_random.fit(train_X, train_y)
print("Best hyperparameters : ", rf_random.best_params_)
