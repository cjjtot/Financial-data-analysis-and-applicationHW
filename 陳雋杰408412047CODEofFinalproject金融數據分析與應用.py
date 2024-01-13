# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 02:09:23 2023

@author: 18497
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

Gold = yf.Ticker("GC=F")
Gold.info #.info 所有基本资料

Gold_data = Gold.history(Gold, start="2018-01-01", end="2023-12-15")
Gold_data

type(Gold_data)
Gold_data.columns #可以查看有哪些column
Gold_data.index #可以查看有哪些row
Gold_data = Gold_data.add_prefix('Gold_')
Gold_data.index= Gold_data.index.date # 将索引修改为只包含年月日
Gold_data = Gold_data.asfreq('B', method='pad')# 将索引重新采样为每个工作日，并向前填充缺失值。'D' 表示每日，'B' 表示每工作日，'W' 表示每周。method: 字符串，可选参数，用于处理重新采样时出现的缺失值。常见的选项有：None（默认）：不插值，保留缺失值。'pad' 或 'ffill'：使用前一个非缺失值填充缺失值。'backfill' 或 'bfill'：使用后一个非缺失值填充缺失值。'nearest'：使用最近的非缺失值进行填充。
'''Gold_data['Gold_Close'].diff()'''
Gold_pct_change=Gold_data['Gold_Close'].pct_change()

Gold_data.plot(y='Gold_Close')
""""""""""""""""""""""""""""""""""""""
NASDAQ = yf.Ticker("^IXIC")
NASDAQ.info

NASDAQ_data = NASDAQ.history(NASDAQ, start="2018-01-01", end="2023-12-15")
NASDAQ_data

NASDAQ_data.columns #可以查看有哪些column
NASDAQ_data.index #可以查看有哪些row
NASDAQ_data = NASDAQ_data.add_prefix('NASDAQ_')
NASDAQ_data.index= NASDAQ_data.index.date # 将索引修改为只包含年月日
NASDAQ_data = NASDAQ_data.asfreq('B', method='pad')# 将索引重新采样为每个工作日，并向前填充缺失值
NASDAQ_pct_change=NASDAQ_data['NASDAQ_Close'].pct_change()

NASDAQ_data.plot(y='NASDAQ_Close')
""""""""""""""""""""""""""""""""""""""
Shanghai = yf.Ticker("000001.SS")
Shanghai.info

Shanghai_data = Shanghai.history(Shanghai, start="2018-01-01", end="2023-12-15")
Shanghai_data

Shanghai_data.columns #可以查看有哪些column
Shanghai_data.index #可以查看有哪些row
Shanghai_data = Shanghai_data.add_prefix('Shanghai_')
Shanghai_data.index= Shanghai_data.index.date # 将索引修改为只包含年月日
Shanghai_data = Shanghai_data.asfreq('B', method='pad')# 将索引重新采样为每个工作日，并向前填充缺失值
Shanghai_pct_change=Shanghai_data['Shanghai_Close'].pct_change()

Shanghai_data.plot(y='Shanghai_Close')
""""""""""""""""""""""""""""""""""""""
df_merged = pd.concat([Gold_data, NASDAQ_data,Shanghai_data], axis=1) #合併資料 pandas套件的.concat (concatenate 連接)
df_merged

pct_change_merged = pd.concat([Gold_pct_change, NASDAQ_pct_change,Shanghai_pct_change], axis=1) #合併資料 pandas套件的.concat (concatenate 連接)
pct_change_merged
pct_change_merged = pct_change_merged.add_prefix('PctChange_')
pct_change_merged.columns #可以查看有哪些column

pct_change_merged.plot(y='PctChange_Gold_Close')
'PctChange_NASDAQ_Close'
'PctChange_Shanghai_Close'

""""""""""""""""""""""""""""""""""""""
fig,ax = plt.subplots() #先创建一个“画布”和子图对象
ax.plot(df_merged.index, df_merged['Gold_Close'],color="blue", label='Gold_Close') #括号内，可在后面加marker="o"
#繪圖，兩個y軸，第一个。x轴使用df_merged的索引，y轴使用选定列的数据
ax2=ax.twinx() #通过ax.twinx()创建了一个新的子图对象ax2，它共享相同的x轴，但有一个独立的y轴，用于绘制第二个折线图。
ax2.plot(df_merged.index, df_merged['NASDAQ_Close'],color="red", label='NASDAQ_Close')
ax2.plot(df_merged.index, df_merged['Shanghai_Close'], color="green", label='Shanghai_Close')
# Show legend for both y-axes
ax.legend(loc='upper left')
ax2.legend(loc='center right')
# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Gold_Close', color="black")
ax2.set_ylabel('NASDAQ_Close and Shanghai_Close', color="black")
""""""""""""""""""""""""""""""""""""""

