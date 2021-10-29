import dataclasses
import typing

@dataclasses.dataclass
class ProductIdentifier:
    name:     str
    version:  str

    def __str__(self) -> str:
        return f'{self.name}/{self.version}'

@dataclasses.dataclass
class Product:
    identifier: ProductIdentifier
    comments:   typing.List[str] = dataclasses.field(default_factory = list)

    def __str__(self):
        return str(self.identifier) + \
        (
            ' ({comment})'.format \
            (
                comment = '; '.join(self.comments),
            )
            if self.comments
            else ''
        )

@dataclasses.dataclass
class UserAgent:
    products: typing.List[Product]

    def __str__(self):
        return ' '.join(map(str, self.products))
