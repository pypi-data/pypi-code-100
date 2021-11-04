from pydantic.main import BaseModel


class TsMin(BaseModel):
    TsCode = ''
    Freq = ''
    TradeTime = ''
    Open = ''
    Close = ''
    High = ''
    Low = ''
    Volume = ''
    Amount = ''
    OpenInterest = ''