df_merged.plot(y=['Gold_Close', 'Shanghai_Close'])

pct_change_merged.corr() #計算相關係數

sns.heatmap(pct_change_merged.corr())
Gold_pct_change_and_NASDAQ_pct_changeheatmap = sns.heatmap(pct_change_merged.corr(), cmap="Blues", annot=True) #画热力图,创建变数PAYEMSandCPIAUCSLheatmap用于存储sns.heatmap返回值
figure = Gold_pct_change_and_NASDAQ_pct_changeheatmap.get_figure() # 获取与图形相关联的Figure对象
""""""""""""""""""""""""""""""""""""""
'''【时间序列】ACF与PACF'''
# 创建一个2行3列的子图布局
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))
# 绘制第一行的ACF图
plot_acf(df_merged['Gold_Close'], ax=axes[0, 0], lags=40, title='Gold_Close ACF')
plot_acf(df_merged['NASDAQ_Close'], ax=axes[0, 1], lags=40, title='NASDAQ_Close ACF')
plot_acf(df_merged['Shanghai_Close'], ax=axes[0, 2], lags=40, title='Shanghai_Close ACF')
# 绘制第二行的PACF图
plot_pacf(df_merged['Gold_Close'], ax=axes[1, 0], lags=40, title='Gold_Close PACF')
plot_pacf(df_merged['NASDAQ_Close'], ax=axes[1, 1], lags=40, title='NASDAQ_Close PACF')
plot_pacf(df_merged['Shanghai_Close'], ax=axes[1, 2], lags=40, title='Shanghai_Close PACF')
# 调整布局
plt.tight_layout()


# 删除含有缺失值的行,产生新dataframe：pct_change_merged2 为了之后跑pct_change的ACF与PACF
pct_change_merged2 =pct_change_merged.dropna()
pct_change_merged2
# 创建一个2行3列的子图布局
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))
# 绘制第一行的ACF图
plot_acf(pct_change_merged2['PctChange_Gold_Close'], ax=axes[0, 0], lags=40, title='PctChange_Gold_Close ACF')
plot_acf(pct_change_merged2['PctChange_NASDAQ_Close'], ax=axes[0, 1], lags=40, title='PctChange_NASDAQ_Close ACF')
plot_acf(pct_change_merged2['PctChange_Shanghai_Close'], ax=axes[0, 2], lags=40, title='PctChange_Shanghai_Close ACF')
# 绘制第二行的PACF图
plot_pacf(pct_change_merged2['PctChange_Gold_Close'], ax=axes[1, 0], lags=40, title='PctChange_Gold_Close PACF')
plot_pacf(pct_change_merged2['PctChange_NASDAQ_Close'], ax=axes[1, 1], lags=40, title='PctChange_NASDAQ_Close PACF')
plot_pacf(pct_change_merged2['PctChange_Shanghai_Close'], ax=axes[1, 2], lags=40, title='PctChange_Shanghai_Close PACF')
# 调整布局
plt.tight_layout()
""""""""""""""""""""""""""""""""""""""
#MA均线的画图
df_merged['Gold_Close_MA'] = df_merged['Gold_Close'].rolling(window=5).mean()
df_merged['NASDAQ_Close_MA'] = df_merged['NASDAQ_Close'].rolling(window=5).mean()
df_merged['Shanghai_Close_MA'] = df_merged['Shanghai_Close'].rolling(window=5).mean()
fig2,ax = plt.subplots() #先创建一个“画布”和子图对象
ax.plot(df_merged.index, df_merged['Gold_Close_MA'],color="blue", label='Gold_Close_MA') #括号内，可在后面加marker="o"
#繪圖，兩個y軸，第一个。x轴使用df_merged的索引，y轴使用选定列的数据
ax2=ax.twinx() #通过ax.twinx()创建了一个新的子图对象ax2，它共享相同的x轴，但有一个独立的y轴，用于绘制第二个折线图。
ax2.plot(df_merged.index, df_merged['NASDAQ_Close_MA'],color="red", label='NASDAQ_Close_MA')
ax2.plot(df_merged.index, df_merged['Shanghai_Close_MA'], color="green", label='Shanghai_Close_MA')
# Show legend for both y-axes
ax.legend(loc='upper left')
ax2.legend(loc='center right')
# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Gold_Close', color="black")
ax2.set_ylabel('NASDAQ_Close_MA and Shanghai_Close_MA', color="black")
""""""""""""""""""""""""""""""""""""""
# 创建一个一行三列的子图
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
# 第一个子图：Gold_Close vs NASDAQ_Close
axs[0].scatter(df_merged['Gold_Close'], df_merged['NASDAQ_Close'])
axs[0].set_title('Gold_Close vs NASDAQ_Close')
axs[0].set_xlabel('Gold_Close')
axs[0].set_ylabel('NASDAQ_Close')
# 第二个子图：Gold_Close vs Shanghai_Close
axs[1].scatter(df_merged['Gold_Close'], df_merged['Shanghai_Close'])
axs[1].set_title('Gold_Close vs Shanghai_Close')
axs[1].set_xlabel('Gold_Close')
axs[1].set_ylabel('Shanghai_Close')
# 第三个子图：NASDAQ_Close vs Shanghai_Close
axs[2].scatter(df_merged['NASDAQ_Close'], df_merged['Shanghai_Close'])
axs[2].set_title('NASDAQ_Close vs Shanghai_Close')
axs[2].set_xlabel('NASDAQ_Close')
axs[2].set_ylabel('Shanghai_Close')
# 调整子图之间的间距
plt.tight_layout()
""""""""""""""""""""""""""""""""""""""
# 创建包含3个子图的图表，每行1个子图
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
# 绘制第一个散点图
axs[0].scatter(pct_change_merged['PctChange_Gold_Close'], pct_change_merged['PctChange_NASDAQ_Close'])
axs[0].set_title('PctChange_Gold_Close vs PctChange_NASDAQ_Close')
axs[0].set_xlabel('PctChange_Gold_Close')
axs[0].set_ylabel('PctChange_NASDAQ_Close')
# 绘制第二个散点图
axs[1].scatter(pct_change_merged['PctChange_Gold_Close'], pct_change_merged['PctChange_Shanghai_Close'])
axs[1].set_title('PctChange_Gold_Close vs PctChange_Shanghai_Close')
axs[1].set_xlabel('PctChange_Gold_Close')
axs[1].set_ylabel('PctChange_Shanghai_Close')
# 绘制第三个散点图
axs[2].scatter(pct_change_merged['PctChange_NASDAQ_Close'], pct_change_merged['PctChange_Shanghai_Close'])
axs[2].set_title('PctChange_NASDAQ_Close vs PctChange_Shanghai_Close')
axs[2].set_xlabel('PctChange_NASDAQ_Close')
axs[2].set_ylabel('PctChange_Shanghai_Close')
# 调整子图之间的间距
plt.tight_layout()

