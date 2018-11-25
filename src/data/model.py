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

    
class DMI(Base):
    __tablename__ = 'dmi'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    pdm = Column(DECIMAL(28, 6))
    mdm = Column(DECIMAL(28, 6))
    tr = Column(DECIMAL(28, 6))
    pdi = Column(DECIMAL(28, 6))
    mdi = Column(DECIMAL(28, 6))
    dx = Column(DECIMAL(28, 6))
    pdm12 = Column(DECIMAL(28, 6))
    mdm12 = Column(DECIMAL(28, 6))
    tr12 = Column(DECIMAL(28, 6))
    pdi12 = Column(DECIMAL(28, 6))
    mdi12 = Column(DECIMAL(28, 6))
    adx = Column(DECIMAL(28, 6))
    adxr = Column(DECIMAL(28, 6))


class ARBR(Base):
    __tablename__ = 'arbr'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    ar_26 = Column(DECIMAL(28, 6))
    br_26 = Column(DECIMAL(28, 6))

    
class EMV(Base):
    __tablename__ = 'emv'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    em = Column(DECIMAL(28, 6))
    emv = Column(DECIMAL(28, 6))
    maemv = Column(DECIMAL(28, 6))


class BOLL(Base):
    __tablename__ = 'boll'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    md = Column(DECIMAL(28, 6))
    up = Column(DECIMAL(28, 6))
    dn = Column(DECIMAL(28, 6))

    
class RSI(Base):
    __tablename__ = 'rsi'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    rsi_6 = Column(DECIMAL(28, 6))    
    rsi_12 = Column(DECIMAL(28, 6))
    rsi_24 = Column(DECIMAL(28, 6))

    
class BIAS(Base):
    __tablename__ = 'bias'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    bias_6 = Column(DECIMAL(28, 6))    
    bias_12 = Column(DECIMAL(28, 6))
    bias_24 = Column(DECIMAL(28, 6))    
    bias_72 = Column(DECIMAL(28, 6))


class ROC(Base):
    __tablename__ = 'roc'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    roc = Column(DECIMAL(28, 6))    
    rocma = Column(DECIMAL(28, 6))


class WR(Base):
    __tablename__ = 'wr'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    wr_6 = Column(DECIMAL(28, 6))  
    wr_10 = Column(DECIMAL(28, 6)) 
    wr_20 = Column(DECIMAL(28, 6)) 
    wr_40 = Column(DECIMAL(28, 6))   


class DMA(Base):
    __tablename__ = 'dma'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    dma = Column(DECIMAL(28, 6))  
    ama = Column(DECIMAL(28, 6)) 


class CR(Base):
    __tablename__ = 'cr'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    cr = Column(DECIMAL(28, 6))  

    
class Evaluation(Base):
    __tablename__ = 'evaluation'

    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    time_date = Column(String(30))
    score = Column(DECIMAL(28, 6))  
    feature = Column(String(255))
