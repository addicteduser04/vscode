import pandas as pd 

df=pd.read_csv('./Book1.csv')

df2=df.drop_duplicates()
df3=df2[~df2.isin(df)].dropna()

code_mapping = {
    "AD": 100,
    "BJ": 210, 
    "BO": 220,
    "GB": 300,
    "GJ": 310,
    "GQ": 320,
    "GZ": 330,
    "OD": 400,
    "OE": 410,
    "XD": 500,
    "XE": 510,
    "YD": 600,
    "ZD": 700,
    "ZE": 710
}