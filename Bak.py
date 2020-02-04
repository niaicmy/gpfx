import pretty_errors
import os
from struct import unpack
import re

# talib 金融分析库
# import talib
# import numpy
# import matplotlib.pyplot as plt
# import matplotlib as mpl

# 使用ggplot样式，好看些
# mpl.style.use("ggplot")

# 个股的匹配规则
re_rule = r'^sh6[08]\d{4}\.[dl][ac][y5]|^sz[03][0]\d{4}\.[dl][ac][y5]'
stock_file_rule = re.compile(re_rule)
# 板块指数的匹配规则
# todo: 修改板块指数的匹配模式
block_re_rule = r'^sh6[08]\d{4}\.[dl][ac][y5]|^sz[03][0]\d{4}\.[dl][ac][y5]'
block_rule = re.compile(block_re_rule)

# 数据共用结构 参照数据结构文件说明
data_structure = {
    "stock_date": [],
    "stock_open": [],
    "stock_high": [],
    "stock_low": [],
    "stock_close": [],
    "stock_amount": [],
    "stock_vol": [],
    "stock_reservation": [],
    "stock_num": []  # 增加一个股票代码的参数，方便满足条件时记录股票编码
}
data_ext = {'day': r".day", 'lc5': r".lc5"}
# 一个大的列表 储存stock_day stock_lc5 一个表 包含所有股票，股票的子表包含数据
# 每32字节（32bytes）为一组记录
data_size = 32
# 默认分析周期
analysis_cycle = 500
# 文件目录
file_path_set = {
    'sh_day': r"D:\通达信\new_tdx\vipdoc\sh\lday",
    'sh_lc5': r"D:\通达信\new_tdx\vipdoc\sh\fzline",
    'sz_day': r"D:\通达信\new_tdx\vipdoc\sz\lday",
    'sz_lc5': r"D:\通达信\new_tdx\vipdoc\sz\fzline"
}


def walk_directory(_file_directory):
    # 取得文件夹里面的所有子文件
    root, dirs, files = tuple(os.walk(_file_directory))[0]
    # 取得判断扩展名
    # name, ext = os.path.splitext(files[0])

    # 生成文件列表
    file_urls = []
    for file in files:
        # re 匹配文件
        if stock_file_rule.match(file):
            file_urls.append(os.path.join(_file_directory, file))
    # print(file_urls)
    return file_urls


