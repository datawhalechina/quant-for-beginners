"""Notebook 共用的美股日线读取：Yahoo Finance 失败时回退 AkShare。"""

import logging

import pandas as pd


_OFFSETS = {
    "6mo": pd.DateOffset(months=6),
    "1y": pd.DateOffset(years=1),
    "2y": pd.DateOffset(years=2),
    "3y": pd.DateOffset(years=3),
}
_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def _dates(period):
    try:
        offset = _OFFSETS[period]
    except KeyError as exc:
        raise ValueError(f"不支持的 period={period!r}；可选：{'、'.join(_OFFSETS)}") from exc
    end = pd.Timestamp.now(tz="UTC").normalize().tz_localize(None) + pd.Timedelta(days=1)
    return end - offset, end


def _ohlcv(data, symbol, start, end):
    if data is None or data.empty:
        raise ValueError("未返回行情")
    if isinstance(data.columns, pd.MultiIndex):
        for level in (-1, 0):
            if symbol in data.columns.get_level_values(level):
                data = data.xs(symbol, axis=1, level=level, drop_level=True)
                break
    data = data.copy()
    if "date" in data.columns:
        data = data.set_index("date")
    data.index = pd.to_datetime(data.index).tz_localize(None)
    data.columns = [str(column).title() for column in data.columns]
    missing = set(_COLUMNS).difference(data.columns)
    if missing:
        raise ValueError(f"字段不完整：缺少 {sorted(missing)}")
    return data.sort_index().loc[start:end, _COLUMNS].dropna(subset=["Close"])


def _yahoo(symbol, start, end):
    import yfinance as yf

    logger = logging.getLogger("yfinance")
    was_disabled = logger.disabled
    logger.disabled = True  # 请求失败会回退，避免底层日志干扰 Notebook。
    try:
        data = yf.download(
            symbol,
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            auto_adjust=True,
            progress=False,
        )
    finally:
        logger.disabled = was_disabled
    return _ohlcv(data, symbol, start, end)


def _akshare(symbol, start, end):
    import akshare as ak

    return _ohlcv(ak.stock_us_daily(symbol=symbol, adjust="qfq"), symbol, start, end)


def _load_all(symbols, period):
    start, end = _dates(period)
    errors = []
    for name, loader in (("Yahoo Finance", _yahoo), ("AkShare", _akshare)):
        try:
            return [loader(symbol, start, end) for symbol in symbols], name
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    raise RuntimeError(
        "无法获取美股日线；请运行 `pip install -r requirements.txt` 并检查网络。"
        f"尝试结果：{'；'.join(errors)}"
    )


def fetch_us_data(symbols, period="1y"):
    """读取美股并返回 ``{代码: 标准 OHLCV 表}`` 与实际数据源。"""
    symbols = [symbol.upper() for symbol in symbols]
    if not symbols:
        raise ValueError("至少需要一个标的代码")
    frames, source = _load_all(symbols, period)
    return dict(zip(symbols, frames)), source
