from google.protobuf import json_format

from tushare.subs.model.min import TsMin
from tushare.subs.model.tick import TsTick, TsTickIdx, TsTickOpt, TsTickFuture

datatype_map = {
    "TICK": 1,
    "TRANSACTION": 2,
    "ORDER": 3,
    "1MIN": 20,
    "5MIN": 21,
    "15MIN": 22,
    "30MIN": 23,
    "60MIN": 24,
    "1DAY": 25,
    "15SECOND": 26
}
datatype_map1 = {v: k for k, v in datatype_map.items()}


def convert_ts_model(inst):
    inst_data = json_format.MessageToDict(inst)
    ts_inst = None
    if 'MIN' in inst_data['marketDataType']:
        ts_inst = convert_min_model(inst)
    elif 'TICK' in inst_data['marketDataType'] and 'mdStock' in inst_data:
        ts_inst = convert_tick_stock(inst_data['mdStock'])
    elif 'TICK' in inst_data['marketDataType'] and 'mdFund' in inst_data:
        ts_inst = convert_tick_stock(inst_data['mdFund'])
    elif 'TICK' in inst_data['marketDataType'] and 'mdBond' in inst_data:
        ts_inst = convert_tick_stock(inst_data['mdBond'])
    elif 'TICK' in inst_data['marketDataType'] and 'mdIndex' in inst_data:
        ts_inst = convert_tick_index(inst_data['mdIndex'])
    elif 'TICK' in inst_data['marketDataType'] and 'mdOption' in inst_data:
        ts_inst = convert_tick_option(inst_data['mdOption'])

    return dict(ts_inst), inst_data


def convert_min_model(ht_inst):
    inst = TsMin()
    ds = str(ht_inst.mdKLine.MDDate)
    ts = str(ht_inst.mdKLine.MDTime)
    inst.TsCode = ht_inst.mdKLine.HTSCSecurityID
    inst.Freq = datatype_map1[ht_inst.marketDataType]
    inst.TradeTime = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}'
    inst.Open = ht_inst.mdKLine.OpenPx
    inst.Close = ht_inst.mdKLine.ClosePx
    inst.High = ht_inst.mdKLine.HighPx
    inst.Low = ht_inst.mdKLine.LowPx
    inst.Volume = ht_inst.mdKLine.TotalVolumeTrade
    inst.Amount = ht_inst.mdKLine.TotalValueTrade
    inst.OpenInterest = ht_inst.mdKLine.KLineCategory
    return inst


def convert_tick_stock(md_stock):
    inst = TsTick()
    ds = str(md_stock['MDDate'])
    ts = str(md_stock['MDTime'])
    inst.TsCode = md_stock['HTSCSecurityID']
    inst.Name = ''
    inst.TradeTime = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.PrePrice = md_stock.get('PreClosePx')
    inst.Price = md_stock.get('LastPx')
    inst.Open = md_stock.get('OpenPx')
    inst.High = md_stock.get('HighPx')
    inst.Low = md_stock.get('LowPx')
    inst.Close = md_stock.get('ClosePx')
    inst.OpenInt = md_stock.get('OpenInterest')    # ����û��
    inst.Volume = md_stock.get('TotalVolumeTrade')
    inst.Amount = md_stock.get('TotalValueTrade')
    inst.Num = md_stock.get('NumTrades')
    for i, v in enumerate(md_stock.get('SellPriceQueue')):
        setattr(inst, f'AskPrice{i+1}', v)
    for i, v in enumerate(md_stock.get('SellOrderQtyQueue')):
        setattr(inst, f'AskVolume{i+1}', v)
    for i, v in enumerate(md_stock.get('BuyPriceQueue')):
        setattr(inst, f'BidPrice{i+1}', v)
    for i, v in enumerate(md_stock.get('BuyOrderQtyQueue')):
        setattr(inst, f'BidVolume{i+1}', v)

    return inst


