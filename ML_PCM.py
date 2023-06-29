#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 16:36:30 2023

@author: vipin
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)


import pandas as pd
import numpy as np

from ta import add_all_ta_features

# Statistics
from statsmodels.tsa.stattools import adfuller

# Unsupervised Machine Learning
from sklearn.decomposition import PCA

# Supervised Machine Learning
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

# Reporting
import matplotlib.pyplot as plt
import yfinance


df = yfinance.download(tickers = "TATAMOTORS.NS",start="2000-03-06",
                               interval = "1d", group_by = 'ticker', auto_adjust = True)


df = df[["Open", "High", "Low", "Close","Volume"]]
df.head()


# Add TA
df = add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)


# Identify non-stationary columns
non_stationaries = []
for col in df.columns:
    dftest = adfuller(df[col].values)
    p_value = dftest[1]
    t_test = dftest[0] < dftest[4]["1%"]
    if p_value > 0.05 or not t_test:
        non_stationaries.append(col)
print(f"Non-Stationary Features Found: {len(non_stationaries)}")


df_stationary = df.copy()
df_stationary[non_stationaries] = df_stationary[non_stationaries].pct_change()
df_stationary = df_stationary.iloc[1:]

# Find NaN Rows

na_list = df_stationary.columns[df_stationary.isna().any().tolist()]
df_stationary.drop(columns=na_list, inplace=True)

df_stationary.replace([np.inf,-np.inf],0,inplace=True)
df_stationary.head()


df_stationary["TARGET"] = -1
#TOMMOROW PRICE IS HIGHER OR NOT
df_stationary.loc[df_stationary["Close"].shift(-1) > df_stationary["Close"],"TARGET"] = 1
df_stationary.dropna(inplace=True)

# Split Target from Featureset
X = df_stationary.iloc[:, :-1]
y = df_stationary.iloc[:, -1]

# Feature Scaling
df_sc = df_stationary.copy()
X_fs = StandardScaler().fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_fs, y, test_size=0.7, random_state=42)


# PCA
n_components = 14
pca = PCA(n_components=n_components)
pca_result = pca.fit(X_train)
X_train_pca = pca_result.transform(X_train)
X_test_pca = pca_result.transform(X_test)

# Calculate the variance explained by Principle Components
print("Variance of each component: ", pca.explained_variance_ratio_)
print("\n Total Variance Explained: ", round(sum(list(pca.explained_variance_ratio_)) * 100, 2))


#Create columns
pca_cols = []
for i in range(n_components):
    pca_cols.append(f"PC_{i}")
    
pca_cols


df_pca = pd.DataFrame(data=X_train_pca,columns=pca_cols)
df_pca.head()

classifier = RandomForestClassifier(n_estimators=12, max_depth=2, random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy}")
print(f"Test Precision: {precision}")


# Test for Overfitting
train_scores, test_scores = list(), list()
values = [i for i in range(1, 200)]
for i in values:
    classifier = RandomForestClassifier(n_estimators=i, max_depth=2, random_state=0)
    classifier.fit(X_train, y_train)
    
    # Training Data
    y_train_pred = classifier.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_train_pred)
    train_scores.append(accuracy_train)
    
    # Test Data
    y_test_pred = classifier.predict(X_test)
    accuracy_test = accuracy_score(y_test, y_test_pred)
    test_scores.append(accuracy_test)
    
len(X_test[1])
X_test[0].shape
qq = classifier.predict([X_test[-1]])
qq[0]