def unpack_stock_data(_file_url, _data_size=32, _analysis_cycle=1):
    """
    # 解析本地数据 .day .lc5 文件
    :param _file_url: 数据文件
    :param _data_size: 数据结构大小 默认 32
    :param _analysis_cycle: 需要分析的数据周期 默认 1 只能是正整数(int)
    :return:
    """

    # # 取得文件夹里面的所有子文件
    # root, dirs, files = tuple(os.walk(_file_directory))[0]
    # 取得判断扩展名
    # name, ext = os.path.splitext(files[0])
    # name, ext = os.path.splitext(_file_urls)
    #
    # # 生成文件列表
    # file_urls = []
    # for file in files:
    #     # re 匹配文件
    #     if stock_file_rule.match(file):
    #         file_urls.append(os.path.join(_file_directory, file))
    # # print(file_urls)

    name, ext = os.path.splitext(os.path.basename(_file_url))
    for key in data_structure.keys():
        data_structure[key] = []

    if data_ext['day'] == ext:
        # 遍历文件
        # for file_url in _file_url:
            # 取得判断扩展名
            # name2 = os.path.basename(file_url)
            # name, ext = os.path.splitext(os.path.basename(file_url))
            # name, ext = os.path.splitext(file_url)

            file_size = os.path.getsize(_file_url)
            # print(file_url)
            # 清空原本的数据
            # data_structure.clear()
            # for key in data_structure.keys():
            #     data_structure[key] = []
            # 打开读取文件 设置文件指针 设置读取文件的循环周期
            # 解决文件根本不够分析周期的问题
            # 获取文件内容大小，区分读取方式
            # if data_ext['day'] == ext:
            #     pass
            with open(_file_url, r'rb') as fp:
                if file_size > _data_size * _analysis_cycle:
                    fp.seek(-_data_size * _analysis_cycle, os.SEEK_END)
                    range_cycle = _analysis_cycle
                    # print('大于')
                else:
                    fp.seek(0, os.SEEK_SET)
                    range_cycle = int(file_size / _data_size)
                    # print('小于size')

                # 提取数据
                for i in range(0, range_cycle):
                    buff = fp.read(32)
                    _date, _open, _high, _low, _close, _amount, _vol, _reservation = unpack(r"IIIIIfII", buff)
                    # print(_date)
                    # print(_open/100)
                    data_structure['stock_date'].append(_date)  # 4字节 如20091229
                    data_structure['stock_open'].append(_open / 100)  # 开盘价*100
                    data_structure['stock_high'].append(_high / 100)  # 最高价*100
                    data_structure['stock_low'].append(_low / 100)  # 最低价*100
                    data_structure['stock_close'].append(_close / 100)  # 收盘价*100
                    data_structure['stock_amount'].append(_amount)  # 成交额
                    data_structure['stock_vol'].append(_vol)  # 成交量
                    data_structure['stock_reservation'].append(_reservation)  # 保留值
                    data_structure['stock_num'].append(name)  # 股票代码

            # stock_ta_lib(data_structure)
            # fp.close()
    # 按天算 5 分钟数据 天数*48(48 是一天的5分钟周期总和)
    elif data_ext['lc5'] == ext:
        # print('lc5')
        for file_url in _file_url:
            # 取得判断扩展名
            # name2 = os.path.basename(file_url)
            # name, ext = os.path.splitext(os.path.basename(file_url))
            # name, ext = os.path.splitext(file_url)
            file_size = os.path.getsize(file_url)
            # print(file_url)
            # 清空原本的数据
            # data_structure.clear()
            for key in data_structure.keys():
                data_structure[key] = []

            # 打开读取文件 设置文件指针 设置读取文件的循环周期
            # 48个周期为一天4小时的5分钟数据
            _analysis_cycle = _analysis_cycle * 48
            with open(file_url, r'rb') as fp:
                if file_size > _data_size * _analysis_cycle:
                    fp.seek(-_data_size * _analysis_cycle, os.SEEK_END)
                    range_cycle = _analysis_cycle
                    # print('大于')
                else:
                    fp.seek(0, os.SEEK_SET)
                    range_cycle = int(file_size / _data_size)
                    # print('小于size')
                for i in range(0, range_cycle):
                    buff = fp.read(32)
                    a0, a1, _open, _high, _low, _close, _amount, _vol, _reservation = unpack(r"HHfffffII", buff)
                    # print(_date)
                    # print(_open/100)
                    # a = unpack("HH", stock_date)
                    _date = str(int(a0 / 2048) + 2004) + '-' + str(int(a0 % 2048 / 100)).zfill(2) + '-' + str(
                        a0 % 2048 % 100).zfill(2), str(int(a1 / 60)).zfill(2) + ':' + str(a1 % 60).zfill(
                        2) + ':00'
                    data_structure['stock_date'].append(_date)  # (日期, 时间)
                    data_structure['stock_open'].append(round(_open, 2))  # 开盘价
                    data_structure['stock_high'].append(round(_high, 2))  # 最高价
                    data_structure['stock_low'].append(round(_low, 2))  # 最低价
                    data_structure['stock_close'].append(round(_close, 2))  # 收盘价
                    data_structure['stock_amount'].append(round(_amount, 2))  # 成交额
                    data_structure['stock_vol'].append(_vol)  # 成交量
                    data_structure['stock_reservation'].append(_reservation)  # 保留值
                    data_structure['stock_num'].append(name)


if __name__ == "__main__":
    file_path_set['sh_day'] = r'F:\PycharmProjects\gpfx\test_talib'
    unpack_stock_data(file_path_set['sh_day'], _analysis_cycle=50)
    print(data_structure)
    pass
    # unpack_stock_day(r"F:\PycharmProjects\gpfx\sz000028.day")
    # unpack_stock_lc5(r"F:\PycharmProjects\gpfx\sz000028.lc5")
    # print(stock_lc5['stock_date'])
    # print(stock_lc5['stock_open'])
    # print(stock_day['stock_date'])
    # print(stock_day['stock_open'])
    # print(stock_day['stock_high'])
    # print(stock_day['stock_low'])
    # print(stock_day['stock_close'])
    # print(stock_day['stock_amount'])
    # print(stock_day['stock_vol'])
    # print(stock_day['stock_reservation'])
