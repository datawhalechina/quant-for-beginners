<p align="center">
  <a href="notebooks/phase1_intro/01_什么是量化金融.ipynb">
    <img src="assets/images/cover-phase1.jpg" width="49%" alt="第一期 · 从 Python 到 AI 量化交易实战" style="max-width: 450px; border-radius: 8px;"/>
  </a>
  <a href="notebooks/phase2_intro/01_理解波动率.ipynb">
    <img src="assets/images/cover-phase2.jpg" width="49%" alt="第二期 · 风险与组合管理" style="max-width: 450px; border-radius: 8px;"/>
  </a>
</p>

<p align="center">
  <strong>Quant-for-Beginners</strong> · 中文零基础量化金融 Notebook 路线 · Phase 1 &amp; 2 已上线
</p>

<p align="center">
  <a href="requirements.txt"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/></a>
  <a href="notebooks/"><img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter"/></a>
  <a href="notebooks/phase1_intro/"><img src="https://img.shields.io/badge/Phase_1-4_chapters-2ea043?style=flat-square" alt="Phase 1"/></a>
  <a href="notebooks/phase2_intro/"><img src="https://img.shields.io/badge/Phase_2-4_chapters-1f6feb?style=flat-square" alt="Phase 2"/></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#课程目录">课程目录</a> ·
  <a href="#学习路线">学习路线</a> ·
  <a href="#后续规划">后续规划</a> ·
  <a href="#yibo-quant-成长会">Yibo Quant 成长会</a>
</p>

---

## 简介

哈喽，我是 Yibo。这是一份面向**零基础**读者的中文量化金融教程：每章配有可运行的 Notebook 和配套交互演示，边读边跑，把概念落到真实行情上。

本仓库由 **Yibo** 整理维护，侧重可运行的代码与清晰图示，而非堆砌公式。内容持续更新，欢迎 Star 方便日后查阅。

| 项目 | 说明 |
|------|------|
| 形式 | Jupyter Notebook + 配套交互 HTML |
| 数据 | `yfinance` · `akshare` 免费日线行情 |
| 第一期 | 4 章（已全部上线） |
| 第二期 | 4 章（已全部上线） |
| 不适合 | 已具备完整回测框架、仅需高级因子参考的读者 |

---

## 快速开始

```bash
git clone https://github.com/datawhalechina/quant-for-beginners.git
cd quant-for-beginners
pip install -r requirements.txt
jupyter lab
```

---

## 课程目录

### 第一期 · 量化入门

| 章 | 主题 | Notebook | 你将完成 |
|:--:|------|----------|----------|
| 01 | 什么是量化金融 | [打开](notebooks/phase1_intro/01_什么是量化金融.ipynb) | 建立量化直觉；下载真实 AAPL 行情 |
| 02 | 你的第一个量化实验 | [打开](notebooks/phase1_intro/02_你的第一个量化实验.ipynb) | OHLCV、收益率、波动对比 |
| 03 | 移动平均线策略 | [打开](notebooks/phase1_intro/03_移动平均线策略.ipynb) | MA5/MA20、金叉/死叉、首个交易规则 |
| 04 | 策略回测 | [打开](notebooks/phase1_intro/04_策略回测.ipynb) | 模拟交易、净值曲线、胜率与回撤 |

### 第二期 · 风险与组合

| 章 | 主题 | Notebook | 你将完成 |
|:--:|------|----------|----------|
| 05 | 理解波动率 | [打开](notebooks/phase2_intro/01_理解波动率.ipynb) | 波动率度量、年化换算、多票对比 |
| 06 | 夏普比率与 Beta | [打开](notebooks/phase2_intro/02_夏普比率与Beta.ipynb) | 风险调整收益、个股相对大盘敏感度 |
| 07 | 最大回撤与仓位管理 | [打开](notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) | 回撤测算、仓位与风险承受 |
| 08 | 多标的组合与相关性 | [打开](notebooks/phase2_intro/04_多标的组合与相关性.ipynb) | 等权组合、相关性矩阵、分散化 |

### 配套交互演示

在浏览器本地打开（无需联网，对应各章公式推导）：

| 演示 | 链接 | 对应章节 |
|------|------|----------|
| 布朗运动与随机游走 | [打开](assets/interactive/brownian-random-walk.html) | 第一期 · 第一章 |
| 日收益率 | [打开](assets/interactive/daily-return-demo.html) | 第二期 · 理解波动率 |
| 样本标准差 | [打开](assets/interactive/std-dev-demo.html) | 第二期 · 理解波动率 |
| 总体方差 | [打开](assets/interactive/population-variance-demo.html) | 第二期 · 理解波动率 |
| 方差修正公式 | [打开](assets/interactive/variance-formulas-demo.html) | 第二期 · 理解波动率 |
| 夏普比率 | [打开](assets/interactive/sharpe-ratio-demo.html) | 第二期 · 夏普比率与 Beta |
| Beta | [打开](assets/interactive/beta-demo.html) | 第二期 · 夏普比率与 Beta |

