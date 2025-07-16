import pandas as pd 
import numpy as np
df=pd.read_csv('./jde_3b11.csv')
columns1=["RPKCO","RPDCT","RPDOC","RPSFX","RPAG","RPAAP","RPAN8","RPCTY","RPFY","RPPN"]
a=df.columns
b=np.array(a)
print(b[0])
c=b[0]
d=c.split(';')
print(d)
df1 = pd.DataFrame([d], columns=columns1)
print(df1.head())
i=0
for i in range(len(df)) : 
    a_i=df.loc[i]
    b_i=np.array(a_i)
    c_i=b_i[0]
    d_i=c_i.split(';')
    df1.loc[len(df1)] = d_i
    i+=1

df1.to_csv("jde_3b11_fixed.csv",index=False)