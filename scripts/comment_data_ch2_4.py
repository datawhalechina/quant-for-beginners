# -*- coding: utf-8 -*-
"""第 2～4 章 Notebook 带注释源码。"""

SOURCES_CH2_4: dict[str, dict[int, str]] = {
    "02_你的第一个量化实验.ipynb": {
        4: r'''# ========== 环境准备：导入库并设置画图中文 ==========
import warnings
warnings.filterwarnings('ignore')  # 忽略次要警告，输出更干净

import numpy as np           # 数值计算
import pandas as pd          # 表格数据处理
import matplotlib.pyplot as plt  # 绘图
import yfinance as yf        # 下载雅虎财经股票数据（需联网）

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']

print('环境就绪 ✓')
''',
        6: r'''# ========== 下载苹果 AAPL 最近约 1 年的日线数据 ==========
aapl = yf.download('AAPL', period='1y', progress=False, multi_level_index=False)  # 下载
aapl = aapl.dropna()  # 删掉有空值的行，保证数据完整

print('数据形状（行=交易日，列=字段）：', aapl.shape)  # 例如 (251, 5)
print('\n前 5 行：')
display(aapl.head())  # Jupyter 里美观显示表格前几行

print('\n各列含义速查：')
for col in aapl.columns:  # 遍历每一列的名字
    print(f'  {col}')
''',
        7: r'''# ========== 配图1：收盘价折线 + 成交量柱状图 ==========
fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True,  # 2行1列，共用日期横轴
                         gridspec_kw={'height_ratios': [3, 1]})  # 上图更高

axes[0].plot(aapl.index, aapl['Close'], color='tab:blue', linewidth=1.2, label='收盘价 Close')
axes[0].set_ylabel('价格 (美元)')
axes[0].set_title('苹果 AAPL：收盘价与成交量（真实行情）', fontsize=14)
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

axes[1].bar(aapl.index, aapl['Volume'], width=0.8, color='gray', alpha=0.5, label='成交量 Volume')
axes[1].set_ylabel('股数')
axes[1].legend(loc='upper left')
axes[1].set_xlabel('日期')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
''',
        8: r'''# ========== 配图2：最近8天 OHLC 示意图 ==========
sample = aapl.tail(8).copy()   # 取最后 8 个交易日
dates = range(len(sample))     # 0,1,...,7 用作横轴位置

fig, ax = plt.subplots(figsize=(12, 5))

for i, (idx, row) in enumerate(sample.iterrows()):  # 逐行遍历每一天
    o, h, l, c = row['Open'], row['High'], row['Low'], row['Close']  # 开高低收
    color = 'tab:red' if c < o else 'tab:green'   # 收跌红色、收涨绿色
    ax.vlines(i, l, h, color=color, linewidth=2, alpha=0.85)   # 竖线：最低到最高
    ax.hlines(o, i - 0.15, i + 0.15, color=color, linewidth=2)  # 开盘价短横线
    ax.hlines(c, i - 0.15, i + 0.15, color=color, linewidth=3)  # 收盘价粗横线

ax.set_xticks(dates)
ax.set_xticklabels([d.strftime('%m-%d') for d in sample.index], rotation=45)  # 日期标签
ax.set_ylabel('价格 (美元)')
ax.set_title('最近 8 个交易日：竖线 = High↔Low，短横线 = Open / Close（粗线=收盘）', fontsize=13)
ax.grid(True, axis='y', alpha=0.3)

from matplotlib.lines import Line2D  # 自定义图例用的小线段
legend_elements = [
    Line2D([0], [0], color='tab:green', linewidth=2, label='收涨日 (Close ≥ Open)'),
    Line2D([0], [0], color='tab:red', linewidth=2, label='收跌日 (Close < Open)'),
]
ax.legend(handles=legend_elements, loc='upper left')
plt.tight_layout()
plt.show()

print('小贴士：一天之内，价格一定满足  Low ≤ Open, Close ≤ High')
''',
        10: r'''# ========== 验证 100元→110元 的收益率例子 ==========
p_yesterday, p_today = 100, 110   # 昨天价、今天价
r = (p_today - p_yesterday) / p_yesterday  # 收益率公式
print(f'昨天: {p_yesterday} 元, 今天: {p_today} 元')
print(f'日收益率 r = {r:.2%}')  # :.2% 表示格式化为百分比，保留2位小数
''',
        12: r'''# ========== 用 pandas 计算整列日收益率 ==========
df = aapl[['Close']].copy()              # 只保留收盘价一列
df['日收益率'] = df['Close'].pct_change()  # 今天相对昨天的涨跌比例

print('最近 10 天的收盘价与日收益率：')
display(df.tail(10))

# 手算最后一天，和 pct_change 对照
row_today = df.iloc[-1]       # 最后一行（今天）
row_yesterday = df.iloc[-2]   # 倒数第二行（昨天）
manual_r = (row_today['Close'] - row_yesterday['Close']) / row_yesterday['Close']
print(f"\n验证最后一天：手算 {manual_r:.4%}，pct_change {row_today['日收益率']:.4%}")
''',
        14: r'''# ========== 日收益率曲线 + 直方图 ==========
rets = df['日收益率'].dropna()  # 去掉第一天的 NaN

fig, axes = plt.subplots(1, 2, figsize=(14, 5))  # 1行2列

axes[0].plot(rets.index, rets.values, color='steelblue', linewidth=0.9, alpha=0.85)
axes[0].axhline(0, color='black', linewidth=0.8, linestyle='--')  # 零轴参考线
axes[0].set_title('苹果 AAPL：日收益率曲线', fontsize=13)
axes[0].set_xlabel('日期')
axes[0].set_ylabel('日收益率')
axes[0].grid(True, alpha=0.3)

axes[1].hist(rets.values, bins=40, color='steelblue', edgecolor='white', alpha=0.85)
axes[1].axvline(0, color='black', linewidth=0.8, linestyle='--')
axes[1].axvline(rets.mean(), color='orange', linewidth=2, label=f'平均值 {rets.mean():.2%}')
axes[1].set_title('日收益率分布（Histogram）', fontsize=13)
axes[1].set_xlabel('日收益率')
axes[1].set_ylabel('天数')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f'样本天数: {len(rets)}')
print(f'平均日收益率: {rets.mean():.3%}（正=整体偏多涨）')
print(f'日收益率标准差: {rets.std():.3%}（越大=波动越剧烈）')
''',
        15: r'''# ========== 累计收益率曲线 ==========
cum_return = (1 + rets).cumprod() - 1  # 每天 (1+r) 连乘，再减1得到累计涨跌

plt.figure(figsize=(12, 4))
plt.plot(cum_return.index, cum_return.values * 100, color='tab:purple', linewidth=1.5)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.title('苹果 AAPL：累计收益率曲线（%）', fontsize=14)
plt.xlabel('日期')
plt.ylabel('累计收益率 (%)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f'这段区间累计涨跌: {cum_return.iloc[-1]:.2%}')
''',
        17: r'''# ========== 小实验：下载三只股票并算波动 ==========
tickers = {
    'AAPL': '苹果',
    'TSLA': '特斯拉',
    'NVDA': '英伟达',
}

period = '1y'   # 时间长度，可改成 '6mo'、'2y'
all_rets = {}   # 用字典存每只股票的中文名 → 日收益率序列

for symbol, name in tickers.items():
    data = yf.download(symbol, period=period, progress=False, multi_level_index=False).dropna()
    all_rets[name] = data['Close'].pct_change().dropna()  # 只关心收盘价涨跌
    print(f'{name} ({symbol}): {len(all_rets[name])} 个交易日')

vol = pd.Series({name: s.std() for name, s in all_rets.items()}).sort_values(ascending=False)
print('\n=== 日收益率波动（标准差，越大越猛）===')
for name, v in vol.items():
    print(f'  {name}: {v:.3%}')
''',
        18: r'''# ========== 三只股票收益率对比图 ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
colors = ['tab:blue', 'tab:orange', 'tab:green']

for (name, series), c in zip(all_rets.items(), colors):
    axes[0].plot(series.index, series.values, label=name, alpha=0.75, linewidth=0.8)
axes[0].axhline(0, color='black', linestyle='--', linewidth=0.6)
axes[0].set_title('日收益率对比', fontsize=13)
axes[0].set_xlabel('日期')
axes[0].set_ylabel('日收益率')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].bar(vol.index, vol.values * 100, color=colors[: len(vol)], edgecolor='white')
axes[1].set_title('波动大小对比（标准差 %）', fontsize=13)
axes[1].set_ylabel('标准差 (%)')
axes[1].grid(True, axis='y', alpha=0.3)
for i, v in enumerate(vol.values):
    axes[1].text(i, v * 100 + 0.02, f'{v:.2%}', ha='center', fontsize=11)

plt.tight_layout()
plt.show()

winner = vol.index[0]
print(f'\n在本实验设定下（{period} 日线），波动最大的是：{winner}')
''',
        19: r'''# ========== 三只股票 Histogram 并排对比 ==========
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, (name, series), c in zip(axes, all_rets.items(), colors):
    ax.hist(series.values, bins=35, color=c, alpha=0.75, edgecolor='white')
    ax.axvline(0, color='black', linestyle='--', linewidth=0.6)
    ax.set_title(f'{name}\nσ = {series.std():.2%}')
    ax.set_xlabel('日收益率')

axes[0].set_ylabel('天数')
fig.suptitle('三只股票：日收益率 Histogram 对比', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()
''',
    },
    "03_移动平均线策略.ipynb": {
        4: r'''# ========== 环境准备 ==========
import warnings
warnings.filterwarnings('ignore')  # 隐藏无关警告

import numpy as np              # 数值计算
import pandas as pd             # 表格数据
import matplotlib.pyplot as plt   # 画图
import yfinance as yf           # 下载股票行情（需联网）

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']

TICKER = 'AAPL'   # 股票代码，可改成 TSLA、NVDA
PERIOD = '2y'     # 下载多长历史（均线需要足够天数）

print('环境就绪 ✓')
''',
        6: r'''# ========== 模拟三种市场状态并分区上色 ==========
np.random.seed(7)              # 固定随机数，图可复现
n_up, n_down, n_noise = 60, 50, 70  # 上涨段、下跌段、横盘段各多少天

ret_up = np.random.normal(0.004, 0.008, n_up)        # 上涨段：平均日收益偏正
ret_down = np.random.normal(-0.005, 0.010, n_down)   # 下跌段：平均日收益偏负
ret_noise = np.random.normal(0.0, 0.015, n_noise)    # 横盘：均值约0，波动大

price = 100 * np.cumprod(1 + np.r_[ret_up, ret_down, ret_noise])  # 拼成价格
x = np.arange(len(price))  # 横轴：第几个交易日

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(x, price, color='black', linewidth=1.2, label='价格')

ax.axvspan(0, n_up, alpha=0.15, color='green', label='上涨趋势')
ax.axvspan(n_up, n_up + n_down, alpha=0.15, color='red', label='下跌趋势')
ax.axvspan(n_up + n_down, len(price), alpha=0.15, color='gray', label='噪声/横盘')

ax.set_title('三种市场状态（模拟）：趋势 vs 噪声', fontsize=14)
ax.set_xlabel('交易日（示意）')
ax.set_ylabel('价格')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print('绿色区：整体向上 | 红色区：整体向下 | 灰色区：方向不明显、抖动大')
''',
        8: r'''# ========== 对比「乱的价格」和「平滑的均线」==========
demo = pd.DataFrame({'Close': price})           # 用上面模拟的价格
demo['MA20'] = demo['Close'].rolling(20).mean()  # 20日移动平均

fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(demo['Close'], label='原始收盘价（很乱）', color='lightgray', linewidth=1.5)
ax.plot(demo['MA20'], label='20日移动平均线（更平滑）', color='tab:blue', linewidth=2)
ax.set_title('为什么需要平均？—— 磨平噪声，看清趋势', fontsize=14)
ax.set_xlabel('交易日（示意）')
ax.set_ylabel('价格')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
        10: r'''# ========== 下载真实股票并计算 MA5、MA20 ==========
raw = yf.download(TICKER, period=PERIOD, progress=False, multi_level_index=False)  # 下载行情
df = raw[['Close']].dropna().copy()   # 只留收盘价，去掉空行
df.columns = ['Close']                # 列名统一成 Close

df['MA5'] = df['Close'].rolling(5).mean()    # 5日均线 = 最近5天收盘均价
df['MA20'] = df['Close'].rolling(20).mean()  # 20日均线

print(f'{TICKER} 共 {len(df)} 个交易日')
display(df.tail(8))  # 显示最后8行，检查算得对不对
''',
        11: r'''# ========== 画收盘价 + 两条均线 ==========
plt.figure(figsize=(13, 5))
plt.plot(df.index, df['Close'], label='收盘价', color='gray', alpha=0.5, linewidth=1)
plt.plot(df.index, df['MA5'], label='MA5（5日均线）', color='tab:orange', linewidth=1.5)
plt.plot(df.index, df['MA20'], label='MA20（20日均线）', color='tab:blue', linewidth=2)
plt.title(f'{TICKER}：价格与移动平均线', fontsize=14)
plt.xlabel('日期')
plt.ylabel('价格')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
        13: r'''# ========== 检测金叉、死叉 ==========
df['spread'] = df['MA5'] - df['MA20']              # 短均线减长均线
df['cross'] = np.sign(df['spread']).diff()         # 符号变化：正=金叉，负=死叉

golden = df[df['cross'] > 0].dropna(subset=['MA5', 'MA20'])  # 金叉那些天
death = df[df['cross'] < 0].dropna(subset=['MA5', 'MA20'])    # 死叉那些天

print(f'样本期内 金叉 {len(golden)} 次，死叉 {len(death)} 次')
print('\n最近 3 次金叉日期：')
print(golden.tail(3).index.strftime('%Y-%m-%d').tolist())
print('\n最近 3 次死叉日期：')
print(death.tail(3).index.strftime('%Y-%m-%d').tolist())
''',
        14: r'''# ========== 金叉死叉标注图 ==========
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df.index, df['Close'], color='gray', alpha=0.4, linewidth=1, label='收盘价')
ax.plot(df.index, df['MA5'], color='tab:orange', linewidth=1.5, label='MA5')
ax.plot(df.index, df['MA20'], color='tab:blue', linewidth=2, label='MA20')

ax.fill_between(df.index, df['MA5'], df['MA20'],
                where=(df['MA5'] >= df['MA20']),
                interpolate=True, alpha=0.12, color='green', label='MA5 > MA20')

ax.scatter(golden.index, golden['MA5'], marker='^', s=80, color='green',
           edgecolors='black', linewidths=0.5, zorder=5, label='金叉（买入参考）')
ax.scatter(death.index, death['MA5'], marker='v', s=80, color='red',
           edgecolors='black', linewidths=0.5, zorder=5, label='死叉（卖出参考）')

ax.set_title(f'{TICKER}：MA5 vs MA20 —— 金叉 ▲ 与 死叉 ▼', fontsize=14)
ax.set_xlabel('日期')
ax.set_ylabel('价格')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
        16: r'''# ========== 第一个策略：MA5>MA20 则持仓 ==========
df['signal'] = (df['MA5'] > df['MA20']).astype(int)  # 满足条件=1，否则=0

df['trade'] = 0                              # 默认无交易
df.loc[df['cross'] > 0, 'trade'] = 1         # 金叉日标记买入
df.loc[df['cross'] < 0, 'trade'] = -1        # 死叉日标记卖出

hold_days = df['signal'].sum()             # signal=1 的天数
print(f'规则：MA5 > MA20 则持仓 (signal=1)')
print(f'样本期内约 {hold_days} 个交易日处于持仓状态（共 {len(df)} 天）')
print(f'共产生 { (df["trade"] != 0).sum() } 次调仓信号（买+卖）')

display(df[df['trade'] != 0][['Close', 'MA5', 'MA20', 'signal', 'trade']].tail(6))
''',
        19: r'''# ========== 策略信号大图：价格+买卖点+持仓条 ==========
buys = df[df['trade'] == 1]    # 所有买入日
sells = df[df['trade'] == -1]  # 所有卖出日

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True,
                         gridspec_kw={'height_ratios': [3, 1]})
ax_price, ax_pos = axes

ax_price.plot(df.index, df['Close'], color='gray', alpha=0.45, linewidth=1, label='收盘价')
ax_price.plot(df.index, df['MA5'], color='tab:orange', linewidth=1.5, label='MA5')
ax_price.plot(df.index, df['MA20'], color='tab:blue', linewidth=2, label='MA20')

ax_price.scatter(buys.index, buys['Close'], marker='^', s=120, color='limegreen',
                 edgecolors='darkgreen', linewidths=1, zorder=6, label='买入 ▲')
ax_price.scatter(sells.index, sells['Close'], marker='v', s=120, color='salmon',
                 edgecolors='darkred', linewidths=1, zorder=6, label='卖出 ▼')

ax_price.set_title(f'{TICKER} 双均线策略：均线 + 买卖点', fontsize=14)
ax_price.set_ylabel('价格')
ax_price.legend(loc='upper left')
ax_price.grid(True, alpha=0.3)

ax_pos.fill_between(df.index, 0, df['signal'], step='post', alpha=0.35, color='steelblue')
ax_pos.set_ylim(-0.1, 1.2)
ax_pos.set_yticks([0, 1])
ax_pos.set_yticklabels(['空仓 (0)', '持仓 (1)'])
ax_pos.set_xlabel('日期')
ax_pos.set_ylabel('信号')
ax_pos.set_title('策略持仓状态：MA5 > MA20 时持有', fontsize=12)
ax_pos.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
''',
        20: r'''# ========== 放大最近6个月，看清买卖细节 ==========
recent = df.last('6M') if len(df) > 120 else df.tail(120)  # 取最近约6个月
buys_r = recent[recent['trade'] == 1]
sells_r = recent[recent['trade'] == -1]

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(recent.index, recent['Close'], color='gray', alpha=0.5, linewidth=1, label='收盘价')
ax.plot(recent.index, recent['MA5'], color='tab:orange', linewidth=1.8, label='MA5')
ax.plot(recent.index, recent['MA20'], color='tab:blue', linewidth=2.2, label='MA20')
ax.scatter(buys_r.index, buys_r['Close'], marker='^', s=140, color='limegreen',
           edgecolors='darkgreen', linewidths=1, zorder=6, label='买入')
ax.scatter(sells_r.index, sells_r['Close'], marker='v', s=140, color='salmon',
           edgecolors='darkred', linewidths=1, zorder=6, label='卖出')
ax.set_title(f'{TICKER} 近 6 个月：金叉买入 / 死叉卖出（局部放大）', fontsize=14)
ax.set_xlabel('日期')
ax.set_ylabel('价格')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
    },
    "04_策略回测.ipynb": {
        4: r'''# ========== 环境准备 ==========
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']
BENCHMARK = 'SPY'    # 大盘对比用标普500 ETF
PERIOD = '2y'        # 回测样本长度

print('环境就绪 ✓')
''',
        7: r'''# ========== 第1步：下载数据并算双均线 ==========
raw = yf.download(TICKER, period=PERIOD, progress=False, multi_level_index=False)
df = raw[['Close']].dropna().copy()
df.columns = ['Close']

df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()
df['signal'] = (df['MA5'] > df['MA20']).astype(int)  # 收盘算出的「理论信号」

# ========== 第2步：信号推迟一天，避免用未来数据 ==========
df['position'] = df['signal'].shift(1).fillna(0).astype(int)  # 今天实际仓位

# ========== 第3步：标记买入、卖出日 ==========
df['position_change'] = df['position'].diff().fillna(0)  # 仓位变化：0→1买，1→0卖
df['action'] = ''
df.loc[df['position_change'] > 0, 'action'] = '买入'
df.loc[df['position_change'] < 0, 'action'] = '卖出'

trades = df[df['action'] != '']
print(f'标的 {TICKER}，共 {len(df)} 个交易日')
print(f'模拟交易：买入 { (df["action"]=="买入").sum() } 次，卖出 { (df["action"]=="卖出").sum() } 次')
print('\n最近几次调仓：')
display(trades[['Close', 'MA5', 'MA20', 'position', 'action']].tail(6))
''',
        8: r'''# ========== 价格+均线 + 持仓时间条 ==========
fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True,
                         gridspec_kw={'height_ratios': [2.5, 1]})

axes[0].plot(df.index, df['Close'], color='gray', linewidth=1, label='收盘价')
axes[0].plot(df.index, df['MA5'], color='tab:orange', linewidth=1.2, label='MA5')
axes[0].plot(df.index, df['MA20'], color='tab:blue', linewidth=1.5, label='MA20')
axes[0].set_ylabel('价格')
axes[0].set_title(f'{TICKER}：双均线策略 —— 什么时候持仓？', fontsize=14)
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

axes[1].fill_between(df.index, 0, df['position'], step='post', alpha=0.4, color='green')
axes[1].set_ylim(-0.1, 1.2)
axes[1].set_yticks([0, 1])
axes[1].set_yticklabels(['空仓', '持仓'])
axes[1].set_xlabel('日期')
axes[1].set_ylabel('仓位')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print('绿色区域 = 持仓（买入后、卖出前）| 空白 = 空仓')
''',
        10: r'''# ========== 算日收益率 ==========
df['ret'] = df['Close'].pct_change().fillna(0)  # 股票本身每天涨跌

# ========== 策略收益：只有持仓日才吃到涨跌 ==========
df['strategy_ret'] = df['position'] * df['ret']

# ========== 基准1：买入持有（一直满仓）==========
df['buyhold_ret'] = df['ret']

# ========== 基准2：同期持有大盘 SPY ==========
spy = yf.download(BENCHMARK, period=PERIOD, progress=False, multi_level_index=False)[['Close']]
spy.columns = ['SPY_Close']
df = df.join(spy, how='inner')  # 按日期对齐，只保留两边都有数据的行
df['market_ret'] = df['SPY_Close'].pct_change().fillna(0)

# ========== 累计净值：从 1 元钱出发连乘 ==========
df['nav_strategy'] = (1 + df['strategy_ret']).cumprod()
df['nav_buyhold'] = (1 + df['buyhold_ret']).cumprod()
df['nav_market'] = (1 + df['market_ret']).cumprod()

total_strategy = df['nav_strategy'].iloc[-1] - 1
total_buyhold = df['nav_buyhold'].iloc[-1] - 1
total_market = df['nav_market'].iloc[-1] - 1

print('=== 样本期累计收益（不含手续费，仅供学习）===')
print(f'  双均线策略 ({TICKER}): {total_strategy:+.2%}')
print(f'  买入持有 ({TICKER}):     {total_buyhold:+.2%}')
print(f'  买入持有 ({BENCHMARK} 大盘): {total_market:+.2%}')
''',
        12: r'''# ========== 三条净值曲线对比（回测高潮图）==========
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df.index, df['nav_strategy'], linewidth=2.2, color='tab:purple',
        label=f'双均线策略 ({TICKER})')
ax.plot(df.index, df['nav_buyhold'], linewidth=1.8, color='tab:blue', alpha=0.85,
        label=f'买入持有 ({TICKER})')
ax.plot(df.index, df['nav_market'], linewidth=1.8, color='tab:gray', linestyle='--',
        label=f'买入持有 ({BENCHMARK} 大盘)')

ax.axhline(1.0, color='black', linewidth=0.6, linestyle=':', alpha=0.5)
ax.set_title(f'回测净值曲线：策略 vs 标的 vs 大盘（{PERIOD}）', fontsize=14)
ax.set_xlabel('日期')
ax.set_ylabel('净值（起点=1）')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
        13: r'''# ========== 近12个月局部放大 ==========
recent = df.last('12M') if len(df) > 200 else df.tail(200)

plt.figure(figsize=(14, 5))
plt.plot(recent.index, recent['nav_strategy'], linewidth=2, label='双均线策略')
plt.plot(recent.index, recent['nav_buyhold'], linewidth=1.6, label=f'买入持有 {TICKER}')
plt.plot(recent.index, recent['nav_market'], linewidth=1.6, linestyle='--', label=f'买入持有 {BENCHMARK}')
plt.title('近 12 个月：策略 vs 基准（局部）', fontsize=14)
plt.xlabel('日期')
plt.ylabel('净值')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
        15: r'''# ========== 统计胜率：一轮「买入→卖出」算一局 ==========
wins, losses = 0, 0       # 赢、输次数
entry_price = None        # 记住买入价
records = []              # 存每轮结果

for date, row in df.iterrows():  # 按天遍历整张表
    if row['action'] == '买入':
        entry_price = row['Close']   # 记录买入当天的收盘价
    elif row['action'] == '卖出' and entry_price is not None:
        pnl = row['Close'] / entry_price - 1   # 本轮收益率
        if pnl > 0:
            wins += 1
            outcome = '赢'
        else:
            losses += 1
            outcome = '输'
        records.append({
            '卖出日': date.strftime('%Y-%m-%d'),
            '买入价': round(entry_price, 2),
            '卖出价': round(row['Close'], 2),
            '本轮收益': f'{pnl:+.2%}',
            '结果': outcome,
        })
        entry_price = None   # 本轮结束，清空买入价

total_rounds = wins + losses
win_rate = wins / total_rounds if total_rounds > 0 else np.nan

print(f'完整交易回合：{total_rounds} 轮')
print(f'  赢：{wins} 次')
print(f'  输：{losses} 次')
print(f'  胜率：{win_rate:.1%}' if total_rounds > 0 else '  暂无完整买卖回合')

if records:
    display(pd.DataFrame(records).tail(8))
''',
        17: r'''# ========== 最大回撤：从历史最高点最多跌了多少 ==========
def max_drawdown(nav_series):
    """输入净值序列，返回 (最大回撤比例, 每日回撤序列)。"""
    peak = nav_series.cummax()           # 到每一天为止的历史最高净值
    drawdown = nav_series / peak - 1     # 当前净值相对峰值的跌幅
    return drawdown.min(), drawdown

mdd_strategy, dd_strategy = max_drawdown(df['nav_strategy'])
mdd_buyhold, dd_buyhold = max_drawdown(df['nav_buyhold'])

print('=== 最大回撤（样本期内最深一次「从山顶滑落」）===')
print(f'  双均线策略: {mdd_strategy:.2%}')
print(f'  买入持有 ({TICKER}): {mdd_buyhold:.2%}')

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(df.index, dd_strategy * 100, 0, alpha=0.35, color='tab:purple', label='策略回撤 %')
ax.plot(df.index, dd_strategy * 100, color='tab:purple', linewidth=1)
ax.set_title(f'策略回撤示意图（最大回撤 = {mdd_strategy:.2%}）', fontsize=14)
ax.set_xlabel('日期')
ax.set_ylabel('相对历史高点的跌幅 (%)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
''',
    },
}
