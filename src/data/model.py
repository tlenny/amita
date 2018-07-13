# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月3日

@author: ALEX
'''

from sqlalchemy import Column, String, Integer, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TradingDataDaily(Base):
    __tablename__ = 'trading_data_daily'

    id = Column(Integer, primary_key=True)
    bourse = Column(String(30))
    code = Column(String(30))
    time_date = Column(String(10))
    open = Column(DECIMAL(28, 6))
    high = Column(DECIMAL(28, 6))
    low = Column(DECIMAL(28, 6))
    close = Column(DECIMAL(28, 6))
    change = Column(DECIMAL(28, 6))
    volume = Column(DECIMAL(28, 6))
    money = Column(DECIMAL(28, 6))
    traded_market_value = Column(DECIMAL(28, 6))
    market_value = Column(DECIMAL(28, 6))
    turnover = Column(DECIMAL(28, 6))
    adjust_price = Column(DECIMAL(28, 6))
    pe_ttm = Column(DECIMAL(28, 6))
    ps_ttm = Column(DECIMAL(28, 6))
    pc_ttm = Column(DECIMAL(28, 6))
    pb = Column(DECIMAL(28, 6))
    adjust_price_f = Column(DECIMAL(28, 6))
    created_stamp = Column(TIMESTAMP())


class MA(Base):
    __tablename__ = 'ma'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    ma_5 = Column(DECIMAL(28, 6))
    ma_10 = Column(DECIMAL(28, 6))
    ma_20 = Column(DECIMAL(28, 6))
    ma_30 = Column(DECIMAL(28, 6))
    ma_60 = Column(DECIMAL(28, 6))
    ma_120 = Column(DECIMAL(28, 6))
    ma_250 = Column(DECIMAL(28, 6))


class MACD(Base):
    __tablename__ = 'macd'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    ema_12 = Column(DECIMAL(28, 6))
    ema_26 = Column(DECIMAL(28, 6))
    dif = Column(DECIMAL(28, 6))
    dea = Column(DECIMAL(28, 6))


class TRIX(Base):
    __tablename__ = 'trix'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    ax = Column(DECIMAL(28, 6))
    bx = Column(DECIMAL(28, 6))
    trix = Column(DECIMAL(28, 6))
    tma = Column(DECIMAL(28, 6))


class KDJ(Base):
    __tablename__ = 'kdj'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    rsv = Column(DECIMAL(28, 6))
    k = Column(DECIMAL(28, 6))
    d = Column(DECIMAL(28, 6))
    j = Column(DECIMAL(28, 6))