def convert_tick_index(md_index):
    inst = TsTickIdx()
    ds = str(md_index['MDDate'])
    ts = str(md_index['MDTime'])
    inst.TsCode = md_index['HTSCSecurityID']
    inst.Name = ''
    inst.TradeTime = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.PrePrice = md_index.get('PreClosePx')
    inst.Price = md_index.get('LastPx')
    inst.Open = md_index.get('OpenPx')
    inst.High = md_index.get('HighPx')
    inst.Low = md_index.get('LowPx')
    # inst.Close = md_index.get('ClosePx')
    # inst.OpenInt = md_index.get('OpenInterest')    # ����û��
    inst.Volume = md_index.get('TotalVolumeTrade')
    inst.Amount = md_index.get('TotalValueTrade')
    return inst


def convert_tick_option(md_option):
    inst = TsTickOpt()
    ds = str(md_option['MDDate'])
    ts = str(md_option['MDTime'])
    inst.TsCode = md_option['HTSCSecurityID']
    inst.InstrumentID = ''
    inst.TradeTime = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.PrePrice = md_option.get('PreClosePx')
    inst.Price = md_option.get('LastPx')
    inst.Open = md_option.get('OpenPx')
    inst.High = md_option.get('HighPx')
    inst.Low = md_option.get('LowPx')
    inst.Close = md_option.get('ClosePx')
    inst.OpenInt = md_option.get('OpenInterest')    # ����û��
    inst.Volume = md_option.get('TotalVolumeTrade')
    inst.Amount = md_option.get('TotalValueTrade')
    inst.Num = md_option.get('NumTrades')
    inst.AskPrice1 = md_option.get('BuyPriceQueue')[0]
    inst.AskVolume1 = md_option.get('BuyOrderQtyQueue')[0]
    inst.BidPrice1 = md_option.get('SellPriceQueue')[0]
    inst.BidVolume1 = md_option.get('SellOrderQtyQueue')[0]
    inst.PreDelta = md_option.get('PreDelta')
    inst.CurrDelta = md_option.get('CurrDelta')
    inst.DifPrice1 = md_option.get('DiffPx1')
    inst.DifPrice2 = md_option.get('DiffPx2')
    inst.HighLimitPrice = md_option.get('MaxPx')
    inst.LowLimitPrice = md_option.get('MinPx')
    inst.ReferPrice = md_option.get('ReferencePx')
    return inst


def convert_tick_future(md_future):
    inst = TsTickFuture()
    ds = str(md_future['MDDate'])
    ts = str(md_future['MDTime'])
    inst.TsCode = md_future['HTSCSecurityID']
    inst.Name = ''
    inst.TradeTime = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.PrePrice = md_future.get('PreClosePx')
    inst.Price = md_future.get('LastPx')
    inst.Open = md_future.get('OpenPx')
    inst.High = md_future.get('HighPx')
    inst.Low = md_future.get('LowPx')
    inst.Close = md_future.get('ClosePx')
    inst.OpenInt = md_future.get('OpenInterest')    # ����û��
    inst.Volume = md_future.get('TotalVolumeTrade')
    inst.Amount = md_future.get('TotalValueTrade')
    inst.Num = md_future.get('NumTrades')
    inst.AskPrice1 = md_future.get('BuyPriceQueue')[0]
    inst.AskVolume1 = md_future.get('BuyOrderQtyQueue')[0]
    inst.BidPrice1 = md_future.get('SellPriceQueue')[0]
    inst.BidVolume1 = md_future.get('SellOrderQtyQueue')[0]
    inst.PreDelta = md_future.get('PreDelta')
    inst.CurrDelta = md_future.get('CurrDelta')
    inst.DifPrice1 = md_future.get('DiffPx1')
    inst.DifPrice2 = md_future.get('DiffPx2')
    inst.HighLimitPrice = md_future.get('MaxPx')
    inst.LowLimitPrice = md_future.get('MinPx')
    inst.ReferPrice = md_future.get('ReferencePx')
    inst.PreSettlePrice = md_future.get('PreSettlePrice')
    inst.SettlePrice = md_future.get('SettlePrice')
    return inst

