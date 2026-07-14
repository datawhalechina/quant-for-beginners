"""Generate Phase 2 notebook skeletons for notebooks/phase2_intro/."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "phase2_intro"

COVER = (
    '<p align="center">\n'
    '  <img src="./yibo-quant.jpg" alt="课程封面" width="1300"/>\n'
    "</p>\n"
)

ENV_CODE = """\
# ========== 环境准备：导入库并设置画图中文 ==========
import warnings
warnings.filterwarnings('ignore')

import statistics as stats   # 标准库：描述统计
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']

TRADING_DAYS = 252   # 年化常用交易日数
print('环境就绪 ✓')
"""


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def notebook(cells: list) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }


def header(chapter_num: int, title: str) -> list:
    return [
        md(COVER),
        md(
            f"# 《和Yibo零基础学习量化金融》\n"
            f"## 从Python到AI量化交易实战 第二期\n"
            f"### 第{chapter_num}章：{title}"
        ),
    ]


def env_section(extra: str = "") -> list:
    src = ENV_CODE
    if extra:
        src = src.rstrip() + "\n\n" + extra + "\n"
    return [
        md("### 环境准备\n\n运行下面这个代码块一次即可。如果提示缺少库，在项目根目录执行：`pip install -r requirements.txt`"),
        code(src),
    ]


NOTEBOOKS = [
    {
        "file": "01_理解波动率.ipynb",
        "chapter": 5,
        "title": "理解波动率",
        "intro": """\
---

## 本章你将学会

- ✅ 用金融语言解释 **波动率**（不是纯数学 std）
- ✅ 区分 **历史波动率** 与 **滚动波动率**
- ✅ 用 **pandas** 计算日收益率与滚动标准差
- ✅ 把日波动 **年化**（× √252 的直觉）
- ✅ 对比 **苹果 vs 特斯拉** 的波动「脾气」

**当前等级**
🎮 **Lv.4 风险观察员**

**本章难度**
⭐⭐☆☆☆

**预计学习时间**
30～45 分钟（需联网）

**前置知识**

- 完成 **第一期全部四章**（尤其第二章的收益率与 Histogram）
- Python 基础、会用 Jupyter

---

第二期从这里开始。

第一期你已经会用 **标准差** 粗比三只股票谁更「颠」。这一章我们把这件事说准确：**波动率 = 收益率的不确定性**，是量化里最重要的风险语言之一。

> 提示：文末有 **🎯 挑战任务**——换一只你关注的股票，算它的年化波动率。
""",
        "sections": [
            (
                "5.1 波动率到底是什么？",
                """\
---

### 5.1 波动率到底是什么？

先忘掉公式，听一个生活例子：

- 股票 A：最近一年大多数时候每天涨跌在 **±0.5%** 附近晃
- 股票 B：经常 **±3%** 甚至 **±5%** 乱跳

即使两只股票 **平均收益差不多**，你也会觉得 B **更刺激、更危险**——这种「上下晃动的幅度」，就是 **波动率（Volatility）** 要描述的东西。

在量化里有一个非常实用的近似：

> **历史波动率 ≈ 日收益率的标准差**

第一期第二章你已经算过 `returns.std()`，本章只是把它 **命名、年化、画成时间序列**。
""",
                """\
# ========== 下载苹果与特斯拉，计算日收益率 ==========
tickers = ['AAPL', 'TSLA']
period = '2y'

prices = yf.download(tickers, period=period, progress=False)['Close']
returns = prices.pct_change().dropna()

print('收益率表前几行：')
display(returns.head())

for t in tickers:
    daily_vol = returns[t].std()
    ann_vol = daily_vol * np.sqrt(TRADING_DAYS)
    print(f'{t}  日波动 ≈ {daily_vol:.2%}  |  年化波动 ≈ {ann_vol:.2%}')
""",
            ),
            (
                "5.2 为什么要年化？",
                """\
---

### 5.2 为什么要年化？

日波动 1.5% 和 2.5% 不好直观比较「一年到底多颠」。业界习惯把日波动 **放大到一年尺度**：

$$
\\text{年化波动率} \\approx \\text{日波动率} \\times \\sqrt{252}
$$

**直觉**：252 是大约一年的交易日数；波动按「随机游走」累积时，幅度随时间的平方根增长（先记住结论即可）。

