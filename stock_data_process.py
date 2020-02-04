# import pretty_errors
import numpy
# talib 金融分析库
import talib
from stock_data_collect import *

# 思路：用指标一层一层筛选，先用macd选择大范围

# 通达信 macd 指标
# macd筛选策略
set_macd_30 = set()
set_macd_60 = set()
set_macd_day = set()


def stock_filter_macd(_data_structure, end):
    """
    :param _data_structure: 数据的结构
    :param end: end 代表离最后周期的参数，筛选最近的
    :return: 符合条件的数据集合
    """
    # MACD = 2 * histogram 周期参数(12,26,9)
    dif, dea, histogram = talib.MACD(numpy.array(_data_structure['stock_close']), fastperiod=12, slowperiod=26,
                                     signalperiod=9)
    # 周期参数(6, 13, 9)
    dif2, dea2, histogram2 = talib.MACD(numpy.array(_data_structure['stock_close']), fastperiod=6, slowperiod=13,
                                        signalperiod=4)
    # dif, dea, macd = talib.MACDEXT(numpy.array(_data_structure['stock_close']), fastperiod=12, fastmatype=0,
    #                                slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
    # dif, dea, macd = talib.MACDEXT(numpy.array(_data_structure['stock_close']), signalperiod=9)
    # 1、金叉, 二次金叉
    # 记录金叉时间
    dif_cross_dea = []
    # cross_resonance 周期共振
    cross_resonance = []
    # 背离位置记录
    deviate_from_macd = []
    deviate_from_macd2 = []
    tmp = set()
    for i in range(len(dif)):
        if dif[i - 1] <= dea[i - 1] and dif[i] > dea[i]:
            pass
            # dif_cross_dea.append((_data_structure['stock_date'], i))  # 记录金叉的时间跟位置元组 (时间，位置)
            # print('金叉')
        # 2、背离
        # for i in range(len(histogram)):
        elif histogram[i] >= histogram[i - 1] and \
                _data_structure['stock_close'][i] <= _data_structure['stock_close'][i - 1]:
            pass
            # deviate_from_macd.append((_data_structure['stock_date'], i))  # 记录背离的时间跟位置元组 (时间，位置)
            # print('macd 背离')
        # 3、共振
        # 短周期dea2走平上拐，长周期dif周平上拐，买点
        elif dea2[i - 1] <= dea2[i] and dif[i - 1] <= dif[i] and len(dif) <= i + end:
            # cross_resonance.append((_data_structure['stock_date'], i))  # 记录共振的时间跟位置元组 (时间，位置)
            tmp.add(_data_structure['stock_num'])

    return tmp


# 通达信 trix指标
set_trix_30 = set()
set_trix_60 = set()
set_trix_day = set()


def stock_filter_trix(_data_structure, end):
    """
    :param _data_structure: 数据的结构
    :param end: end 代表离最后周期的参数，筛选最近的
    :return: 符合条件的数据集合
    """
    trix = talib.TRIX(numpy.array(_data_structure['stock_close']), timeperiod=12)
    matrix = talib.MA(trix, timeperiod=9, matype=0)
    # 记录 trix 走平 金叉位置
    tmp = set()
    for i in range(len(trix)):
        if trix[i - 1] <= trix[i] and len(trix) <= i + end:
            tmp.add(_data_structure['stock_num'])

    # return tmp

    tmp1 = set()
    for i in range(len(matrix)):
        if matrix[i - 1] <= matrix[i] and len(matrix) <= i + end:
            tmp1.add(_data_structure['stock_num'])

    return tmp1
    # print(trix)
    # print(matrix)


# 通达信 marsi 指标
set_marsi_30 = set()
set_marsi_60 = set()
set_marsi_day = set()


