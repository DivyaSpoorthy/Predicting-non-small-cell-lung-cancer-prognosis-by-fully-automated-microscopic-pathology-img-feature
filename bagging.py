import numpy as np

#import cv2
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import metrics

#read data and store in X and Y

from numpy import genfromtxt
X = genfromtxt('training_file.csv', delimiter=',', dtype=None)
Y = genfromtxt('test_file.csv', delimiter=',', dtype=None)

#train test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

#Random forest classifier with linear kernel

clf = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)
clf.fit(X_train, Y_train)

#predicting values for X_test

Y_estimated = clf.predict(X_test)
target_names = ['adenocarcimona', 'squamous cell carcinoma']
report = classification_report(Y_test, Y_estimated, target_names=target_names)
print(report)

#AUC score

Y_test[Y_test == 0] = 2
Y_estimated[Y_estimated == 0] = 2

fpr, tpr, thresholds = metrics.roc_curve(Y_test, Y_estimated, pos_label=2)
score = metrics.auc(fpr, tpr)
print("AUC score:")
print(score)