下面用 **statistics** 标准库和 **numpy** 各算一遍，结果应一致——工具不同，金融含义相同。
""",
                """\
# ========== 年化波动率：statistics vs numpy ==========
aapl_rets = returns['AAPL'].dropna()

vol_numpy = aapl_rets.std()
vol_stats = stats.pstdev(aapl_rets)   # 总体标准差；与 pandas 默认 ddof=1 略有差异

print(f'numpy std (样本):     {vol_numpy:.4%}')
print(f'statistics pstdev:    {vol_stats:.4%}')
print(f'年化 (numpy):         {vol_numpy * np.sqrt(TRADING_DAYS):.2%}')
""",
            ),
            (
                "5.3 滚动波动率：风险会变",
                """\
---

### 5.3 滚动波动率：风险会变

**一个数字概括不了整段历史。** 2020 年疫情、2022 年加息——市场「脾气」会变。

**滚动波动率** = 在最近 N 天里重新算一遍标准差，然后画成曲线。常用 **20 日** 或 **60 日** 窗口。

下面用 `pandas` 的 `.rolling().std()` 画出两只股票的 **60 日滚动波动率**。
""",
                """\
# ========== 60 日滚动波动率 ==========
window = 60
rolling_vol = returns.rolling(window).std() * np.sqrt(TRADING_DAYS)

fig, ax = plt.subplots(figsize=(12, 4.5))
for t, c in zip(tickers, ['#007AFF', '#E82127']):
    ax.plot(rolling_vol.index, rolling_vol[t], label=f'{t} ({window}日滚动, 年化)', color=c, linewidth=1.2)

ax.set_title(f'{window} 日滚动年化波动率：苹果 vs 特斯拉', fontsize=14)
ax.set_ylabel('年化波动率')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
""",
            ),
            (
                "5.4 波动率与价格：两张图一起看",
                """\
---

### 5.4 波动率与价格：两张图一起看

专业分析师常把 **价格走势** 和 **波动率** 上下对照：

- 价格大跌时，滚动波动率往往 **飙升**（恐慌）
- 横盘整理时，波动率往往 **回落**（平静）

这不是巧合——**风险与价格运动是一体两面**。
""",
                """\
# ========== 价格 + 滚动波动率 双面板 ==========
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                gridspec_kw={'height_ratios': [2, 1]})

for t, c in zip(tickers, ['#007AFF', '#E82127']):
    norm = prices[t] / prices[t].iloc[0]   # 归一化，方便同图对比
    ax1.plot(norm.index, norm, label=t, color=c, linewidth=1.2)
    ax2.plot(rolling_vol.index, rolling_vol[t], label=t, color=c, linewidth=1.0)

ax1.set_title('归一化价格 vs 60日滚动年化波动率', fontsize=14)
ax1.set_ylabel('归一化价格（起点=1）')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.set_ylabel('年化波动率')
ax2.set_xlabel('日期')
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
""",
            ),
        ],
        "challenge": """\
---

## 🎯 挑战任务（第五章通关）

1. **换标的**：把 `'NVDA'` 或 `'MSFT'` 加入对比，重画滚动波动率图。
2. **改窗口**：把 `window=60` 改成 `20`，观察曲线变「毛」还是变「滑」？
3. **思考题**：特斯拉年化波动通常高于苹果，如果你是保守型投资者，这对你选股有什么启示？
""",
        "summary": """\
## 本章总结

- **波动率** 描述收益的不确定性；历史波动率 ≈ 日收益率标准差。
- **年化** 让不同股票、不同报告口径可以放在同一尺度比较（× √252）。
- **滚动波动率** 告诉你风险随时间变化——恐慌时往往升高。
- 工具：`pandas.pct_change()`、`.rolling().std()`、`numpy.sqrt()`、`statistics`。

**下一章预告**：收益高不一定好——我们会引入 **夏普比率**，学习「每承担一单位风险，多赚多少」。
""",
    },
    {
        "file": "02_夏普比率与Beta.ipynb",
        "chapter": 6,
        "title": "夏普比率与 Beta",
        "intro": """\
---

## 本章你将学会

