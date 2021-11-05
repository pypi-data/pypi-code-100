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

    return ts_inst and dict(ts_inst) or None, inst_data


def convert_min_model(ht_inst) -> TsMin:
    inst: TsMin = TsMin()
    ds = str(ht_inst.mdKLine.MDDate)
    ts = str(ht_inst.mdKLine.MDTime)
    inst.ts_code = ht_inst.mdKLine.HTSCSecurityID
    inst.freq = datatype_map1[ht_inst.marketDataType]
    inst.trade_time = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}'
    inst.open = ht_inst.mdKLine.OpenPx
    inst.close = ht_inst.mdKLine.ClosePx
    inst.high = ht_inst.mdKLine.HighPx
    inst.low = ht_inst.mdKLine.LowPx
    inst.vol = ht_inst.mdKLine.TotalVolumeTrade
    inst.amount = ht_inst.mdKLine.TotalValueTrade
    inst.open_int = ht_inst.mdKLine.KLineCategory
    return inst


def convert_tick_stock(md_stock) -> TsTick:
    inst: TsTick = TsTick()
    ds = str(md_stock['MDDate'])
    ts = str(md_stock['MDTime'])
    inst.ts_code = md_stock['HTSCSecurityID']
    inst.name = ''
    inst.trade_time = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.pre_price = md_stock.get('PreClosePx')
    inst.price = md_stock.get('LastPx')
    inst.open = md_stock.get('OpenPx')
    inst.high = md_stock.get('HighPx')
    inst.low = md_stock.get('LowPx')
    inst.close = md_stock.get('ClosePx')
    inst.open_int = md_stock.get('OpenInterest')    # ����û��
    inst.vol = md_stock.get('TotalVolumeTrade')
    inst.amount = md_stock.get('TotalValueTrade')
    inst.num = md_stock.get('NumTrades')
    for i, v in enumerate(md_stock.get('SellPriceQueue')):
        setattr(inst, f'ask_price{i+1}', v)
    for i, v in enumerate(md_stock.get('SellOrderQtyQueue')):
        setattr(inst, f'ask_volume{i+1}', v)
    for i, v in enumerate(md_stock.get('BuyPriceQueue')):
        setattr(inst, f'bid_price{i+1}', v)
    for i, v in enumerate(md_stock.get('BuyOrderQtyQueue')):
        setattr(inst, f'bid_volume{i+1}', v)

    return inst


def convert_tick_index(md_index) -> TsTickIdx:
    inst: TsTickIdx = TsTickIdx()
    ds = str(md_index['MDDate'])
    ts = str(md_index['MDTime'])
    inst.ts_code = md_index['HTSCSecurityID']
    inst.name = ''
    inst.trade_time = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.pre_price = md_index.get('PreClosePx')
    inst.price = md_index.get('LastPx')
    inst.open = md_index.get('OpenPx')
    inst.high.Low = md_index.get('LowPx')
    # inst.Close = md_index.get('ClosePx')
    # inst.OpenInt = md_index.get('OpenInterest')    # ����û��
    inst.vol = md_index.get('TotalVolumeTrade')
    inst.amount = md_index.get('TotalValueTrade')
    return inst


def convert_tick_option(md_option) -> TsTickOpt:
    inst: TsTickOpt = TsTickOpt()
    ds = str(md_option['MDDate'])
    ts = str(md_option['MDTime'])
    inst.ts_code = md_option['HTSCSecurityID']
    inst.instrument_id = ''
    inst.trade_time = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.pre_price = md_option.get('PreClosePx')
    inst.price = md_option.get('LastPx')
    inst.open = md_option.get('OpenPx')
    inst.high = md_option.get('HighPx')
    inst.low = md_option.get('LowPx')
    inst.close = md_option.get('ClosePx')
    inst.open_int = md_option.get('OpenInterest')    # ����û��
    inst.vol = md_option.get('TotalVolumeTrade')
    inst.amount = md_option.get('TotalValueTrade')
    inst.num = md_option.get('NumTrades')
    inst.ask_price1 = md_option.get('BuyPriceQueue')[0]
    inst.ask_volume1 = md_option.get('BuyOrderQtyQueue')[0]
    inst.bid_price1 = md_option.get('SellPriceQueue')[0]
    inst.bid_volume1 = md_option.get('SellOrderQtyQueue')[0]
    inst.pre_delta = md_option.get('PreDelta')
    inst.curr_delta = md_option.get('CurrDelta')
    inst.dif_price1 = md_option.get('DiffPx1')
    inst.dif_price2 = md_option.get('DiffPx2')
    inst.high_limit_price = md_option.get('MaxPx')
    inst.low_limit_price = md_option.get('MinPx')
    inst.refer_price = md_option.get('ReferencePx')
    return inst


def convert_tick_future(md_future) -> TsTickFuture:
    inst: TsTickFuture = TsTickFuture()
    ds = str(md_future['MDDate'])
    ts = str(md_future['MDTime'])
    inst.ts_code = md_future['HTSCSecurityID']
    inst.trade_time = f'{ds[:4]}-{ds[4:6]}-{ds[6:]} {ts[:-7]}:{ts[-7:-5]}:{ts[-5:-3]}'
    inst.pre_price = md_future.get('PreClosePx')
    inst.price = md_future.get('LastPx')
    inst.open = md_future.get('OpenPx')
    inst.high = md_future.get('HighPx')
    inst.low = md_future.get('LowPx')
    inst.close = md_future.get('ClosePx')
    inst.open_int = md_future.get('OpenInterest')    # ����û��
    inst.vol = md_future.get('TotalVolumeTrade')
    inst.amount = md_future.get('TotalValueTrade')
    inst.num = md_future.get('NumTrades')
    inst.ask_price1 = md_future.get('BuyPriceQueue')[0]
    inst.ask_volume1 = md_future.get('BuyOrderQtyQueue')[0]
    inst.bid_price1 = md_future.get('SellPriceQueue')[0]
    inst.bid_volume1 = md_future.get('SellOrderQtyQueue')[0]
    inst.pre_delta = md_future.get('PreDelta')
    inst.curr_delta = md_future.get('CurrDelta')
    inst.dif_price1 = md_future.get('DiffPx1')
    inst.dif_price2 = md_future.get('DiffPx2')
    inst.high_limit_price = md_future.get('MaxPx')
    inst.low_limit_price = md_future.get('MinPx')
    inst.refer_price = md_future.get('ReferencePx')
    inst.pre_settle_price = md_future.get('PreSettlePrice')
    inst.settle_price = md_future.get('SettlePrice')
    return inst

