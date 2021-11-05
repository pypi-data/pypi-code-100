from pydantic.main import BaseModel


class TsMin(BaseModel):
    ts_code = ''
    freq = ''
    trade_time = ''
    open = ''
    close = ''
    high = ''
    low = ''
    vol = ''
    amount = ''
    open_int = ''
