import pretty_errors
import numpy
import talib
close = numpy.random.random(100)

# 均线系:
sma= talib.SMA(close, timeperiod=30) #simple moving average
# talib中MA与SMA是完全相同的函数, EMA是指数滑动平均, 常用于计算
u, m, l= talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
# 与手动运算的相同, 其上下界是当前段标准差的指定倍数
dif, dem, histogram = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

print(sma)
print(u, m, l)
print(dif, dem, histogram)
