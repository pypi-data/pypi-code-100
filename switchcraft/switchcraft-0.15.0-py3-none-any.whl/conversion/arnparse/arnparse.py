"""Arn.

A simple class that parses Amazon Resource Names (ARNs) and returns its
parts.
"""

from dataclasses import InitVar, asdict, dataclass, field

from switchcraft.exceptions import MalformedArnError


@dataclass
class Arn:
    arn: InitVar[str]
    partition: str = field(init=False)
    service: str = field(init=False)
    region: str = field(init=False)
    account_id: str = field(init=False)
    resource_type: str = field(init=False)
    resource_id: str = field(init=False)

    def __post_init__(self, arn):
        if not arn.startswith('arn:'):
            raise MalformedArnError

        elements = arn.split(':')
        self.partition = elements[1]
        self.service = elements[2]
        self.region = elements[3]
        self.account_id = elements[4]

        if len(elements) == 6:
            res_elements = elements[5].split('/')
            if len(res_elements) == 1:
                self.resource_type = ""
                self.resource_id = elements[5]
            else:
                self.resource_type = res_elements[0]
                self.resource_id = '/'.join(res_elements[1:])

        if len(elements) == 7:
            self.resource_type = elements[5]
            self.resource_id = elements[6]

    def as_dict(self):
        return asdict(self)
