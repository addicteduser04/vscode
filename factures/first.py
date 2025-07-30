import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt 
import numpy as np

x=pd.read_csv('./afriware_julienne.csv',low_memory=False)
y=pd.read_csv('./Book2.csv',low_memory=False)
z=pd.read_csv('./Book3.csv',low_memory=False)

y=y.drop(columns=['GLMCU'],axis=1)
x=x.dropna()
y=y.dropna()
z=z.dropna()

values_to_delete = ['BF', 'KI', 'S1', 'SC', 'SV', 'YG', 'YH', 'ZB']

y = y[~y['GLDCT'].isin(values_to_delete)]
z = z[~z['RPDCT'].isin(values_to_delete)]

x=x[0:10000]
y=y[0:10000]
z=z[0:10000]

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

y['GLDCT'] = y['GLDCT'].map(code_mapping)
z['RPDCT'] = z['RPDCT'].map(code_mapping)
x['TypeFacture'] = x['TypeFacture'].map(code_mapping)

x_ids = set(x["NumFacture"])
y_ids = set(y["GLDOC"])
z_ids = set(z["RPDOC"])

x_y_common = x[x["NumFacture"].isin(y_ids)]
x_z_common = x[x["NumFacture"].isin(z_ids)]

x_missing_y = x[~x["NumFacture"].isin(y_ids)]
x_missing_z = x[~x["NumFacture"].isin(z_ids)]
xy = pd.merge(x, y, left_on="NumFacture" , right_on="GLDOC", how='left')
xz = pd.merge(x, z, left_on="NumFacture", right_on="RPDOC", how = 'left')

X_train_y = xy[x.columns.difference(['NumFacture'])]
y_train = xy[y.columns.difference(['GLDOC'])]

X_train_z = xz[x.columns.difference(['NumFacture'])]
z_train = xz[z.columns.difference(['RPDOC'])]

train_y_combined = pd.concat([X_train_y, y_train], axis=1)
train_y_combined = train_y_combined.dropna()

X_train_y = train_y_combined[X_train_y.columns]
y_train = train_y_combined[y_train.columns]

model_y = MultiOutputRegressor(RandomForestRegressor())
model_y.fit(X_train_y, y_train)

train_z_combined = pd.concat([X_train_z, z_train], axis=1)
train_z_combined = train_z_combined.dropna()

X_train_z = train_z_combined[X_train_z.columns]
z_train = train_z_combined[z_train.columns]

model_z = MultiOutputRegressor(RandomForestRegressor())
model_z.fit(X_train_z, z_train)

X_missing_y = x_missing_y[x.columns.difference(['NumFacture'])]
X_missing_z = x_missing_z[x.columns.difference(['NumFacture'])]

predicted_y = model_y.predict(X_missing_y)
predicted_z = model_z.predict(X_missing_z)

predicted_y_df = pd.DataFrame(predicted_y, columns=y_train.columns)
predicted_y_df.insert(0, 'NumFacture', x_missing_y['NumFacture'].values)

predicted_z_df = pd.DataFrame(predicted_z, columns=z_train.columns)
predicted_z_df.insert(0, 'NumFacture', x_missing_z['NumFacture'].values)

print("Mean Squared Error:", mean_squared_error(y_train, predicted_y[0:len(y_train)]))
print("R² Score:", r2_score(y_train, predicted_y[0:len(y_train)]))

print("Mean Squared Error:", mean_squared_error(z_train, predicted_z[0:len(z_train)]))
print("R² Score:", r2_score(z_train, predicted_z[0:len(z_train)]))


final_y = pd.concat([y, predicted_y_df], ignore_index=True)
final_z = pd.concat([z, predicted_z_df], ignore_index=True)

importances = model_y.estimators_[0].feature_importances_
feature_names = X_train_y.columns

indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10,6))
plt.title("Feature Importances (First Output)")
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
plt.tight_layout()


importances_z = model_z.estimators_[0].feature_importances_
feature_names_z = X_train_z.columns
indices_z = np.argsort(importances_z)[::-1]

plt.figure(figsize=(10,6))
plt.title("Feature Importances for z (First Target Column)")
plt.bar(range(len(importances_z)), importances_z[indices_z])
plt.xticks(range(len(importances_z)), [feature_names_z[i] for i in indices_z], rotation=90)
plt.tight_layout()
plt.show()

final_y.to_csv('test1.csv', index=False)
final_z.to_csv('test2.csv', index=False)