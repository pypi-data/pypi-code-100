import disnake

class ChannelResponseWrapper:
    def __init__(self, channel):
        self.channel = channel
        self.sent_message = None

    async def defer(self, ephemeral=False):
        self.sent_message = await self.channel.send("I am thinking...")
    
    async def send_message(self, content=None, embed=None, view=None, ephemeral=False):
        self.sent_message = await self.channel.send(content=content, embed=embed, view=view)

    async def edit_message(self, content=None, embed=None, view=None):
        if content == None:
            content = self.sent_message.content
        if embed == None:
            if len(self.sent_message.embeds) > 0:
                embed = self.sent_message.embeds[0]
        await self.sent_message.edit(content=content, embed=embed, view=view)

class UserInteractionWrapper:
    def __init__(self, user):
        self.name = "MessageInteractionWrapper"
        self.id = user.id
        self.author = user
        self.guild = None
        self.created_at = user.created_at
        if type(user) == disnake.Member:
            self.guild = user.guild
        self.response = ChannelResponseWrapper(user)

    async def edit_original_message(self, content=None, embed=None, view=None):
        await self.response.edit_message(content=content, embed=embed, view=view)

class MessageInteractionWrapper:
    def __init__(self, message):
        self.name = "MessageInteractionWrapper"
        self.id = message.id
        self.author = message.author
        self.channel = message.channel
        self.created_at = message.created_at
        self.guild = message.guild
        self.response = ChannelResponseWrapper(message.channel)

    async def edit_original_message(self, content=None, embed=None, view=None):
        await self.response.edit_message(content=content, embed=embed, view=view)

