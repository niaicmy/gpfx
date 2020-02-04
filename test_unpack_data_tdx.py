import os
import pretty_errors
from struct import unpack
import re

# sh600074.day sh688012.day
# re_rule = r'^s[hz][603][08]\d{4}\.[dl][ac][y5]'
re_rule = r'^sh6[08]\d{4}\.[dl][ac][y5]|^sz[03][0]\d{4}\.[dl][ac][y5]'

re_rule_sh = r'^sh6[08]\d{4}\.[dl][ac][y5]'
re_rule_sz = r'^sz[03]0\d{4}\.[dl][ac][y5]'

file_rule = re.compile(re_rule)
file_path = r"D:\通达信\new_tdx\vipdoc\sh\lday"

stock_day = {
    "stock_date": [],
    "stock_open": [],
    "stock_high": [],
    "stock_low": [],
    "stock_close": [],
    "stock_amount": [],
    "stock_vol": [],
    "stock_reservation": []
}
# 数据共用结构 参照数据结构文件说明
data_structure = {
    "stock_date": [],
    "stock_open": [],
    "stock_high": [],
    "stock_low": [],
    "stock_close": [],
    "stock_amount": [],
    "stock_vol": [],
    "stock_reservation": []
}
data_size = 32
analysis_cycle = 5


def open_file_directory(_file_directory):
    # print(tuple(os.walk(_file_directory)))
    root, dirs, files = tuple(os.walk(_file_directory))[0]
    print(os.path.splitext(files[0]))
    # for root, dirs, files in os.walk(_file_directory):
    # print(root)
    # print(dirs)
    # print(files)


def unpack_stock_day(file_url):
    with open(file_url, r'rb') as f:
        f.seek(-data_size * analysis_cycle, 2)
        for i in range(0, analysis_cycle):
            buff = f.read(32)
            _date, _open, _high, _low, _close, _amount, _vol, _reservation = unpack(r"IIIIIfII", buff)
            # print(_date)
            # print(_open/100)
            stock_day['stock_date'].append(_date)  # 4字节 如20091229
            stock_day['stock_open'].append(_open / 100)  # 开盘价*100
            stock_day['stock_high'].append(_high / 100)  # 最高价*100
            stock_day['stock_low'].append(_low / 100)  # 最低价*100
            stock_day['stock_close'].append(_close / 100)  # 收盘价*100
            stock_day['stock_amount'].append(_amount)  # 成交额
            stock_day['stock_vol'].append(_vol)  # 成交量
            stock_day['stock_reservation'].append(_reservation)  # 保留值
        # while f:
        #     stock_date = f.read(4)
        #     stock_open = f.read(4)
        #     stock_high = f.read(4)
        #     stock_low = f.read(4)
        #     stock_close = f.read(4)
        #     stock_amount = f.read(4)
        #     stock_vol = f.read(4)
        #     stock_reservation = f.read(4)
        #
        #     if not stock_date or i >= 5:
        #         break
        #     stock_day['stock_date'].append(unpack("I", stock_date)[0])  # 4字节 如20091229
        #     stock_day['stock_open'].append(unpack("I", stock_open)[0] / 100)  # 开盘价*100
        #     stock_day['stock_high'].append(unpack("I", stock_high)[0] / 100)  # 最高价*100
        #     stock_day['stock_low'].append(unpack("I", stock_low)[0] / 100)  # 最低价*100
        #     stock_day['stock_close'].append(unpack("I", stock_close)[0] / 100)  # 收盘价*100
        #     stock_day['stock_amount'].append(unpack("f", stock_amount))  # 成交额
        #     stock_day['stock_vol'].append(unpack("I", stock_vol))  # 成交量
        #     stock_day['stock_reservation'].append(unpack("I", stock_reservation))  # 保留值
        #     i = i + 1


def unpack_stock_lc5(file_url, _data_size=32, _analysis_cycle=5):
    with open(file_url, r'rb') as f:
        f.seek(-_data_size * _analysis_cycle, 2)
        for i in range(0, _analysis_cycle):
            buff = f.read(32)
            a0, a1, _open, _high, _low, _close, _amount, _vol, _reservation = unpack(r"HHfffffII", buff)
            # print(_date)
            # print(_open/100)
            # a = unpack("HH", stock_date)
            _date = str(int(a0 / 2048) + 2004) + '-' + str(int(a0 % 2048 / 100)).zfill(2) + '-' + str(
                a0 % 2048 % 100).zfill(2), str(int(a1 / 60)).zfill(2) + ':' + str(a1 % 60).zfill(
                2) + ':00'
            stock_day['stock_date'].append(_date)  #
            stock_day['stock_open'].append(round(_open, 2))  # 开盘价
            stock_day['stock_high'].append(round(_high, 2))  # 最高价
            stock_day['stock_low'].append(round(_low, 2))  # 最低价
            stock_day['stock_close'].append(round(_close, 2))  # 收盘价
            stock_day['stock_amount'].append(_amount)  # 成交额
            stock_day['stock_vol'].append(_vol)  # 成交量
            stock_day['stock_reservation'].append(_reservation)  # 保留值


def my_walk(_file_directory):
    root, dirs, files = tuple(os.walk(_file_directory))[0]
    file_set = []
    for file in files:
        if file_rule.match(file):
            file_set.append(os.path.join(_file_directory, file))
    for file_url in file_set:
        print(file_url)
        file_size = os.path.getsize(file_url)
        print(file_size)
        with open(file_url, r'rb') as fp:
            if file_size >= data_size * analysis_cycle:
                fp.seek(-data_size * analysis_cycle, os.SEEK_END)
                print('大于')
            else:
                fp.seek(0, os.SEEK_SET)
                print('小于size')

    print(file_set)


if __name__ == "__main__":
    # file_path_day_sh = r"D:\通达信\new_tdx\vipdoc\sh\lday"
    file_path_day_sh = r"F:\PycharmProjects\gpfx\test_re"
    # my_walk(file_path_day_sh)
    file_url = r"F:\PycharmProjects\gpfx\test_re\sh000904.day"
    # name, ext = os.path.splitext(file_url)
    name2 = os.path.basename(file_url)
    name, ext = os.path.splitext(name2)
    print(name)
    print('ext:', ext)
    print(name2)
    # print(re_rule)
    # open_file_directory(file_path)
    # unpack_stock_day(r"F:\PycharmProjects\gpfx\sz000028.day")
    # unpack_stock_lc5(r"F:\PycharmProjects\gpfx\sz000028.lc5")
    # print(stock_day['stock_date'])
    # print(stock_day['stock_open'])
    # print(stock_day['stock_high'])
    # print(stock_day['stock_low'])
    # print(stock_day['stock_close'])
    # print(stock_day['stock_amount'])
