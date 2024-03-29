# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:05:50 2019

@author: Emil Chrisander
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, plot, title, xlabel, ylabel, show, legend
from scipy.linalg import svd

## Set URL for raw data
url_raw_data = "https://drive.google.com/uc?export=download&id=1DEmiVdf5UGOo8lqNvNiiHqJQuiNCgxc2" ## This is a download url for a text file located on google drive. The original dataset is only available as a .rdata file (r data file). Thus, we have downloaded a text version and uploaded to a google drive server instead. 


## Load raw data file (South African Heart Disease dataset)
df_heart_disease = pd.read_csv(url_raw_data)

## Initial data manipulations
df_heart_disease = df_heart_disease.drop(columns = "row.names", axis = 1) ## erases column 'row.names'. Axis = 1 indicates it is a column rather than row drop.
df_heart_disease["famhist"] = df_heart_disease["famhist"].astype('category') ## Set discrete variables to categorial type
df_heart_disease["chd_cat"] = df_heart_disease["chd"].astype('category') ## Set discrete variables to categorial type
df_heart_disease["famhist_present"] = pd.get_dummies(df_heart_disease.famhist, prefix='famhist_',drop_first=True)
df_heart_disease = df_heart_disease.drop(columns = "famhist", axis = 1) ## erases column 'row.names'. Axis = 1 indicates it is a column rather than row drop.


## Show content of dataframe
print("Show content of dataframe")
print(df_heart_disease.head())


#######################################################
### MISSING DATA ANALYSIS #############################
#######################################################

## Check for NA observations
print("Count of NA observations (0 means no NA in variable)")
print(df_heart_disease.isnull().sum())


#######################################################
### DESCRIPTIVE SUMMARY STATISTICS ####################
#######################################################

print("Summary statistics (numerical variables)")
print(round(df_heart_disease.describe(),2))

print("Summary statistics (categorial variables)")
print(round(df_heart_disease.describe(include='category'),0))

#######################################################
### OUTLIER DETECTION  ################################
#######################################################
#boxplot(X)
#xticks(range(1,5),attributeNames)
#ylabel('cm')
#title('Fisher\'s Iris data set - boxplot')
#show()

#######################################################
### DISTRIBUTION OF VARIABLES##########################
#######################################################

print("Histogram of attributes")
print(df_heart_disease.hist())

#######################################################
### CORRELATION TABLE #################################
#######################################################

print("Correlation Matrix")
print(round(df_heart_disease.corr(method='pearson'),1))

#######################################################
### STANDARDIZATION OF ATTRIBUTES #####################
#######################################################

## Start by creating a matric representation of the dataframe (only keep attributes)
X = df_heart_disease.drop(columns = ["chd","chd_cat"], axis = 1).to_numpy(dtype=np.float32) ## Type is set to float to allow for math calculations

## Store dimensions of X as local variables
N = np.shape(X)[0] ## Number of observations
M = np.shape(X)[1] ## Number of attributes

## Substract mean values from X (create X_tilde)
X_tilde = X - np.ones((N,1))*X.mean(axis=0)

## Divide by std. deviation from X_tilde
X_tilde = X_tilde*(1/np.std(X_tilde,0))

# PCA by computing SVD of X_tilde
U,S,V = svd(X_tilde,full_matrices=False)

## Calculate rho
rho = (S*S) / (S*S).sum() 

print("First PCA")
print(V[0])

## Set threshold for variance explained
threshold = 0.95

# Plot variance explained
plt.figure()
plt.plot(range(1,len(rho)+1),rho,'x-')
plt.plot(range(1,len(rho)+1),np.cumsum(rho),'o-')
plt.plot([1,len(rho)],[threshold, threshold],'k--')
plt.title('Variance explained by principal components');
plt.xlabel('Principal component');
plt.ylabel('Variance explained');
plt.legend(['Individual','Cumulative','Threshold'])
plt.grid()
plt.show()

#######################################################
### Plot PC1 and PC2 against each other################
#######################################################

U,S,Vh = svd(X_tilde,full_matrices=False)
V = Vh.T  
# Project the centered data onto principal component space
Z = X_tilde @ V

# Indices of the principal components to be plotted
i = 0
j = 1
y = X[:,0] #################### not sure about X
# Plot PCA of the data
f = figure()
title('South African heart disease data: PCA')
#Z = array(Z)
C = M
for c in range(C):
    # select indices belonging to class c:
    class_mask = y==c
    plot(Z[class_mask,i], Z[class_mask,j], 'o', alpha=.5)
#legend(classNames)
xlabel('PC{0}'.format(i+1))
ylabel('PC{0}'.format(j+1))

# Output result to screen
show()

