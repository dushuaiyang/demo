import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('arms1.csv', encoding='utf-8')

df['price'] = pd.to_numeric(df['price'], errors='coerce')

unique_types = df['type'].unique()

for weapon_category in unique_types:
    avg_prices = []
    subset = df[df['type'] == weapon_category]
    unique_weapon_types = subset['weapon_type'].unique()

    for weapon_type in unique_weapon_types:
        subset_weapon = subset[subset['weapon_type'] == weapon_type]

        if not subset_weapon.empty:
            avg_price = subset_weapon['price'].mean()
            avg_prices.append(avg_price)
        else:
            avg_prices.append(np.nan)

    plt.figure(figsize=(10, 6))
    bar_positions = np.arange(len(unique_weapon_types))
    plt.bar(bar_positions, avg_prices, width=0.8, color='tab:blue')
    plt.xlabel('weapon_type')
    plt.ylabel('average price', color='tab:blue')
    plt.title(f"不同type的武器平均价格 - {weapon_category}")
    plt.xticks(bar_positions, unique_weapon_types, rotation=45)

    # 添加数值标签
    for j, price in enumerate(avg_prices):
        if not np.isnan(price):
            plt.text(j, price, f'{price:.2f}', ha='center', va='bottom')

    # 隐藏顶部和右侧的边框
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # 显示图形
    plt.tight_layout()
    plt.show()