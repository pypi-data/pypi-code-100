from typing import Optional, List


class RangeItems:
    def __init__(self, range_from: Optional[int] = None, range_to: Optional[int] = None,
                 range_id: Optional[int] = None):
        # range_id为1表示红包抵后价（单位分）， range_id为2表示佣金比例（单位千分之几)
        self.range_from = range_from
        self.range_to = range_to
        self.range_id = range_id


class DIYRedPacketParam:
    def __init__(self, amount_probability: Optional[List[int]], dis_text: Optional[bool],
                 not_show_background: Optional[bool], opt_id: Optional[int],
                 range_from: Optional[int] = None, range_to: Optional[int] = None,
                 range_id: Optional[int] = None):
        self.amount_probability: Optional[List[int]] = amount_probability
        self.dis_text: Optional[bool] = dis_text
        self.not_show_background: Optional[bool] = not_show_background
        self.opt_id: Optional[int] = opt_id
        self.range_items = RangeItems(range_from, range_to, range_id)
