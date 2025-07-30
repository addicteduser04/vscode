import pandas as pd 

df = pd.read_csv('./Book1.csv')

df1=df['CompteProduit'].drop_duplicates()

df2=df1['CompteProduit']

df.to_csv('DROP_DUPLICATES.csv', index = False)