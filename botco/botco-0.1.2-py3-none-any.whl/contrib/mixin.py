from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from botco.bot import Bot


class BotObjectMixin:
    bot: Optional["Bot"] = None

    class Config:
        pass

    def set_bot(self, bot):
        self.Config.allow_mutation = True
        self.bot = bot
        self.Config.allow_mutation = False
