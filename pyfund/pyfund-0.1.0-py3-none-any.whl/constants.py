import os
from enum import Enum


IS_DEBUG = False

# print(os.environ['HOME'])
# print(os.path.expandvars('$HOME'))
DATA_PATH = os.path.join(os.path.expanduser('~'), 'pyfund-datas')
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

# indicator
I_TIMESTAMP = 'timestamp'
I_DATE = 'date'
I_VOLUME = 'volume'
I_OPEN = 'open'
I_HIGH = 'high'
I_LOW = 'low'
I_CLOSE = 'close'
I_CHG = 'chg'
I_PERCENT = 'percent'
I_TURNOVERRATE = 'turnoverrate'
I_AMOUNT = 'amount'
I_VOLUME_POST = 'volume_post'
I_AMOUNT_POST = 'amount_post'
I_MA5 = 'ma5'
I_MA10 = 'ma10'
I_MA20 = 'ma20'
I_MA30 = 'ma30'
I_DEA = 'dea'
I_DIF = 'dif'
I_MACD = 'macd'
I_MACDX = 'macdx'
I_UB = 'ub'
I_LB = 'lb'
I_BOLL = 'boll'
I_KDJK = 'kdjk'
I_KDJD = 'kdjd'
I_KDJJ = 'kdjj'
I_RSI1 = 'rsi1'
I_RSI2 = 'rsi2'
I_RSI3 = 'rsi3'
I_WR6 = 'wr6'
I_WR10 = 'wr10'
I_BIAS1 = 'bias1'
I_BIAS2 = 'bias2'
I_BIAS3 = 'bias3'
I_CCI = 'cci'
I_PSY = 'psy'
I_PSYMA = 'psyma'
I_PE = 'pe'
I_PB = 'pb'
I_ROE = 'roe'
I_PS = 'ps'
I_PCF = 'pcf'
I_MARKET_CAPITAL = 'market_capital'
I_CR_VOLUME = 'cr_volume'
I_CR_CLOSE = 'cr_close'
I_CR_KDJD = 'cr_kdjd'
I_CR_MA5 = 'cr_ma5'
I_CR_MA10 = 'cr_ma10'
I_CR_MA20 = 'cr_ma20'
I_CR_DEA = 'cr_dea'
I_CR_DIF = 'cr_dif'
I_CR_MACD = 'cr_macd'
