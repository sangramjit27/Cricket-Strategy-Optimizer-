#NUMPY
import numpy as np
from numpy import *
array=zeros((2,10))
print arr
arr=np.array([2,3,4,5,6])
arr1=np.array([[2,3,4,5],[4,5,6,7]])
print(type(arr))
print(arr1.ndim)

arr3=newlinspace(1,100,8)
print(arr3)
print(arr3.itemsize)
arr4=np.random.randint(5,20,(2,10))
print(arr4)


from numpy import *
array=zeros((2,10))
print( arr)
arrays=ones((1,10))
print(arrays)
    
#PANDAS
import pandas as pd
df=pd.read_csv(r"C:\Users\hp\Desktop\NIT\demo_new.csv")
print(df)
print(type(df["Roll No"]))
print(type(df))
print(df[["Roll No","Percentage"]])
print(df[3:5][['Name',"Percentage"]])
print(df.columns)
df1=df.drop('Percentage',axis=1) #default axis=0
print(df1)
df2=df.drop(1)
print(df2.reset_index(drop=True))


import pandas as pd
df=pd.read_csv(r"C:\Users\hp\Desktop\NIT\Demo.csv")
print (df)
print(df.isnull().sum())
df1=df.dropna(how="all")
print(df1)
print(df1.describe())
#In this data 900 in scienc is outliers as it changes the entire statistics of percentage. Use median to remove outliers
df1.fillna(df['English'].median(),inplace=True)
print(df1)
print(df1.duplicated().sum)
df1.drop_duplicates(inplace=True)
print(df1)


#DAY2
import pandas as pd
df=pd.read_csv(r"C:\Users\hp\Desktop\NIT\matches.csv")
print (df)
#print(df['bowler'].value_counts().head())
df1=df['team1'].value_counts()
df2=df['team2'].value_counts()
df3=df1+df2
print(df3.sort_values(ascending=False).head())
df3=df.drop_duplicates('season')
#print(df1.sort_values('season'))
dff=df.drop_duplicates('season',keep='last')
dff.sort_values('season',inplace=True)
print(dff[['season','winner']]) #seasonwise winner


import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

df=pd.read_csv(r"C:\Users\hp\Desktop\NIT\StudentsPerformance.csv") #Alwaysv check for missing data,info,data description,duplicates
print (df.describe())
#print(df.duplicates())
df['Average']=round((df['math score']+df['reading score']+df['writing score'])/3,2)
print(df)
sb.histplot(data=df,x='Average',color='blue',bins=30,kde=True)#kde=kernel density(skew line), no. of bars=no. of divisons made between best and worst
#plt.show()
sb.histplot(data=df,x='Average',color='blue',bins=30,kde=True,hue='gender')
#plt.show
sb.histplot(data=df,x='Average',color='blue',bins=30,kde=True,hue='parental level of education')
#plt.show()
sb.histplot(data=df[df['gender']=='male'],x='Average',color='blue',bins=30,kde=True,hue='lunch')
plt.show()



import pandas as pd
from sklearn.preprocessing import StandardScaler,MinMaxScaler
df=pd.read_csv(r"C:\Users\hp\Desktop\NIT\pricee.csv")
print (df)
scaler=StandardScaler()
scale=MinMaxScaler()
df['Size_new']=scaler.fit_transform(df[['Size']])
df['Size_new1']=scale.fit_transform(df[['Size']])
print(df)

import pandas as pd
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
df=pd.read_csv(r"C:\Users\hp\Desktop\NIT\regression.csv")
#print(df)
encoder=LabelEncoder()
df['Encoded_Data']=encoder.fit_transform(df[['Qualification']])
#print(df)
df1=pd.get_dummies(df['Qualification']).astype(int)
df2=pd.concat([df,df1],axis=1)
#print(df2)
#clean the data
df2.drop('Qualification',axis=1,inplace=True)
df2['Interniew_score]=df2['Interniew_score'].fillna(df2['Interniew_score'].mean())
df2['Experience'].fillna(df2['Experi3ence'].mode()[0])
df2['Experience_new']=df2['Experience'].replace({'zero':0,'one':1,'Two':2,'Three':3,'Four':4})
df2.drop('Experience',axis=1,inplace=True)
print(df2)