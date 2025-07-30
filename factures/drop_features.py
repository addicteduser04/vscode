import pandas as pd 
from datetime import datetime

df1=pd.read_csv('./Book1.csv',low_memory=False)
df2=pd.read_csv('./Book2.csv',low_memory=False)
df3=pd.read_csv('./Book3.csv',low_memory=False)
df4=pd.read_csv('./julienne.csv',low_memory=False,sep=';')

df4 = df4.rename(columns={'ddmmyyyy': 'date'})
df4 = df4.rename(columns={'jjjjjj': 'julienne'})

df1=df1.drop(columns=['DateCreation','DateModification','DateEDI','ReferenceEDI','Taxes'],axis=1)

df4['date'] = pd.to_datetime(df4['date'], format="%Y-%m-%d %H:%M:%S.%f")
df1['DateFacture'] = pd.to_datetime(df1['DateFacture'],format="%m/%d/%Y %H:%M")
df1['DateFacture'] = df1['DateFacture'].dt.date
df4['DateFacture'] = df4['date'].dt.date


df5 = pd.merge(df1, df4, on="DateFacture", how='left')
df5 = df5.drop(columns=['DateFacture', 'date'])


df5.to_csv('afriware_julienne.csv',index=False)