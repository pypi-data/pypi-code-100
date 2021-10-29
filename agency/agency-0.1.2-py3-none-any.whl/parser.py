import typing

import parse

from . import models

class Parser:
    @staticmethod
    def chunk(user_agent: str) -> typing.List[str]:
        chunks: typing.List[str] = []

        segment: str
        for segment in user_agent.split():
            if '/' in segment or not chunks:
                chunks.append(segment)
            else:
                chunks[-1] += f' {segment}'

        return chunks

    @classmethod
    def parse(cls, user_agent: str) -> models.UserAgent:
        products: typing.List[models.Product] = []

        segment: str
        for segment in cls.chunk(user_agent):
            segment = segment.strip()

            comments: typing.List[str] = []

            result: typing.Optional[parse.Result]
            if (result := parse.search('({})', segment)):
                comment: str                    = result.fixed[0]
                span:    typing.Tuple[int, int] = result.spans[0]

                comments = list(map(str.strip, comment.split(';')))

                segment = segment[:span[0] - 1].strip()

            if (result := parse.parse('{}/{}', segment)):
                name:    str
                version: str
                name, version = result.fixed

                product = models.Product \
                (
                    identifier = models.ProductIdentifier \
                    (
                        name    = name,
                        version = version,
                    ),
                    comments = comments,
                )

                products.append(product)

        return models.UserAgent \
        (
            products = products
        )