- ✅ 为什么 **只看收益率不够**（高风险高收益的陷阱）
- ✅ 计算 **夏普比率（Sharpe Ratio）** 并解读
- ✅ 理解 **Beta**：股票相对大盘的「敏感度」
- ✅ 用 **numpy** 算协方差，手推 Beta
- ✅ 给多只股票做 **风险收益散点图**

**当前等级**
🎮 **Lv.4 风险分析师**

**本章难度**
⭐⭐⭐☆☆

**预计学习时间**
30～45 分钟（需联网）

**前置知识**

- 完成 **第五章**（波动率、年化）
- 第一期 **第四章**（回测与基准对比）

---

假设两只股票：A 一年赚 30%，B 一年赚 15%。你会选 A 吗？

如果 A 的波动是 B 的 **三倍**，很多专业投资者反而更选 B——因为 A 的「性价比」可能更差。

这一章，我们学习两个最常用的 **风险指标**：**夏普比率** 和 **Beta**。
""",
        "sections": [
            (
                "6.1 夏普比率：性价比",
                """\
---

### 6.1 夏普比率：性价比

**夏普比率** 回答一个问题：

> 每多承担一单位风险，我比「无风险收益」多赚了多少？

简化版公式（初学者够用）：

$$
\\text{Sharpe} \\approx \\frac{\\text{年化收益} - \\text{无风险利率}}{\\text{年化波动率}}
$$

无风险利率可先用 **常数近似**（例如 4%），后面章节再细化。

**直觉**：Sharpe 越高，同样风险下赚得越多——像「性价比」。
""",
                """\
# ========== 下载数据，计算年化收益与 Sharpe ==========
tickers = ['AAPL', 'TSLA', 'NVDA', 'SPY']
period = '3y'
rf_annual = 0.04   # 近似无风险利率 4%

prices = yf.download(tickers, period=period, progress=False)['Close']
returns = prices.pct_change().dropna()

rows = []
for t in tickers:
    r = returns[t]
    ann_return = (1 + r.mean()) ** TRADING_DAYS - 1
    ann_vol = r.std() * np.sqrt(TRADING_DAYS)
    sharpe = (ann_return - rf_annual) / ann_vol
    rows.append({'股票': t, '年化收益': ann_return, '年化波动': ann_vol, 'Sharpe': sharpe})

summary = pd.DataFrame(rows).set_index('股票')
summary['年化收益'] = summary['年化收益'].map('{:.2%}'.format)
summary['年化波动'] = summary['年化波动'].map('{:.2%}'.format)
summary['Sharpe'] = summary['Sharpe'].map('{:.2f}'.format)
print('风险收益一览（近似 Sharpe）：')
display(summary)
""",
            ),
            (
                "6.2 风险收益散点图",
                """\
---

### 6.2 风险收益散点图

把每只股票画在 **横轴=波动、纵轴=收益** 的平面上，一眼看出：

- 左上角：低波动、高收益（理想，但少见）
- 右下角：高波动、低收益（性价比差）

**SPY** 代表大盘，常作对比基准。
""",
                """\
# ========== 风险-收益散点图 ==========
fig, ax = plt.subplots(figsize=(8, 6))

for t in tickers:
    r = returns[t]
    ann_return = (1 + r.mean()) ** TRADING_DAYS - 1
    ann_vol = r.std() * np.sqrt(TRADING_DAYS)
    ax.scatter(ann_vol, ann_return, s=120, label=t, zorder=3)
    ax.annotate(t, (ann_vol, ann_return), textcoords='offset points',
                xytext=(6, 6), fontsize=11)