# 筛选marsi10 最后end 周期内拐头向上的
def stock_filter_marsi(_data_structure, end):
    # rsi6 = talib.RSI(numpy.array(_data_structure['stock_close']), timeperiod=6)
    # marsi6 = talib.MA(rsi6, timeperiod=6, matype=0)
    rsi10 = talib.RSI(numpy.array(_data_structure['stock_close']), timeperiod=10)
    marsi10 = talib.MA(rsi10, timeperiod=10, matype=0)
    tmp = set()
    for i in range(len(marsi10)):
        if marsi10[i - 1] <= marsi10[i] and len(marsi10) <= i + end:
            tmp.add(_data_structure['stock_num'])

    return tmp
    # print(rsi10)
    # print(marsi6)
    # print(marsi10)


def stock_filter_cci(_data_structure):
    pass


# def stock_filter_fsl(_data_structure):
#     pass

def stock_filter_average(_data_structure):
    ma10 = talib.MA(numpy.array(_data_structure['stock_close']), timeperiod=10)
    ma20 = talib.MA(numpy.array(_data_structure['stock_close']), timeperiod=20)
    ma30 = talib.MA(numpy.array(_data_structure['stock_close']), timeperiod=30)


# 用于数据转换的存储，而不修改原始的数据
data_copy = {}


# 30 & 60分钟数据转换 日线也可以(但要求数据是_timeperiod的倍数)
def cycle_transform(_data_structure, _timeperiod=6):
    """
    :param _data_structure: 数据共用结构
    :param _timeperiod: 30分钟数据是6个周期(默认分析30分钟数据), 60分钟数据是12个周期
    :return: 组合好的data_structure 数据共用结构
    """
    # 30 分钟数据是 6 个周期
    # 60 分钟数据是 12 个周期
    # 周线数据是日线数据的5个周期
    # i = 0
    # range_cycle = 0
    il = len(_data_structure['stock_date'])
    ir = il % _timeperiod
    # 构造循环的周期数
    if ir == 0:
        range_cycle = il // _timeperiod
    else:
        range_cycle = (il - ir) // _timeperiod
    # 清空原本的数据
    # data_structure.clear()
    # data_copy = data_structure.copy()
    for key in data_copy.keys():
        data_copy[key] = []
    # data_copy = {}
    # 组合数据
    for i in range(range_cycle):
        # 数据起步基数 数据取段为[base:base+_timeperiod]
        base = ir + i * _timeperiod
        # 30分钟数据
        # if _timeperiod == 6:
        # print(_data_structure['stock_date'])
        data_copy['stock_date'].append(_data_structure['stock_date'][base:base + _timeperiod][-1])
        data_copy['stock_open'].append(_data_structure['stock_open'][base:base + _timeperiod][0])
        data_copy['stock_close'].append(_data_structure['stock_close'][base:base + _timeperiod][-1])
        data_copy['stock_high'].append(max(_data_structure['stock_high'][base:base + _timeperiod]))
        data_copy['stock_low'].append(min(_data_structure['stock_low'][base:base + _timeperiod]))
        data_copy['stock_amount'].append(sum(_data_structure['stock_amount'][base:base + _timeperiod]))
        data_copy['stock_vol'].append(sum(_data_structure['stock_vol'][base:base + _timeperiod]))
        # data_structure['stock_reservation'] = _data_structure['stock_reservation'][base::_timeperiod]
        data_copy['stock_num'] = _data_structure['stock_num']
    return data_copy


if __name__ == '__main__':
    # file_path_set['sh_day'] = r'F:\PycharmProjects\gpfx\test_talib'
    # unpack_stock_data(file_path_set['sh_day'], _analysis_cycle=150)

    # print(data_structure['stock_close'])
    # stock_filter_trix(data_structure)
    # stock_filter_marsi(data_structure)

    file_path_set['sh_lc5'] = r'F:\PycharmProjects\gpfx\test_talib'
    file_urls = walk_directory(file_path_set['sh_lc5'])

    for file_url in file_urls:
        unpack_stock_data(file_url, _analysis_cycle=2)
        # 转换数据周期
        date_transform_30 = cycle_transform(data_structure, 6)
        # print(date_transform_30['stock_date'])
        # print(date_transform_30['stock_open'])
        date_transform_60 = cycle_transform(data_structure, 12)
        # print(date_transform_60['stock_date'])
        # print(date_transform_60['stock_open'])
