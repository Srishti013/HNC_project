# -*- coding: utf-8 -*-
"""Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R1fkCb1JazeuL242ENMOSAQv5mHQwdvI
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import sem
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import r2_score
from sklearn import linear_model
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR

from google.colab import drive
drive.mount('/content/drive')

master = pd.read_csv('/content/drive/My Drive/HNC/Data/Master_file')
master.head()

# Keeping only replanned patients
replanned = pd.DataFrame(master.loc[master['replanned_or_not']=='R'])
len(replanned)

len(replanned.columns)

# Deleting columns with more than 30% null values

for col in replanned.columns:
  if replanned[col].isna().sum() >= 0.3 * len(replanned):
    del replanned[col]
cols = replanned.columns.tolist()
len(cols)

# Dropping numerical features with < 3  unique values
for col in replanned.columns:
  if replanned[col].nunique() < 3 and replanned[col].dtype == 'float64':
    print(f"{col} {replanned[col].dtype}: {replanned[col].unique()}\n\n")
    del replanned[col]
cols = replanned.columns.tolist()
len(cols)

# List of columns having categorical data
obj_df = replanned.select_dtypes(include=['object']).copy()
obj_df.head()

# List of columns having numerical data
num_df = replanned.select_dtypes(include=['int64','float64']).copy()
num_df.head()

# Filled Nan with mode
print(replanned['cancer_category_id'].value_counts())
replanned['cancer_category_id'].fillna(replanned['cancer_category_id'].mode()[0],inplace=True)
print(replanned['cancer_category_id'].isna().sum())

# filling numerical variables with median
for col in num_df.columns:
  if replanned[col].isna().sum() > 0:
    print(f"{col} {replanned[col].dtype}: {replanned[col].isna().sum()}" )
    replanned[col].fillna(replanned[col].median(),inplace=True)
    print(f"{col} {replanned[col].dtype}: {replanned[col].isna().sum()}" )

# filling categorical variables with mode
for col in obj_df.columns:
  if replanned[col].isna().sum() > 0:
    print(f"{col} {replanned[col].dtype}: {replanned[col].isna().sum()}" )
    replanned[col].fillna(replanned[col].mode()[0],inplace=True)
    print(f"{col} {replanned[col].dtype}: {replanned[col].isna().sum()}" )

for col in obj_df:
  replanned[col] = replanned[col].astype('category')
  replanned[col] = replanned[col].cat.codes
replanned.head()

cols = replanned.columns.tolist()
list(enumerate(cols))

# Deleting data after 12th fraction
for i in range(13,27):
  del replanned[f'xmin-slope_Body-{i}']
  del replanned[f'xmed-slope_Body-{i}']
  del replanned[f'xave-slope_Body-{i}']
  del replanned[f'volume-slope_body_Body-{i}']
  del replanned[f'volume-slope_outer-PTV_Body-{i}']
  del replanned[f'volume-ratio-slope_inner-PTV_Body-{i}']
  del replanned[f'volume-ratio-slope_outer-PTV_Body-{i}']

# Deleting replanned_or_not column because we are only using replanned data here
del replanned['replanned_or_not']

# Creating the input of training and testing data
Rx = replanned.copy()
del Rx['patient_num']
del Rx['R_fx-determined']
Rx.head()

# Data Split
# dividing into 70%(train) and 30%(test)
X_train, X_test, y_train, y_test = train_test_split(Rx, Ry, test_size=0.3)
X_train.shape, y_train.shape

names = ["Random_Forest", "Decesion_Tree","SVR"]

regressors = [
    RandomForestRegressor(),
    DecisionTreeRegressor(),
    SVR(),
    ]

scores = []
for name, clf in zip(names, regressors):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    score = r2_score(y_test,y_pred)
    scores.append(score)

scores