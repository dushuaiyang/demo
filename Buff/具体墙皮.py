import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 设置显示中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('arms1.csv', encoding='utf-8')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

num = ''
while num != '2':
    num = input("请输入\n1:查询枪皮 2:结束查询\n")
    if num == '1':
        key = input('请输入你想查看的枪皮:')
        key1 = input("请输入该武器的类型:")
        if key in df['name'].values:
            if key1 in df[df['weapon_type'] == key1].values:
                plt.figure(figsize=(10, 6))
                selected_data1 = df[df['name'] == key]
                selected_data = selected_data1[selected_data1['weapon_type'] == key1]
                print(selected_data)
                selected_data.sort_values('exterior_wear', inplace=True)

                bar_positions = np.arange(len(selected_data))
                plt.bar(bar_positions, selected_data['price'], width=0.4, color='tab:blue')
                plt.xlabel('磨损程度')
                plt.ylabel('价格', color='tab:blue')
                plt.title(f"{key} 不同磨损程度的价格分布")
                plt.xticks(bar_positions, selected_data['exterior_wear'])

                # 将价格显示在条形图上，调整价格显示位置以避免与条形图重叠
                for i, price in enumerate(selected_data['price']):
                    plt.text(i, price + 0.02 * max(selected_data['price']), f'{price:.2f}', ha='center', va='bottom')

                # 隐藏顶部和右侧的边框
                ax = plt.gca()
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)

                plt.tight_layout()
                plt.show()
        else:
            print(f"未找到枪皮肤为 '{key}' 的数据。")
    else:
        print("结束查询")