from botco.types import TelegramObject, Message


class BaseFilter:
    keys: tuple = None

    def __call__(self, *args, **kwargs):
        pass

    def check(self, obj: TelegramObject, filters: dict) -> bool:
        pass


class Hashtag:
    def __call__(self, hashtag: str = None):
        def decorator(obj: Message):
            if obj.entities:
                for entity in obj.entities:
                    if entity.type == "hashtag":
                        if hashtag:
                            return hashtag == obj.text[entity.offset + 1: entity.length]
                        return True
            return False

        return decorator


class Url:
    def __call__(self, url: str = None):
        def decorator(obj: Message):
            if obj.entities:
                for entity in obj.entities:
                    if entity.type == "url" or entity.type == "text_link":
                        if url:
                            return url == obj.text[entity.offset + 1: entity.length]
                        return True
            return False

        return decorator


class Cashtag:
    def __call__(self, url: str = None):
        def decorator(obj: Message):
            if obj.entities:
                for entity in obj.entities:
                    if entity.type == "cashtag":
                        if url:
                            return url == obj.text[entity.offset + 1: entity.length]
                        return True
            return False

        return decorator


HashtagFilter = Hashtag()
CashtagFilter = Cashtag()
UrlFilter = Url()
