#Import libraries
import re
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import pickle
import pandas_profiling as pdp
#%matplotlib inline


#load data
df = pd.read_csv('cheki.csv', index_col=0)

#Check data
df.head()

#basic feature engineering and data transformation
df['brand'] = df['desc'].apply(lambda x: str(x).lower().split()[1])
df['year'] = df['desc'].apply(lambda x: str(x).lower().split()[0]).astype(int)
df['model'] = df['desc'].apply(lambda x: " ".join(str(x).lower().split()[2:]))
df = df.fillna('manual')

df['trans'] = df['trans'].apply(lambda x: 1 if x=='automatic' else 0)
df['origin'] = df['origin'].apply(lambda x: 1 if x=='foreign' else 0)
df['engine'] = df['engine'].apply(lambda x: 1 if x=='petrol' else 0)

#drop the description column
df = df.drop('desc', axis=1)

#check data again
df.head()

#Get quick insight about the data with pandas profiling
pdp.ProfileReport(df)

#get dummy variables for the categorical data (i.e brand and model)
df = pd.get_dummies(df, columns = ['brand', 'model'])

#plot the correlation of all features
corr= df.corr()
#corr
f, ax = plt.subplots(figsize=(20, 5))
sns.heatmap(corr,cmap='coolwarm',linewidths=2.0, annot=True)

#split data into dependent and independent variable (X and y)
X = df.drop('price', axis=1)
y = df['price'].values

#split data into traning set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.20, random_state=2)

#import metrics for model evaluation
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import roc_curve,auc
from sklearn.metrics import r2_score
from math import sqrt

#train random forest model
model = RandomForestRegressor()
model.fit(X_train,y_train)

#make predictions and check for the root mean square error
pred_cv = model.predict(X_test)
score = sqrt(mean_squared_error(y_test,pred_cv))
print('Root_mean_squared_error',score)

#Fit the model on the entire dataset
model.fit(X,y)

# save the model to disk/serialise the model
filename = 'may.pkl'
pickle.dump(model, open(filename, 'wb'))
