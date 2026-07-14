"""Generate README showcase images (run from repo root)."""
from __future__ import annotations

import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["PingFang HK", "STHeiti", "Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def save(fig, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path.relative_to(ROOT))


def ch02_returns():
    aapl = yf.download("AAPL", period="1y", progress=False, multi_level_index=False)
    rets = aapl["Close"].pct_change().dropna()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(rets.index, rets.values, color="steelblue", lw=0.9)
    axes[0].axhline(0, color="k", ls="--", lw=0.6)
    axes[0].set_title("AAPL 日收益率曲线")
    axes[1].hist(rets.values, bins=35, color="steelblue", edgecolor="white", alpha=0.85)
    axes[1].axvline(0, color="k", ls="--", lw=0.6)
    axes[1].set_title("日收益率分布")
    fig.suptitle("第二章 · 收益率分析", fontsize=13, y=1.02)
    save(fig, "ch02_returns.png")


def ch03_ma_signals():
    df = yf.download("AAPL", period="2y", progress=False, multi_level_index=False)[["Close"]]
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["spread"] = df["MA5"] - df["MA20"]
    cross = np.sign(df["spread"]).diff()
    golden = df[cross > 0].dropna()
    death = df[cross < 0].dropna()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df["Close"], color="gray", alpha=0.4, lw=1)
    ax.plot(df.index, df["MA5"], color="tab:orange", lw=1.2, label="MA5")
    ax.plot(df.index, df["MA20"], color="tab:blue", lw=1.8, label="MA20")
    ax.scatter(golden.index, golden["MA5"], marker="^", s=50, c="green", edgecolors="k", lw=0.3, label="金叉")
    ax.scatter(death.index, death["MA5"], marker="v", s=50, c="red", edgecolors="k", lw=0.3, label="死叉")
    ax.set_title("第三章 · 双均线策略买卖点")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    save(fig, "ch03_ma_signals.png")


def ch04_backtest():
    ticker, bench, period = "AAPL", "SPY", "2y"
    df = yf.download(ticker, period=period, progress=False, multi_level_index=False)[["Close"]]
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["signal"] = (df["MA5"] > df["MA20"]).astype(int)
    df["position"] = df["signal"].shift(1).fillna(0)
    df["ret"] = df["Close"].pct_change().fillna(0)
    df["strategy_ret"] = df["position"] * df["ret"]
    spy = yf.download(bench, period=period, progress=False, multi_level_index=False)[["Close"]]
    spy.columns = ["SPY"]
    df = df.join(spy, how="inner")
    df["market_ret"] = df["SPY"].pct_change().fillna(0)
    df["nav_strategy"] = (1 + df["strategy_ret"]).cumprod()
    df["nav_buyhold"] = (1 + df["ret"]).cumprod()
    df["nav_market"] = (1 + df["market_ret"]).cumprod()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df["nav_strategy"], lw=2.2, color="tab:purple", label="双均线策略")
    ax.plot(df.index, df["nav_buyhold"], lw=1.6, color="tab:blue", label=f"买入持有 {ticker}")
    ax.plot(df.index, df["nav_market"], lw=1.6, color="gray", ls="--", label=f"买入持有 {bench}")
    ax.axhline(1, color="k", lw=0.5, ls=":")
    ax.set_title("第四章 · 策略回测净值曲线")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    save(fig, "ch04_backtest.png")


def ch01_stock():
    aapl = yf.download("AAPL", period="6mo", progress=False, multi_level_index=False)
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    axes[0].plot(aapl.index, aapl["Close"], color="tab:blue", lw=1.5)
    axes[0].set_title("第一章爽点 · 真实苹果 AAPL 股票数据")
    axes[0].set_ylabel("收盘价 (USD)")
    axes[0].grid(True, alpha=0.3)
    axes[1].bar(aapl.index, aapl["Volume"], width=0.8, color="gray", alpha=0.5)
    axes[1].set_ylabel("成交量")
    axes[1].set_xlabel("日期")
    axes[1].grid(True, alpha=0.3)
    save(fig, "ch01_real_stock.png")


def cover_banner():
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis("off")
    ax.text(
        0.5,
        0.55,
        "Quant-for-Beginners",
        ha="center",
        va="center",
        fontsize=28,
        fontweight="bold",
        color="#1a1a2e",
    )
    ax.text(
        0.5,
        0.25,
        "中文零基础 · 量化金融学习路线  |  30分钟做出可运行结果",
        ha="center",
        va="center",
        fontsize=14,
        color="#4a4a6a",
    )
    ax.set_facecolor("#f0f4ff")
    fig.patch.set_facecolor("#f0f4ff")
    save(fig, "cover_banner.png")


if __name__ == "__main__":
    cover_banner()
    ch01_stock()
    ch02_returns()
    ch03_ma_signals()
    ch04_backtest()
    print("done")
