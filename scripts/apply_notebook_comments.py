# -*- coding: utf-8 -*-
"""为 phase1 四个 Notebook 的代码单元添加逐行中文注释。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks" / "phase1_intro"

# 格式：文件名 -> { 单元格序号: 带注释的完整源码 }
SOURCES: dict[str, dict[int, str]] = {}

SOURCES["01_什么是量化金融.ipynb"] = {
    5: r'''# ========== 导入本实验需要的库 ==========
import numpy as np              # 做数值计算（随机数、累乘价格等）
import pandas as pd             # 处理表格数据（像 Excel 一张表）
import matplotlib.pyplot as plt   # 画折线图、对比图

# ========== 让图表能正确显示中文 ==========
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']
np.random.seed(7)                             # 固定随机种子：每次运行随机数相同，方便对照

# ========== 第1步：模拟三段行情（涨→跌→恢复）==========
n1, n2, n3 = 90, 40, 120                      # 三个阶段分别有多少个交易日
ret = np.r_[                                    # 把三段「日收益率」拼成一条长数组
    np.random.normal(0.0010, 0.010, n1),        # 阶段1：平均每天略涨，波动较小
    np.random.normal(-0.012, 0.015, n2),       # 阶段2：平均每天偏跌，波动更大
    np.random.normal(0.0012, 0.012, n3)        # 阶段3：震荡恢复
]
price = 100 * np.cumprod(1 + ret)              # 起点100元，每天按 (1+收益率) 连乘得到价格

# ========== 第2步：做成 DataFrame，并算每日涨跌比例 ==========
df = pd.DataFrame({"close": price})            # 把价格放进表格，列名叫 close
df["ret"] = df["close"].pct_change().fillna(0) # pct_change = 日收益率；第一天填 0

# ========== 第3步：量化规则——收盘价在20日均线上方就持有 ==========
df["ma20"] = df["close"].rolling(20).mean()    # rolling(20).mean() = 20日移动平均线
df["signal_quant"] = (df["close"] > df["ma20"]).astype(int)  # 高于均线记1，否则记0

# ========== 第4步：随机买卖策略（对照组，乱买乱卖）==========
rng = np.random.default_rng(7)                 # 随机数生成器（种子7）
df["signal_random"] = rng.integers(0, 2, size=len(df))  # 每天随机 0 或 1

# ========== 第5步：算各策略的日收益（信号用昨天的，避免偷看未来）==========
df["ret_quant"] = df["signal_quant"].shift(1).fillna(0) * df["ret"]    # 量化策略收益
df["ret_random"] = df["signal_random"].shift(1).fillna(0) * df["ret"]  # 随机策略收益
df["ret_buyhold"] = df["ret"]                                          # 买入并持有：天天在场

# ========== 第6步：把日收益连乘成「净值曲线」（起点相当于1块钱）==========
for col in ["ret_quant", "ret_random", "ret_buyhold"]:   # 遍历三种收益列
    df[f"nav_{col}"] = (1 + df[col]).cumprod()         # (1+r) 连乘 = 累计净值

# ========== 第7步：画图——上图价格+均线，下图三种净值 ==========
fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)  # 2行1列子图，共用横轴

axes[0].plot(df["close"], label="Price", color="black", linewidth=1.4)  # 模拟收盘价
axes[0].plot(df["ma20"], label="MA20", color="tab:blue", alpha=0.9)     # 20日均线
axes[0].set_title("模拟市场价格与均线")                                  # 子图标题
axes[0].legend()                                                        # 显示图例

axes[1].plot(df["nav_ret_buyhold"], label="买入并持有", linewidth=2)       # 买入持有净值
axes[1].plot(df["nav_ret_quant"], label="量化规则策略", linewidth=2)     # 规则策略净值
axes[1].plot(df["nav_ret_random"], label="随机买卖", linewidth=2, alpha=0.85)  # 随机策略
axes[1].set_title("三种方法的净值对比")
axes[1].legend()

plt.tight_layout()   # 自动调整子图间距，避免标签被裁切
plt.show()           # 在 Notebook 里显示图片
''',
    20: r'''# ========== 导入库 ==========
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']

np.random.seed(42)          # 固定随机数，结果可复现
days = 120                  # 一共模拟 120 个交易日
daily_returns = np.random.normal(loc=0.0008, scale=0.02, size=days)  # 每天随机收益率
price = 100 * np.cumprod(1 + daily_returns)     # 从100元出发连乘成价格序列

df = pd.DataFrame({
    '收盘价': price,                              # 原始模拟收盘价
    '5日均线': pd.Series(price).rolling(5).mean(),   # 最近5天均价
    '20日均线': pd.Series(price).rolling(20).mean()  # 最近20天均价
})

plt.figure(figsize=(12, 5))                     # 创建画布，宽12高5英寸
plt.plot(df['收盘价'], label='收盘价', alpha=0.6, linewidth=1)
plt.plot(df['5日均线'], label='5日均线 (MA5)', linewidth=1.5)
plt.plot(df['20日均线'], label='20日均线 (MA20)', linewidth=1.5)
plt.fill_between(range(days), df['5日均线'], df['20日均线'], alpha=0.1, color='orange')  # 两线之间浅色填充
plt.title('Python 模拟股价走势 + 移动平均线', fontsize=14)
plt.xlabel('交易日')                             # 横轴说明
plt.ylabel('价格')
plt.legend()                                    # 图例
plt.grid(True, alpha=0.3)                       # 浅色网格，方便读数
plt.tight_layout()
plt.show()

print(f"起始价格: ¥{price[0]:.2f}")              # 第一天价格
print(f"最终价格: ¥{price[-1]:.2f}")              # 最后一天价格
print(f"区间收益率: {(price[-1]/price[0] - 1)*100:.2f}%")  # 整段涨跌幅
print(f"最大回撤价格: ¥{price.min():.2f}")        # 期间最低价
print(f"最高价格: ¥{price.max():.2f}")            # 期间最高价
''',
    27: r'''# ========== 实验一：布朗运动 / 随机游走 ==========
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']

n_stocks = 50               # 模拟 50 只「虚拟股票」
n_days = 250                # 每只走 250 个交易日（约一年）
start_price = 100           # 起始价都是 100 元
daily_volatility = 0.02     # 日波动强度（标准差约2%）

fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # 1行3列，三个子图

# --- 左图：画出 50 条价格路径 ---
all_paths = []              # 用来存每只股票的路径
for _ in range(n_stocks):   # 循环 50 次，每只股一条路径
    daily_returns = np.random.normal(0, daily_volatility, n_days)  # 每天随机收益
    price_path = start_price * np.cumprod(1 + daily_returns)       # 价格连乘
    all_paths.append(price_path)          # 存入列表
    axes[0].plot(price_path, alpha=0.3, linewidth=0.8)  # 画在左图，半透明

axes[0].axhline(y=start_price, color='red', linestyle='--', alpha=0.5, label='起始价 100元')  # 参考线
axes[0].set_title('50只虚拟股票的随机游走路径', fontsize=13)
axes[0].set_xlabel('交易日')
axes[0].set_ylabel('价格 (元)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# --- 中图：一年后的终点价格分布（直方图）---
final_prices = [path[-1] for path in all_paths]   # 取每条路径最后一天的价格
axes[1].hist(final_prices, bins=15, color='steelblue', edgecolor='white', alpha=0.8)
axes[1].axvline(x=start_price, color='red', linestyle='--', label=f'起始价 {start_price}元')
axes[1].axvline(x=np.mean(final_prices), color='orange', linestyle='-', linewidth=2,
                label=f'平均终点价 {np.mean(final_prices):.1f}元')
axes[1].set_title('1年后的终点价格分布', fontsize=13)
axes[1].set_xlabel('最终价格 (元)')
axes[1].set_ylabel('股票数量')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# --- 右图：验证「波动 ∝ 时间的平方根」---
time_points = [5, 10, 20, 50, 100, 150, 200, 250]  # 选取若干观察日
std_at_time = []                                    # 存放每个时点的价格标准差
for t in time_points:
    prices_at_t = [path[t-1] for path in all_paths]  # 所有股票在第 t 天的价格
    std_at_time.append(np.std(prices_at_t))         # 算标准差

sqrt_time = np.sqrt(time_points)                    # 时间开平方
scale = std_at_time[0] / sqrt_time[0]               # 缩放系数，让理论线对齐第一个点

axes[2].scatter(time_points, std_at_time, s=80, color='steelblue', zorder=5, label='实际波动(标准差)')
axes[2].plot(time_points, scale * sqrt_time, 'r--', linewidth=2, label='理论值: σ ∝ √t')
axes[2].set_title('波动率 vs 时间 (验证√t法则)', fontsize=13)
axes[2].set_xlabel('交易天数')
axes[2].set_ylabel('价格标准差 (元)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ========== 打印文字结论 ==========
print("=" * 60)
print("实验结论：")
print(f"  50只股票起始价均为 {start_price}元")
print(f"  1年后最高价: {max(final_prices):.2f}元")
print(f"  1年后最低价: {min(final_prices):.2f}元")
print(f"  1年后平均价: {np.mean(final_prices):.2f}元")
print(f"  价格标准差:  {np.std(final_prices):.2f}元")
print("-" * 60)
print("  → 每条路径完全不可预测（左图）")
print("  → 但大量路径的终点价格呈正态分布（中图）")
print("  → 波动幅度与时间平方根成正比（右图）——Regnault 1860年代的发现！")
print("=" * 60)
''',
    30: r'''# ========== 实验二：索普——概率优势 + 凯利仓位 ==========
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']

n_rounds = 1000             # 每位玩家模拟下注 1000 轮
n_simulations = 200         # 每种策略重复 200 次（看分布）
initial_capital = 1000      # 初始本金 1000 元

win_prob_no_edge = 0.50     # 玩家A：无优势，胜率 50%
win_prob_edge = 0.52        # 玩家B/C：有 2% 概率优势
payout_ratio = 1.0          # 赔率 1:1（赢一倍赌注，输一倍赌注）

# 凯利公式: f* = (bp - q) / b  → 最优下注占本金比例
kelly_fraction = (payout_ratio * win_prob_edge - (1 - win_prob_edge)) / payout_ratio
aggressive_fraction = 0.25  # 玩家C：有优势但每次下注 25%（太激进）


def simulate_player(win_prob, bet_fraction, n_sims=n_simulations):
    """模拟多人在 n_rounds 轮里的资金曲线。"""
    all_curves = []
    for _ in range(n_sims):              # 外层：重复很多次实验
        capital = initial_capital        # 本轮起始资金
        curve = [capital]              # 记录每轮后的资金
        for _ in range(n_rounds):      # 内层：一轮轮下注
            bet = capital * bet_fraction   # 本轮下注额 = 本金 × 比例
            if np.random.random() < win_prob:  # 随机数小于胜率 → 赢
                capital += bet * payout_ratio
            else:                              # 否则 → 输
                capital -= bet
            capital = max(capital, 0.01)       # 防止资金变成负数
            curve.append(capital)
        all_curves.append(curve)
    return np.array(all_curves)        # 转成二维数组：行=实验，列=轮次


curves_A = simulate_player(win_prob_no_edge, kelly_fraction)       # 无优势 + 凯利
curves_B = simulate_player(win_prob_edge, kelly_fraction)          # 有优势 + 凯利
curves_C = simulate_player(win_prob_edge, aggressive_fraction)     # 有优势 + 重仓

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))  # 三个玩家各一张子图

configs = [
    (curves_A, '玩家A: 无优势 (胜率50% + 凯利仓位)', 'red', f'胜率50%, 仓位{kelly_fraction*100:.1f}%'),
    (curves_B, '玩家B: 索普策略 (胜率52% + 凯利仓位)', 'green', f'胜率52%, 仓位{kelly_fraction*100:.1f}%'),
    (curves_C, '玩家C: 有优势但冒进 (胜率52% + 重仓)', 'goldenrod', f'胜率52%, 仓位25%'),
]

for ax, (curves, title, color, label) in zip(axes, configs):
    for i in range(min(30, n_simulations)):   # 只画前30条细线，避免太乱
        ax.plot(curves[i], alpha=0.15, linewidth=0.6, color=color)
    median_curve = np.median(curves, axis=0)  # 200次实验的中位数轨迹
    ax.plot(median_curve, color=color, linewidth=2.5, label=f'中位数轨迹 ({label})')
    ax.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5, label=f'初始本金 {initial_capital}元')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('下注轮次')
    ax.set_ylabel('资金 (元)')
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')      # 纵轴用对数刻度，差距大时更好看
    ax.set_ylim(1, None)

plt.tight_layout()
plt.show()

print("=" * 70)
print(f"凯利公式计算: 最优下注比例 f* = {kelly_fraction*100:.2f}% (胜率52%, 赔率1:1)")
print("=" * 70)

for name, curves, color in [("玩家A (无优势)", curves_A, "red"),
                              ("玩家B (索普策略)", curves_B, "green"),
                              ("玩家C (有优势但冒进)", curves_C, "goldenrod")]:
    finals = curves[:, -1]                    # 每个实验最后一轮的资金
    win_rate = np.mean(finals > initial_capital) * 100  # 最终赚钱的比例
    median_final = np.median(finals)
    print(f"\n  【{name}】")
    print(f"    中位数终点资金: {median_final:,.0f}元")
    print(f"    盈利概率: {win_rate:.1f}%")
    print(f"    最好情况: {np.max(finals):,.0f}元 | 最差情况: {np.min(finals):,.2f}元")

print("\n" + "=" * 70)
print("  → 没有概率优势，凯利公式也救不了你（玩家A）")
print("  → 仅仅2%的胜率优势 + 科学仓位管理 = 长期稳定复利（玩家B）")
print("  → 有优势但仓位过重，反而可能亏光（玩家C）")
print("  → 这就是索普的核心发现：概率优势 × 仓位管理 = 量化盈利的底层公式")
print("=" * 70)
''',
    34: r'''# ========== 第一章爽点：下载真实股票数据 ==========
import warnings
warnings.filterwarnings('ignore')   # 隐藏不影响学习的警告信息

import matplotlib.pyplot as plt     # 画图
import yfinance as yf               # 从雅虎财经免费下载行情

plt.rcParams['font.sans-serif'] = ['PingFang HK', 'STHeiti', 'Microsoft YaHei', 'SimHei']
aapl = yf.download('AAPL', period='6mo', progress=False, multi_level_index=False)

print('🎉 恭喜！你已经拿到真实股票数据')
print(f'   共 {len(aapl)} 个交易日')                              # 行数 = 交易日个数
print(f'   最新收盘价: ${aapl["Close"].iloc[-1]:.2f}')            # iloc[-1] = 最后一行
display(aapl.tail(5))   # 在 Notebook 里美观地显示最后 5 行表格

# ========== 上图收盘价、下图成交量 ==========
fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True,       # 2行子图，横轴对齐
                         gridspec_kw={'height_ratios': [3, 1]})    # 上图占 3 份高度
axes[0].plot(aapl.index, aapl['Close'], color='tab:blue', linewidth=1.5)  # 折线：收盘价
axes[0].set_title('真实数据 · 苹果 AAPL 收盘价', fontsize=14)
axes[0].set_ylabel('美元')
axes[0].grid(True, alpha=0.3)

axes[1].bar(aapl.index, aapl['Volume'], width=0.8, color='gray', alpha=0.5)  # 柱状：成交量
axes[1].set_ylabel('成交量')
axes[1].set_xlabel('日期')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
''',
}


# 第 2～4 章注释见同目录 comment_data_ch2_4.py
from comment_data_ch2_4 import SOURCES_CH2_4  # noqa: E402

SOURCES.update(SOURCES_CH2_4)


def _to_nb_source(code: str) -> list[str]:
    """Notebook 单元格 source：每行以换行符结尾。"""
    lines = code.splitlines()
    if not lines:
        return []
    return [line + "\n" for line in lines]


def apply():
    for fname, cells in SOURCES.items():
        path = NB_DIR / fname
        nb = json.loads(path.read_text(encoding="utf-8"))
        n = 0
        for idx, code in cells.items():
            if idx >= len(nb["cells"]):
                print(f"SKIP {fname} cell {idx}: index out of range")
                continue
            if nb["cells"][idx]["cell_type"] != "code":
                print(f"SKIP {fname} cell {idx}: not code")
                continue
            nb["cells"][idx]["source"] = _to_nb_source(code)
            n += 1
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"OK {fname}: updated {n} code cells")


if __name__ == "__main__":
    apply()