ax.set_xlabel('年化波动率')
ax.set_ylabel('年化收益率')
ax.set_title('风险-收益散点图（样本约 3 年）', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()
""",
            ),
            (
                "6.3 Beta：相对大盘的敏感度",
                """\
---

### 6.3 Beta：相对大盘的敏感度

**Beta（β）** 衡量：大盘动 1%，这只股票平均动多少？

- β ≈ 1：跟大盘差不多
- β > 1：比大盘更「冲」（涨跌幅放大）
- β < 1：比大盘更「稳」

计算公式（用日收益率）：

$$
\\beta = \\frac{\\text{Cov}(R_{\\text{股票}}, R_{\\text{大盘}})}{\\text{Var}(R_{\\text{大盘}})}
$$

下面用 **numpy** 的 `cov` 手算，再与 pandas 对照。
""",
                """\
# ========== 计算 Beta（相对 SPY）==========
market = returns['SPY']
stocks = ['AAPL', 'TSLA', 'NVDA']

beta_rows = []
for t in stocks:
    stock = returns[t]
    cov_matrix = np.cov(stock, market)
    beta_numpy = cov_matrix[0, 1] / cov_matrix[1, 1]
    beta_pandas = stock.cov(market) / market.var()
    beta_rows.append({'股票': t, 'Beta(numpy)': beta_numpy, 'Beta(pandas)': beta_pandas})

beta_df = pd.DataFrame(beta_rows).set_index('股票')
print('Beta 相对 SPY：')
display(beta_df.map('{:.2f}'.format))
""",
            ),
            (
                "6.4 用 statistics 看收益分布",
                """\
---

### 6.4 用 statistics 看收益分布

**statistics** 是 Python 标准库，不需要额外安装。除了均值、标准差，还可以看 **中位数**——当某天极端涨跌把均值「拉歪」时，中位数更稳健。

金融数据分析 ≠ 只会 pandas；标准库在快速验证时很方便。
""",
                """\
# ========== statistics 描述 AAPL 日收益 ==========
aapl = returns['AAPL'].dropna().tolist()

print(f'均值:   {stats.mean(aapl):.4%}')
print(f'中位数: {stats.median(aapl):.4%}')
print(f'标准差: {stats.pstdev(aapl):.4%}')
print(f'最大单日涨: {max(aapl):.2%}')
print(f'最大单日跌: {min(aapl):.2%}')
""",
            ),
        ],
        "challenge": """\
---

## 🎯 挑战任务（第六章通关）

1. **扩充名单**：再加 `'MSFT'`、`'GOOGL'`，按 Sharpe 从高到低排序。
2. **Beta 实验**：算 `'JPM'`（银行）相对 SPY 的 Beta，和 NVDA 比，谁更贴近大盘？
3. **思考题**：Sharpe 高是否意味着未来一定更好？（提示：回顾第一期「回测不是算命」）
""",
        "summary": """\
## 本章总结

- **夏普比率** = 风险调整后的「性价比」；不能只看绝对收益。
- **Beta** 描述相对大盘的敏感度；用协方差 / 大盘方差即可手算。
- **散点图** 是沟通风险收益最直观的方式之一。
- `numpy.cov`、`statistics`、`pandas` 可以交叉验证同一指标。

**下一章预告**：我们会深入 **最大回撤**，并初探 **仓位管理**——同样策略，买多少可能决定生死。
""",
    },
    {
        "file": "03_最大回撤与仓位管理.ipynb",
        "chapter": 7,
        "title": "最大回撤与仓位管理",
        "intro": """\
---

## 本章你将学会

- ✅ 从第一期回测出发，**深入理解最大回撤**
- ✅ 画 **水下曲线（Underwater Plot）** 看「坑有多深、多久爬出来」
- ✅ 理解 **仓位（Position Sizing）** 为什么和策略同样重要
- ✅ 用代码对比 **满仓 vs 半仓** 对净值曲线的影响
- ✅ 建立「先想能亏多少，再想能赚多少」的风险意识

**当前等级**
🎮 **Lv.5 仓位管理员**

**本章难度**
⭐⭐⭐☆☆

**预计学习时间**
30～45 分钟（需联网）

**前置知识**

- 完成 **第一期第四章**（回测、最大回撤初识）
- 完成 **第五～六章**（波动率、Sharpe）

---

第一期你已经见过 **最大回撤** 这个数字。这一章我们把它 **拆开、画出来、和仓位挂钩**。

专业交易员常说：**策略决定方向，仓位决定生死。**
""",
        "sections": [
            (
                "7.1 最大回撤：账户最深的坑",
                """\
---

### 7.1 最大回撤：账户最深的坑

**回撤（Drawdown）** = 从历史最高点往下掉了多少比例。

**最大回撤（Max Drawdown）** = 整段样本里，最深的那一次「坑」。

例子：净值从 1.5 跌到 1.0，回撤 = (1.0 - 1.5) / 1.5 = **-33%**。

它回答的问题不是「赚多少」，而是：**最惨时你会经历什么？** 这决定你能不能扛到策略恢复。
""",
                """\
# ========== 下载 AAPL，构造买入持有净值 ==========
ticker = 'AAPL'
period = '3y'

prices = yf.download(ticker, period=period, progress=False)['Close']
returns = prices.pct_change().dropna()
equity = (1 + returns).cumprod()   # 买入持有净值曲线

# 计算回撤序列
running_max = equity.cummax()
drawdown = equity / running_max - 1
max_dd = drawdown.min()

print(f'{ticker} 买入持有 最大回撤: {max_dd:.2%}')
print(f'回撤最深日期: {drawdown.idxmin().date()}')
""",
            ),
            (
                "7.2 水下曲线",
                """\
---

### 7.2 水下曲线（Underwater Plot）

把 **回撤序列** 画成填充图，俗称 **水下曲线**——你在水面下待得越久，心理压力越大。

好的策略不仅要回撤浅，还要 **恢复快**（后面因子、组合章节会继续用）。
""",
                """\
# ========== 净值 + 水下曲线 ==========
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                gridspec_kw={'height_ratios': [2, 1]})

