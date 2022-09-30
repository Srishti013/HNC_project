# -*- coding: utf-8 -*-
"""Data_Cleaning, Preparation and Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cXj1MyACqzmYnsRYabn4_bTWYPtzc3vM
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns 
import scipy as sp
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import sem
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier
import seaborn as sns
!pip install catboost
from catboost import CatBoostClassifier

master = pd.read_csv('Master_file')

len(master.columns.tolist())

# Deleting columns with more than 30% null values

for col in master.columns:
  if master[col].isna().sum() >= 0.3 * len(master):
    del master[col]
cols = master.columns.tolist()
len(cols)

# Dropping numerical features with < 3  unique values
for col in master.columns:
  if master[col].nunique() < 3 and master[col].dtype == 'float64':
    print(f"{col} {master[col].dtype}: {master[col].unique()}\n\n")
    del master[col]
cols = master.columns.tolist()
len(cols)

# List of columns having categorical data
obj_df = master.select_dtypes(include=['object']).copy()
obj_df.head()

# List of columns having numerical data
num_df = master.select_dtypes(include=['int64','float64']).copy()
num_df.head()

# Filled Nan with mode
print(master['cancer_category_id'].value_counts())
master['cancer_category_id'].fillna(master['cancer_category_id'].mode()[0],inplace=True)
print(master['cancer_category_id'].isna().sum())

# filling numerical variables with median
for col in num_df.columns:
  if master[col].isna().sum() > 0:
    print(f"{col} {master[col].dtype}: {master[col].isna().sum()}" )
    master[col].fillna(master[col].median(),inplace=True)
    print(f"{col} {master[col].dtype}: {master[col].isna().sum()}" )

# filling categorical variables with mode
for col in obj_df.columns:
  if master[col].isna().sum() > 0:
    print(f"{col} {master[col].dtype}: {master[col].isna().sum()}" )
    master[col].fillna(master[col].mode()[0],inplace=True)
    print(f"{col} {master[col].dtype}: {master[col].isna().sum()}" )

for col in obj_df:
  master[col] = master[col].astype('category')
  master[col] = master[col].cat.codes
master.head()

cols = master.columns.tolist()
list(enumerate(cols))

for i in range(13,27):
  del master[f'xmin-slope_Body-{i}']

for i in range(13,27):
  del master[f'xmed-slope_Body-{i}']

for i in range(13,27):
  del master[f'xave-slope_Body-{i}']

for i in range(13,27):
  del master[f'volume-slope_body_Body-{i}']

for i in range(13,27):
  del master[f'volume-slope_outer-PTV_Body-{i}']

for i in range(13,27):
  del master[f'volume-ratio-slope_inner-PTV_Body-{i}']

for i in range(13,27):
  del master[f'volume-ratio-slope_outer-PTV_Body-{i}']

cols = master.columns.tolist()
list(enumerate(cols))

master.shape

master.head()

# Input
X = master.copy()
del X['replanned_or_not']
del X['patient_num']
X.head()

# Output Labels
y = pd.DataFrame(master['replanned_or_not'])
y.head()

# Data Split
# diving into 70%(train) and 30%(test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
X_train.shape, y_train.shape

X_test.shape, y_test.shape

names = ["Nearest_Neighbors", "Cat_Boost", "Linear_SVM", "Polynomial_SVM", "RBF_SVM", "Gaussian_Process",
         "Gradient_Boosting", "Decision_Tree", "Extra_Trees", "Random_Forest", "Neural_Net", "AdaBoost",
         "Naive_Bayes", "QDA", "SGD"]

classifiers = [
    KNeighborsClassifier(3),
    CatBoostClassifier(iterations=5, learning_rate=0.1, ),
    SVC(kernel="linear", C=0.025),
    SVC(kernel="poly", degree=3, C=0.025),
    SVC(kernel="rbf", C=1, gamma=2),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0),
    DecisionTreeClassifier(max_depth=5),
    ExtraTreesClassifier(n_estimators=10, min_samples_split=2),
    RandomForestClassifier(max_depth=5, n_estimators=100),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(n_estimators=100),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
    SGDClassifier(loss="hinge", penalty="l2")]

scores = []
for name, clf in zip(names, classifiers):
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    scores.append(score)

scores

df = pd.DataFrame()
df['name'] = names
df['score'] = scores
df

cm = sns.light_palette("green", as_cmap=True)
s = df.style.background_gradient(cmap=cm)
s

sns.set(style="whitegrid")
ax = sns.barplot(y="name", x="score", data=df)