# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月13日

@author: ALEX
指标计算公式：
（1）计算当日动向值
动向指数的当日动向值分为上升动向、下降动向和无动向等三种情况，每日的当日动向值只能是三种情况的一种。
A、上升动向（+DM）
+DM代表正趋向变动值即上升动向值，其数值等于当日的最高价减去前一日的最高价，如果<=0 则+DM=0。
B、下降动向（-DM）
﹣DM代表负趋向变动值即下降动向值，其数值等于前一日的最低价减去当日的最低价，如果<=0 则-DM=0。注意-DM也是非负数。
再比较+DM和-DM，较大的那个数字保持，较小的数字归0。
C、无动向
无动向代表当日动向值为“零”的情况，即当日的+DM和﹣DM同时等于零。有两种股价波动情况下可能出现无动向。一是当当日的最高价低于前一日的最高价并且当日的最低价高于前一日的最低价，二是当上升动向值正好等于下降动向值。
（2）计算真实波幅（TR）
TR代表真实波幅，是当日价格较前一日价格的最大变动值。取以下三项差额的数值中的最大值（取绝对值）为当日的真实波幅：
A、当日的最高价减去当日的最低价的价差。
B、当日的最高价减去前一日的收盘价的价差。
C、当日的最低价减去前一日的收盘价的价差。
TR是A、B、C中的数值最大者
（3）计算方向线DI
方向线DI是衡量股价上涨或下跌的指标，分为“上升指标”和“下降指标”。在有的股市分析软件上，+DI代表上升方向线，-DI代表下降方向线。其计算方法如下：
+DI=（+DM÷TR）×100
-DI=（-DM÷TR）×100
要使方向线具有参考价值，则必须运用平滑移动平均的原理对其进行累积运算。以12日作为计算周期为例，先将12日内的+DM、-DM及TR平均化，所得数值分别为+DM12，-DM12和TR12，具体如下：
+DI（12）=（+DM12÷TR12）×100
-DI（12）=（-DM12÷TR12）×100
随后计算第13天的+DI12、-DI12或TR12时，只要利用平滑移动平均公式运算即可。
上升或下跌方向线的数值永远介于0与100之间。
（4）计算动向平均数ADX
依据DI值可以计算出DX指标值。其计算方法是将+DI和—DI间的差的绝对值除以总和的百分比得到动向指数DX。由于DX的波动幅度比较大，一般以一定的周期的平滑计算，得到平均动向指标ADX。具体过程如下：
DX=(DI DIF÷DI SUM) ×100
其中，DI DIF为上升指标和下降指标的差的绝对值
DI SUM为上升指标和下降指标的总和
ADX就是DX的一定周期n的移动平均值。
（5）计算评估数值ADXR
在DMI指标中还可以添加ADXR指标，以便更有利于行情的研判。
ADXR的计算公式为：
ADXR=（当日的ADX+前n日的ADX）÷2
n为选择的周期数
'''

from data.model import DMI, TradingDataDaily
import data.db_helper as db_helper
import numpy as np

DMI_N = 12


def query_data_fn(sess, args):
    code = args[0]
    time_day = args[1]
    if time_day == None:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.code, TradingDataDaily.high, TradingDataDaily.low, TradingDataDaily.close).filter(TradingDataDaily.code == code).order_by(TradingDataDaily.time_date.asc())
    else:
        return sess.query(TradingDataDaily.time_date, TradingDataDaily.code, TradingDataDaily.high, TradingDataDaily.low, TradingDataDaily.close).filter(TradingDataDaily.code == code, TradingDataDaily.time_date <= time_day).order_by(TradingDataDaily.time_date.desc()).limit(2) 


def query_dmi_fn(sess, args):
    code = args[0]
    time_day = args[1]
    #last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx
    return sess.query(DMI.pdm,DMI.mdm,DMI.tr,DMI.pdi,DMI.mdi,DMI.dx,DMI.adx).filter(DMI.code == code, DMI.time_date < time_day).order_by(DMI.time_date.desc()).limit(DMI_N - 1)


def _ma(_last, curr):
    if curr == None :
        return None, _last
    _last = np.append(np.array(_last),np.array([curr]))
    if len(_last) > DMI_N:
        _last = np.delete(_last, 0)
    avg = None
    if len(_last) == DMI_N:
        avg = np.float(round(np.average(np.array(_last)), 4))
    return avg, _last


def _calc_dmi(code, last_data, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx):
    dmi = DMI()
    dmi.code = code
    dmi.time_date = last_data[-1][0]
    # +DM代表正趋向变动值即上升动向值，其数值等于当日的最高价减去前一日的最高价，如果<=0 则+DM=0。
    pdm = np.float(last_data[-1][2]) - np.float(last_data[-2][2])
    dmi.pdm = pdm = np.float(np.max([pdm, 0]))
    # ﹣DM代表负趋向变动值即下降动向值，其数值等于前一日的最低价减去当日的最低价，如果<=0 则-DM=0。注意-DM也是非负数。
    mdm = np.float(last_data[-2][3]) - np.float(last_data[-1][3])
    dmi.mdm = mdm = np.float(np.max([mdm, 0]))
    # tr_a当日的最高价减去当日的最低价的价差。
    tr_a = np.float(last_data[-1][2]) - np.float(last_data[-1][3])
    # 当日的最高价减去前一日的收盘价的价差。
    tr_b = np.float(last_data[-1][2]) - np.float(last_data[-2][4])
    # 当日的最低价减去前一日的收盘价的价差。
    tr_c = np.float(last_data[-1][3]) - np.float(last_data[-2][4])
    tr = np.float(round(np.max([np.abs(tr_a), np.abs(tr_b), np.abs(tr_c)]), 4))
    
    if tr != 0:
        # +DI=（+DM÷TR）×100
        pdi = round(pdm / tr * 100, 4)
        # -DI=（-DM÷TR）×100
        mdi = round(mdm / tr * 100, 4)
    else:
        pdi, mdi = 0, 0
    dmi.tr = tr
    dmi.pdi = pdi
    dmi.mdi = mdi
    # +DI和—DI间的差的绝对值除以总和的百分比得到动向指数DX,DX=(DI DIF÷DI SUM) ×100
    if pdi + mdi == 0:
        dmi.dx = 0
    else:
        dmi.dx = np.float(round(np.abs(pdi - mdi) / (pdi + mdi) * 100, 4))
    
    dmi.pdm12, last_pdm = _ma(last_pdm, dmi.pdm)
    dmi.mdm12, last_mdm = _ma(last_mdm, dmi.mdm)
    dmi.tr12, last_tr = _ma(last_tr, dmi.tr)
    dmi.pdi12, last_pdi = _ma(last_pdi, dmi.pdi)
    dmi.mdi12, last_mdi = _ma(last_mdi, dmi.mdi)
    dmi.adx, last_adx = _ma(last_dx, dmi.dx)
    # ADXR=（当日的ADX+前n日的ADX）÷2
    if len(last_adx) == DMI_N:
        dmi.adxr = np.float((last_adx[0] + last_adx[-1]) / 2)
    
    return dmi, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx


def _init_all(code):
    data = db_helper.select(query_data_fn, (code, None))
    if len(data) < 2:
        return None
    data = np.array(data)
    dmi_list = []
    last_data, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx = [], [], [], [], [], [], [], []
    for i in range(len(data) - 1):
        last_data = data[i:2 + i]
        dmi, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx = _calc_dmi(code, last_data, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx)
        dmi_list.append(dmi)
    return dmi_list


def _init_day(code, day):
    data = db_helper.select(query_data_fn, (code, day))
    if len(data) < 2:
        return None
    data = np.array(data)
    if data[0][0] != day:
        return None
    data = data[::-1]
    last_dmi = db_helper.select(query_dmi_fn, (code, day))
    last_dmi = np.array(last_dmi)
    last_dmi = last_dmi[::-1]
    last_data = data
    last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx = last_dmi[:, 0].astype(float), last_dmi[:, 1].astype(float), last_dmi[:, 2].astype(float), last_dmi[:, 3].astype(float), last_dmi[:, 4].astype(float), last_dmi[:, 5].astype(float), last_dmi[:, 6].astype(float)
    dmi, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx = _calc_dmi(code, last_data, last_pdm, last_mdm, last_tr, last_pdi, last_mdi, last_dx, last_adx)
    return dmi


def calc(code, time_day):
    """
    time_date is None时初始化全量
    """
    if time_day == None:
        data = _init_all(code)
        if data != None and len(data) > 0:
            pass
            db_helper.batch_insert(data)
        return None
    else:
        return _init_day(code, time_day)


if __name__ == '__main__':
    print(calc('600004', None))
    pass
