import pandas_datareader as pdr
from config import tiingo_token
import numpy as np
from findiff import FinDiff
import findiff
import datetime
import os
import time

trend = 0
# Текущий тренд: 0 - не определено, 1 - восходящий, -1 - нисходящий

ticker = 'TSLA'
nowdate = datetime.datetime.now()
lastdate = nowdate - datetime.timedelta(days = 45)

data = pdr.get_data_tiingo(ticker,
                           api_key = tiingo_token,
                           start = f'{lastdate.year}-{lastdate.month}-{lastdate.day}',
                           end = f'{nowdate.year}-{nowdate.month}-{nowdate.day}'
)
# Получение показателей по тикеру

def get_extrema(isMin):
  return [x for x in range(len(mom))
    if (momacc[x] > 0 if isMin else momacc[x] < 0) and
      (mom[x] == 0 or #slope is 0
        (x != len(mom) - 1 and #check next day
          (mom[x] > 0 and mom[x+1] < 0 and
           h[x] >= h[x+1] or
           mom[x] < 0 and mom[x+1] > 0 and
           h[x] <= h[x+1]) or
         x != 0 and #check prior day
          (mom[x-1] > 0 and mom[x] < 0 and
           h[x-1] < h[x] or
           mom[x-1] < 0 and mom[x] > 0 and
           h[x-1] > h[x])))]

#uturnpoints = data[data['close'] > data['close'][]]['close']

#gain_items = data[1:][data['close'].values[1:] > data['close'][:-1].values]
#print(gain_items)

def eval_rsi(data, period):
    data['index'] = list(range(0, data['close'].size))
    # Индексация массива

    gain_items = data[1:][data['close'][1:].values > data['close'][:-1].values]
    losses_items = data[1:][data['close'][1:].values < data['close'][:-1].values]
    # Сборка подъёмов и падений

    gain_items['ewm'] = gain_items['close'].ewm(span = period, min_periods = 0, ignore_na = False).mean()
    losses_items['ewm'] = losses_items['close'].ewm(span = period, min_periods = 0, ignore_na = False).mean()
    # Экспонинциальное сглаживание цен

    data['RSI'] = [100 - (100 / (1 + (gain_items[gain_items['index'].values <= d + 1]['ewm'][d-period:d+1].sum() / period) /
                                     (losses_items[losses_items['index'].values <= d + 1]['ewm'][d-period:d+1].sum() / period)))
                                     for d in data['index'].values]

    # Расчёт индикатора RSI

    return data

data = eval_rsi(data, 14)
print(data)

time.sleep(100)
dx = 1 #1 day interval
d_dx = FinDiff(0, dx, 1)
d2_dx2 = FinDiff(0, dx, 2)
clarr = np.asarray(data['close'])
mom = d_dx(clarr)
momacc = d2_dx2(clarr)

#print(data.head())
#print(mom)

#coeff = findiff.coefficients(deriv = 1, acc = 1)
#print(coeff)
