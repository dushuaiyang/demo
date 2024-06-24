import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('arm2.csv', usecols=['price', 'exterior_wear', 'quality', 'rarity', 'type'])
df.drop(df[df['type'].isin(['布章', '收藏品', '通行证', '探员', '涂鸦', '印花', '音乐盒'])].index, inplace=True)


correlation_matrix = df.corr()

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('热力图')
plt.show()
