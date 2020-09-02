import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.transforms as mtransforms
plt.rc('font',family='Times New Roman')

name = ['NIKKEI.csv', 'HANGSENG.csv', 'SENSEX.csv', 'SP500.csv', 'KOSPI.csv', 'SSE.csv', 'EURONEXT.csv']

df = pd.read_csv(name[0], index_col=0, parse_dates=True, na_values='.',infer_datetime_format=True,squeeze=True).fillna(method ='pad')
df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis='columns', inplace=True)
df.rename(columns={'Close': 'NIKKEI'}, inplace=True)

def vol_graph(name):
	for i in range(1,len(name)):
		df_0 = pd.read_csv(name[i], index_col=0, parse_dates=True, na_values='.',infer_datetime_format=True,squeeze=True).fillna(method ='pad')
		df_0.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis='columns', inplace=True)
		index_name = ''
		for j in range(len(name[i])-4):
			index_name = index_name + name[i][j]
		df_0.rename(columns={'Close': index_name}, inplace=True)
		df[index_name] = df_0[index_name]

vol_graph(name)

df = df.apply(lambda x: x/x[0])
df.plot(figsize=(11,6)).axhline(1, lw=1, color='black')
ax = plt.gca()
ax.set_ylabel('Дохідність (відносно початкового значення)')
ax.set_xlabel('Дата')
ax.set_title('Дохідність фондових індексів (2000-2020 рр.)\n')
ax.set_ylim([-0.5,8])
plt.yticks(np.arange(-0.5, 8, step=0.5))
plt.savefig("index_dyn_")
plt.show()
plt.close()