ax1.plot(equity.index, equity, color='#007AFF', linewidth=1.5)
ax1.plot(running_max.index, running_max, color='gray', linestyle='--', alpha=0.6, label='历史最高')
ax1.set_title(f'{ticker} 买入持有净值 & 回撤（水下曲线）', fontsize=14)
ax1.set_ylabel('净值（起点=1）')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.fill_between(drawdown.index, drawdown, 0, color='#E82127', alpha=0.5)
ax2.axhline(max_dd, color='black', linestyle=':', label=f'最大回撤 {max_dd:.1%}')
ax2.set_ylabel('回撤')
ax2.set_xlabel('日期')
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
""",
            ),
            (
                "7.3 仓位管理：同样策略，不同结果",
                """\
---

### 7.3 仓位管理：同样策略，不同结果

**仓位** = 你投入多少比例的资金。

简化模型（本章够用）：

- **满仓**：100% 资金跟着策略走 → 收益和回撤都「满格」
- **半仓**：50% 资金参与 → 收益和回撤大约 **减半**

真实交易还要考虑手续费、杠杆、加仓规则——这里先建立直觉。
""",
                """\
# ========== 双均线策略：满仓 vs 半仓 ==========
ma_short, ma_long = 5, 20

df = pd.DataFrame({'Close': prices, 'Return': returns})
df['MA5'] = df['Close'].rolling(ma_short).mean()
df['MA20'] = df['Close'].rolling(ma_long).mean()
df['Position'] = (df['MA5'] > df['MA20']).astype(float)
df['StrategyRet'] = df['Position'].shift(1) * df['Return']
df = df.dropna()

# 满仓 vs 半仓
df['Equity_100'] = (1 + df['StrategyRet']).cumprod()
df['Equity_50'] = (1 + df['StrategyRet'] * 0.5).cumprod()
df['Equity_BH'] = (1 + df['Return']).cumprod()

def max_drawdown(equity_series):
    dd = equity_series / equity_series.cummax() - 1
    return dd.min()

print('最大回撤对比：')
for name, col in [('双均线满仓', 'Equity_100'), ('双均线半仓', 'Equity_50'), ('买入持有', 'Equity_BH')]:
    print(f'  {name}: {max_drawdown(df[col]):.2%}')
""",
            ),
            (
                "7.4 三条净值曲线对比",
                """\
---

### 7.4 三条净值曲线对比

同一段行情、同一套 MA 规则——**只改仓位**，曲线形态就会变。

半仓可能 **少赚**，但也 **少亏、少回撤**。没有免费午餐，只有适合你的风险预算。
""",
                """\
# ========== 净值曲线对比图 ==========
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df.index, df['Equity_100'], label='双均线 · 满仓', linewidth=1.5)
ax.plot(df.index, df['Equity_50'], label='双均线 · 半仓', linewidth=1.5)
ax.plot(df.index, df['Equity_BH'], label='买入持有', linewidth=1.2, linestyle='--', alpha=0.8)

ax.set_title(f'{ticker} 双均线策略：仓位如何改变曲线', fontsize=14)
ax.set_ylabel('净值')
ax.set_xlabel('日期')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
""",
            ),
        ],
        "challenge": """\
---

## 🎯 挑战任务（第七章通关）

