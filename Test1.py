# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:22:39 2024

@author: maryana
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
#%%
#Dataset
df = pd.read_csv('y_posts.csv')
#%%
# Exploration
print(df.head())
print(df.describe())
print(df.info())

#%%
# Visualization
sns.pairplot(df)
plt.show()

#%%
# Exclude non-numeric columns
numeric_df = df.select_dtypes(include=[np.number])

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.show()

#%%
# Encoding categorical variables using one-hot encoding
df_encoded = pd.get_dummies(df, columns=['Country', 'PostType', 'PostWeekday'], drop_first=True)

# Split data
X = df_encoded.drop('EngagementScore', axis=1)
y = df_encoded['EngagementScore']

#%%
# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#%%
# Define the evaluation
def evaluate_model(y_test, y_pred):
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'MAE: {mae}')
    print(f'MSE: {mse}')
    print(f'R2: {r2}')

#%%
# Fit Random Forest Model
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Evaluate Random Forest
print("Random Forest Performance:")
evaluate_model(y_test, y_pred_rf)
#%%
# Fit Gradient Boosting Model
gb_model = GradientBoostingRegressor()
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

# Evaluate Gradient Boosting
print("Gradient Boosting Performance:")
evaluate_model(y_test, y_pred_gb)

#%%
#  5-fold cross-validation on the Gradient Boosting
cv_scores = cross_val_score(gb_model, X, y, cv=5, scoring='r2')
print(f'Cross-Validation R2 Scores: {cv_scores}')
print(f'Mean Cross-Validation R2 Score: {cv_scores.mean()}')


#%%
#  importance GB
importances = gb_model.feature_importances_
indices = np.argsort(importances)[::-1]
features = X.columns

plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
plt.bar(range(X.shape[1]), importances[indices], align='center')
plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=90)
plt.show()

#%%
import shap

#  SHAP explainer
explainer = shap.TreeExplainer(gb_model)

# SHAP values for the test set
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, feature_names=features)

# Dependence plot for the top feature
shap.dependence_plot(np.argmax(importances), shap_values, X_test, feature_names=features)