更多说明见 [assets/interactive/README.md](assets/interactive/README.md)。

---

## 章节预览

<p align="center">
  <img src="assets/images/ch01_real_stock.png" width="48%" alt="第一章"/>
  <img src="assets/images/ch02_returns.png" width="48%" alt="第二章"/>
</p>
<p align="center">
  <img src="assets/images/ch03_ma_signals.png" width="48%" alt="第三章"/>
  <img src="assets/images/ch04_backtest.png" width="48%" alt="第四章"/>
</p>

<p align="center"><sub>章节示意图见 <code>assets/images/</code>；本地运行 Notebook 可得到交互式图表</sub></p>

---

## 学习路线

```
Phase 1（已上线）
├── 01 量化认知与真实数据
├── 02 收益率与数据分析
├── 03 双均线策略
└── 04 策略回测

Phase 2（已上线）
├── 05 理解波动率
├── 06 夏普比率与 Beta
├── 07 最大回撤与仓位管理
└── 08 多标的组合与相关性

Phase 3（规划）  因子 · 多因子选股
Phase 4（规划）  机器学习与 AI 量化
```

| 章节 | 进度称号 |
|------|----------|
| 第 1 章 | Lv.1 量化探索者 |
| 第 2 章 | Lv.1 数据分析 |
| 第 3 章 | Lv.2 策略设计师 |
| 第 4 章 | Lv.3 回测分析师 |
| 第 5 章 | Lv.4 风险观察员 |
| 第 6 章 | Lv.4 风险分析师 |
| 第 7 章 | Lv.5 仓位管理员 |
| 第 8 章 | Lv.5 组合分析师 |

---

## 仓库结构

```
quant-for-beginners/
├── notebooks/
│   ├── phase1_intro/         # 第一期（第 1～4 章）
│   └── phase2_intro/         # 第二期（第 5～8 章）
├── assets/
│   ├── images/               # README 与传播用配图
│   └── interactive/          # 独立 HTML 交互演示
├── scripts/                  # 配图生成、Notebook 维护脚本
├── docs/ROADMAP.md           # 详细路线图
├── src/                      # 可复用模块（建设中）
└── requirements.txt
```

---

## 后续规划

| 章节 | 主题 | 状态 |
|------|------|------|
| 09 | AI 预测涨跌（入门） | 规划中 |
| 10 | XGBoost 量化策略 | 规划中 |
| 11 | LSTM 时间序列 | 规划中 |
| 12 | Transformer 交易 | 规划中 |
| 13 | 多因子选股 | 规划中 |
| 14 | AI 量化系统搭建 | 规划中 |

完整说明见 [docs/ROADMAP.md](docs/ROADMAP.md)。

---

## Yibo Quant 成长会

<p align="center">
  <img src="assets/images/yiboquant-growth-club.jpg" width="100%" alt="Yibo Quant 成长会" style="max-width: 920px; border-radius: 8px;"/>
</p>

**Yibo Quant 成长会**是完全开源、免费的量化长期成长社群，面向对量化投资、算法建模有强烈热情、具备自主学习能力的优秀学习者开放。

社群以**学术研究**与**真实项目实战**为两大支柱：无付费门槛、无商业引流，汇聚纯粹热爱量化的同路人。我们会定期开展量化前沿文献研读、策略理论深度分享，组队落地完整的量化开源实战项目；同时开放免费学习资料、源码库与交流渠道，搭建纯粹、高质量、轻量化的量化自主研习圈层。

为保持讨论质量，社群采用**有门槛的录取机制**。

**投递通道**：[cyibo815@163.com](mailto:cyibo815@163.com)

---

## Star 趋势

<p align="center">
  <a href="https://www.star-history.com/#yibohere/Quant-for-Beginners,datawhalechina/quant-for-beginners&Date">
    <img alt="Star History Chart" src="assets/images/star-history.svg" width="700"/>
  </a>
</p>

<sub>图表使用仓库内静态 SVG，避免外链 API 加载失败。点击可跳转 star-history.com 查看交互版（含 transfer 前后两个仓库）。</sub>

---

## 作者

**Yibo Cheng（翊博）** — 项目发起人与主要维护者  
GitHub：[@yibohere](https://github.com/yibohere)

---


## 免责声明

本仓库仅供学习与研究，**不构成任何投资建议**。历史回测结果不代表未来表现，市场有风险。

---

<p align="center">
  <sub>如果这份路线对你有帮助，欢迎 Star ⭐</sub>
</p>
