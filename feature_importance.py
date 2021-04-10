import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Get numpy output in readable form
np.set_printoptions(precision=3, suppress=True)

#Load raw data
raw_data = pd.read_csv('data/OfficialCompetitionDataset.csv')

#Extract features to use
raw_features = raw_data[["beats_per_measure", "beats_per_min", "instrumentalness", "length_minutes", "major/minor", "tone", "volume", "vulgar"]]

#Extract and reshape target variable
target = raw_data[["nplays"]]
y = target.to_numpy().reshape(len(target))

#Gather categorical features and encode them
categorical_features = raw_features[["major/minor", "tone", "vulgar"]]
encoded_features = pd.get_dummies(categorical_features, drop_first=True)

#Extract numerical features
numerical_features = raw_features[["beats_per_measure", "beats_per_min", "instrumentalness", "volume"]]

#Combine numerical features and categorical features into training data
X = pd.concat([numerical_features, encoded_features], axis=1)

#Train random forest with 500 trees each with 10 leaf nodes for regularization
rfr = RandomForestRegressor(n_estimators=500, max_leaf_nodes=10)
rfr.fit(X, y)

#Output feature importances alongside feature names
features = [feature for feature in X]
print("Feature Importances:")
print("--------------------------")
for i in range(len(features)):
    print(features[i], ":", rfr.feature_importances_[i])