1. **换策略参数**：把 MA 改成 10/30，比较满仓与 30% 仓位的最大回撤。
2. **算恢复时间**：最大回撤发生后的 **60 个交易日** 内，净值是否回到前高？（用代码或肉眼估计均可）
3. **思考题**：如果你只能承受 -15% 回撤，本章实验里哪种仓位更合适？
""",
        "summary": """\
## 本章总结

- **最大回撤** 衡量「最深的那次坑」；比最终赚多少更能反映持仓体验。
- **水下曲线** 把回撤可视化，方便看深度与持续时间。
- **仓位管理** 是独立于选股的第二杠杆：同样信号，不同仓位 → 不同命运。
- 先设定 **可承受回撤**，再反推合理仓位——这是专业风控的起点。

**下一章预告**：把视野从 **单只股票** 扩展到 **多标的组合**——相关性、分散投资，Coming next。
""",
    },
    {
        "file": "04_多标的组合与相关性.ipynb",
        "chapter": 8,
        "title": "多标的组合与相关性",
        "intro": """\
---

## 本章你将学会

- ✅ 一次下载 **多只股票 + 大盘**，对齐成一张表
- ✅ 计算 **相关性矩阵（Correlation Matrix）**
- ✅ 画 **热力图** 读懂谁和谁「同涨同跌」
- ✅ 构造 **等权组合**，对比单票 vs 组合的波动
- ✅ 用直觉理解 **分散投资（Diversification）**

**当前等级**
🎮 **Lv.5 组合分析师**

**本章难度**
⭐⭐⭐☆☆

**预计学习时间**
35～45 分钟（需联网）

**前置知识**

- 完成 **第二～七章**
- 第一期 **第二章**（多标的 `pct_change`）

---

「不要把鸡蛋放在同一个篮子里」——这句话人人都听过。

这一章我们用 **数据** 而不是口号来验证：当几只股票 **不完全同涨同跌** 时，组合波动往往 **低于** 任意单票。

这是 **多标的分析** 的核心，也是量化组合研究的起点。
""",
        "sections": [
            (
                "8.1 多标的数据一张表",
                """\
---

### 8.1 多标的：一张表对齐

量化里常同时看 **科技 + 消费 + 大盘 + 债券代理** 等。第一步：下载收盘价，算日收益率，**列 = 标的、行 = 日期**。

下面选 5 只常见标的（可自行替换）：

| 代码 | 含义 |
|------|------|
| AAPL | 苹果 |
| MSFT | 微软 |
| JPM | 摩根大通 |
| XLE | 能源 ETF |
| SPY | 标普500 |
""",
                """\
# ========== 下载多标的并对齐 ==========
tickers = ['AAPL', 'MSFT', 'JPM', 'XLE', 'SPY']
period = '3y'

prices = yf.download(tickers, period=period, progress=False)['Close']
returns = prices.pct_change().dropna()

print(f'样本: {len(returns)} 个交易日 × {len(tickers)} 只标的')
display(returns.head())
""",
            ),
            (
                "8.2 相关性矩阵",
                """\
---

### 8.2 相关性矩阵

**相关系数 ρ** 介于 -1 和 1 之间：

- **ρ ≈ 1**：几乎同涨同跌（分散效果差）
- **ρ ≈ 0**：关系不大（分散可能有帮助）
- **ρ ≈ -1**：往往一涨一跌（对冲直觉，实际少见）

`pandas.DataFrame.corr()` 一行搞定。
""",
                """\
# ========== 相关性矩阵 ==========
corr = returns.corr()
print('日收益率相关系数：')
display(corr.round(2))
""",
            ),
            (
                "8.3 热力图",
                """\
---

### 8.3 热力图：一眼读懂关系

热力图是 Phase 2 的 **成果图之一**——建议截图保存。

颜色越深（绝对值越大），关系越强。你会看到 **AAPL 与 MSFT 往往高度相关**，而 **XLE（能源）** 可能与科技股没那么同步。
""",
                """\
# ========== 相关性热力图（matplotlib 纯实现）==========
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1)

ax.set_xticks(range(len(tickers)))
ax.set_yticks(range(len(tickers)))
ax.set_xticklabels(tickers)
ax.set_yticklabels(tickers)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