""""""""""""""""""""""""""""""""""""""

#MA均线的画图
fig2,ax = plt.subplots() #先创建一个“画布”和子图对象
ax.plot(df_merged.index, df_merged['Gold_Close_MA'],color="blue", label='Gold_Close_MA') #括号内，可在后面加marker="o"
#繪圖，兩個y軸，第一个。x轴使用df_merged的索引，y轴使用选定列的数据
ax2=ax.twinx() #通过ax.twinx()创建了一个新的子图对象ax2，它共享相同的x轴，但有一个独立的y轴，用于绘制第二个折线图。
ax2.plot(df_merged.index, df_merged['NASDAQ_Close_MA'],color="red", label='NASDAQ_Close_MA')
# Show legend for both y-axes
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Gold_Close', color="black")
ax2.set_ylabel('NASDAQ_Close_MA', color="black")

#MA均线的画图
fig2,ax = plt.subplots() #先创建一个“画布”和子图对象
ax.plot(df_merged.index, df_merged['Gold_Close_MA'],color="blue", label='Gold_Close_MA') #括号内，可在后面加marker="o"
#繪圖，兩個y軸，第一个。x轴使用df_merged的索引，y轴使用选定列的数据
ax2=ax.twinx() #通过ax.twinx()创建了一个新的子图对象ax2，它共享相同的x轴，但有一个独立的y轴，用于绘制第二个折线图。
ax2.plot(df_merged.index, df_merged['Shanghai_Close_MA'],color="green", label='Shanghai_Close_MA')
# Show legend for both y-axes
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Gold_Close', color="black")
ax2.set_ylabel('Shanghai_Close_MA', color="black")

#MA均线的画图
df_merged.plot(y=['NASDAQ_Close_MA', 'Shanghai_Close_MA'], color=['Red', 'green'])
plt.xlabel('Date')
plt.ylabel('NASDAQ_Close_MA and Shanghai_Close_MA')

fig2,ax = plt.subplots() #先创建一个“画布”和子图对象
ax.plot(df_merged.index, df_merged['NASDAQ_Close_MA'],color="Red", label='NASDAQ_Close_MA') #括号内，可在后面加marker="o"
#繪圖，兩個y軸，第一个。x轴使用df_merged的索引，y轴使用选定列的数据
ax2=ax.twinx() #通过ax.twinx()创建了一个新的子图对象ax2，它共享相同的x轴，但有一个独立的y轴，用于绘制第二个折线图。
ax2.plot(df_merged.index, df_merged['Shanghai_Close_MA'],color="green", label='Shanghai_Close_MA')
# Show legend for both y-axes
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('NASDAQ_Close_MA', color="black")
ax2.set_ylabel('Shanghai_Close_MA', color="black")