for i in range(len(tickers)):
    for j in range(len(tickers)):
        ax.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center', color='black', fontsize=10)

ax.set_title('多标的日收益率相关性热力图', fontsize=14)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.show()
""",
            ),
            (
                "8.4 等权组合 vs 单票波动",
                """\
---

### 8.4 等权组合 vs 单票波动

**等权组合** = 每只股票占 **相同权重**（这里 4 只股票各 25%，不含 SPY 基准）。

若它们不完全相关，组合波动往往 **低于** 单票平均——这就是 **分散化红利** 的数学来源。

下面用 **numpy** 算组合日收益，再与 AAPL 单票对比。
""",
                """\
# ========== 等权组合波动 vs 单票 ==========
portfolio_tickers = ['AAPL', 'MSFT', 'JPM', 'XLE']
port_returns = returns[portfolio_tickers].mean(axis=1)   # 等权：逐行平均

comparison = {}
for t in portfolio_tickers:
    comparison[t] = returns[t].std() * np.sqrt(TRADING_DAYS)
comparison['等权组合'] = port_returns.std() * np.sqrt(TRADING_DAYS)

comp_series = pd.Series(comparison).sort_values()
print('年化波动率对比：')
display(comp_series.map('{:.2%}'.format))

fig, ax = plt.subplots(figsize=(8, 4.5))
comp_series.sort_values(ascending=True).plot(kind='barh', ax=ax, color='#007AFF', alpha=0.85)
ax.set_xlabel('年化波动率')
ax.set_title('单票 vs 等权组合：波动对比', fontsize=14)
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.show()
""",
            ),
            (
                "8.5 组合净值曲线",
                """\
---

### 8.5 组合净值曲线

最后把 **等权组合** 与 **SPY 大盘** 净值画在一起——第二期收官图。

注意：这里没有做再平衡、没有手续费，仍是 **教学级简化模型**；但足够建立「多标的思维」。
""",
                """\
# ========== 等权组合 vs SPY 净值 ==========
equity_port = (1 + port_returns).cumprod()
equity_spy = (1 + returns['SPY']).cumprod()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(equity_port.index, equity_port, label='等权组合 (AAPL+MSFT+JPM+XLE)', linewidth=1.5)
ax.plot(equity_spy.index, equity_spy, label='SPY 大盘', linewidth=1.5, linestyle='--')

ax.set_title('等权组合 vs 标普500：净值对比（样本约 3 年）', fontsize=14)
ax.set_ylabel('净值（起点=1）')
ax.set_xlabel('日期')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
""",
            ),
        ],
        "challenge": """\
---

## 🎯 挑战任务（第八章 · 第二期通关）

1. **自建组合**：选 3 只你熟悉的股票 + SPY，重画热力图。
2. **找低相关**：在热力图里找 **相关系数最低** 的一对，思考能否用来分散风险。
3. **不等权实验**：试试 `0.5*AAPL + 0.5*MSFT`  vs  四票等权，哪个波动更高？
4. **截图打卡**：保存热力图 + 组合净值图——这是你 **Lv.5 组合分析师** 的通关证明。
""",
        "summary": """\
## 本章总结

- **多标的分析** 从「对齐数据表」开始；列是标的，行是日期。
- **相关性** 量化「同涨同跌」程度；热力图是最常见的展示方式。
- **等权组合** 在标的不完全相关时，波动往往低于单票——分散投资的数学直觉。
- 第二期完结！你已掌握：**波动率 → Sharpe/Beta → 回撤与仓位 → 组合与相关性**。

**第三期预告（规划）**：因子选股、更系统的组合优化，以及 AI 量化入门——Stay tuned。
""",
    },
]


def build_nb(spec: dict) -> dict:
    cells = header(spec["chapter"], spec["title"])
    cells.append(md(spec["intro"]))
    cells.extend(env_section())
    for _, md_text, code_text in spec["sections"]:
        cells.append(md(md_text))
        cells.append(code(code_text))
    cells.append(md(spec["challenge"]))
    cells.append(code(""))  # 留白给读者写挑战代码
    cells.append(md(spec["summary"]))
    return notebook(cells)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in NOTEBOOKS:
        path = OUT / spec["file"]
        with path.open("w", encoding="utf-8") as f:
            json.dump(build_nb(spec), f, ensure_ascii=False, indent=1)
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
