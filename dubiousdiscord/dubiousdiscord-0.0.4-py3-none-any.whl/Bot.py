
from __future__ import annotations

import inspect
import re
from dataclasses import asdict
from typing import Optional, get_args

import aiohttp

from dubious.Mess import Mess
from dubious.enums import commandTypes, events, interactionCallbackDataFlags, interactionCallbackTypes as ixnCallbackTypes, interactionTypes
from dubious.Listen import Listen, Listener
from dubious.io.Http import HTTPError, Http
from dubious.objects import ApplicationCommand, Interaction, Member, Message, Ready, Snowflake, User, backcasting, dig
from dubious.raw import CreateCommand, CreateCommandOption

namere = re.compile(r"^[a-z_-]{1,32}$")
class Option:
    def __init__(self, name: str, t: type, description: str, choices: Optional[list]=None):
        self.name = name
        self.typeCls = dig(t)
        self.description = description
        self.choices = choices if choices else []
        self.required = not (t != self.typeCls and type(None) in get_args(t))

        if not namere.match(self.name):
            raise Exception(f"Option name {self.name} was invalid")
        if len(self.description) > 100:
            raise Exception(f"Option {self.name}'s description is too long")
        
        if self.typeCls in backcasting: self.type = backcasting[self.typeCls]
        else: raise TypeError(f"Type {self.typeCls} for option {self.name} wasn't a valid type.")

    def asJson(self) -> CreateCommandOption:
        j = {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required
        }
        if self.choices:
            j["choices"] = [{"name": choice, "value": choice} for choice in self.choices]
        return j

class Command(Listen):    
    def __init__(self, description: Optional[str], options: Optional[dict[str, str | list]]=None, guildID: Optional[int]=None):
        self.description = description if description else "No description given."
        self.guildID = guildID
        options = options if options else {}

        if not namere.match(self.name):
            raise Exception(f"Command name {self.name} was invalid")
        if len(self.description) > 100:
            raise Exception(f"Command {self.name}'s description is too long")
        
        self.options: list[Option] = []
        sig = inspect.signature(self.callback)
        for parameter in sig.parameters:
            optName = parameter
            optType = sig.parameters[parameter].annotation
            if optName == "self" or optType == Ixn: continue
            # if list was given for options field, the first str is the description and the rest are choices for the option
            optDesc = options.get(parameter)
            optSxns = optDesc[1:] if isinstance(optDesc, list) else None

            if not optDesc: optDesc = "No description given."
            self.options.append(Option(optName, optType, optDesc, optSxns))
    
    def asJson(self) -> CreateCommand:
        j = {
            "name": self.name,
            "type": commandTypes.chatInput,
            "description": self.description if self.description else "No description given."
        }
        if self.options:
            j["options"] = [option.asJson() for option in self.options]
        return j
    
    def compare(self, to: ApplicationCommand):
        #print(f"Comparing {self.name} with {to.name}")
        selfJson = self.asJson()
        discordJson = asdict(to)
        #print(selfJson.get("description"))
        #print(discordJson.get("description"))
        #print(selfJson.get("options"))
        #print(discordJson.get("options"))
        return (
            selfJson.get("description") == discordJson.get("description") and
            selfJson.get("options") == discordJson.get("options")
        )

class Callback(Listen):
    pass

class Ixn:
    def __init__(self, appID: Snowflake, ixnID: Snowflake, ixnToken: str, ixnType: int, http: Http, message: Optional[Message], member: Optional[Member], user: Optional[User], guildID: Optional[Snowflake], channelID: Optional[Snowflake]):
        self.id = ixnID
        self.appID = appID
        self.token = ixnToken

        self.callback = http.interactions(self.id, self.token)

        self.http = http
        
        self.message = message
        self.user = member.user if member else user
        self.member = member
        self.guildID = guildID
        self.channelID = channelID

        self.type = ixnType
    
    async def getGuild(self):
        return await self.http.guilds(self.guildID).get()
    
    async def getChannel(self):
        return await self.http.channels(self.channelID).get()
    
    async def getOriginalMessage(self) -> Message:
        return await self.http.webhookMessages(self.appID, self.token, "@original").get()
    
    def _makeMess(self, response: str | Mess, private: bool=False):
        if isinstance(response, Mess):
            res = response.asJson()
        else:
            res = {"content": response}
        if private:
            flags = res.get("flags", 0)
            flags |= interactionCallbackDataFlags.ephemeral
            res["flags"] = flags
        return res
    
    def _makeResponse(self, response: str | Mess, private: bool=False):
        res: dict[str, int | dict[str, int | str]] = {
            "type": ixnCallbackTypes.commandRespondWithMessage,
            "data": self._makeMess(response, private)
        }
        return res
    
    async def respond(self, response: str | Mess, private: bool=False):
        res = self._makeResponse(response, private)
        await self.callback.post(res)
    
    async def followup(self, response: str | Message, private: bool=False):
        res = self._makeMess(response, private)
        return await self.http.webhookMessages(self.appID, self.token).post(res)
    
    async def edit(self, response: str | Mess, messageID: str | Snowflake = "@original"):
        res = self._makeMess(response)
        return await self.http.webhookMessages(self.appID, self.token, messageID).patch(res)
    
    async def delete(self, messageID: str | Snowflake = "@original"):
        return await self.http.webhookMessages(self.appID, self.token, messageID).delete()
    
    async def acknowledge(self):
        return await self.callback.post({
            "type": ixnCallbackTypes.componentRespondLater
        })

class Wing(Listener):
    def __init__(self):
        super().__init__()

        self.commands: dict[str, Command] = {}
        self.callbacks: dict[str, Callback] = {}
        for listenName in self.toListen:
            listen: Listen = self.toListen[listenName]
            if isinstance(listen, Command): self.commands[listenName] = listen
            if isinstance(listen, Callback): self.callbacks[listenName] = listen

class Bot(Listener):
    wingClasses: list[type[Wing]] = []
    testing: bool = False
    testIn: Snowflake | int | None = None

    user: User
    guildIDs: list[Snowflake]
    id: Snowflake
    wings: list[Wing]

    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.wings = [wing() for wing in self.wingClasses]

        self.commands: dict[str, Wing] = {}
        self.callbacks: dict[str, Wing] = {}

    @Listen(events.onReady)
    async def onReady(self, ready: Ready):
        self.user = ready.user
        self.guildIDs = [guild.id for guild in ready.guilds]
        self.id = ready.application.id

        self.http = Http(self.id, self.token, aiohttp.ClientSession())

        discordCommands: list[ApplicationCommand] = await self.http.commands().get()
        for guildID in self.guildIDs:
            try: discordCommands += await self.http.commands(guildID=guildID).get()
            except HTTPError: print(f"Missing permissions to get commands from guild {guildID}.")
        registered = {command.name: command for command in discordCommands}
        dupecheckCommands = set()
        for wing in self.wings:
            await self.collectCommands(wing, dupecheckCommands, registered)
            await self.collectCallbacks(wing)
        
        for remaining in registered.values():
            # for any commands that weren't found as a part of the wings' commands, delete
            await self.http.commands(remaining.id, remaining.guild_id).delete()
    
    async def collectCommands(self, wing: Wing, dupecheck: set[str], registered: dict[str, ApplicationCommand]):
        for commandName, command in wing.commands.items():
            if commandName in dupecheck: raise Exception(f"Duplicate command name from wing {wing.__class__.__name__}: {commandName}")
            command.guildID = self.testIn if self.testing else command.guildID
            dupecheck.add(commandName)
    
            if command.name in registered:
                # check whether or not it's the same as what we've got
                discordCommand = registered[command.name]
                if not command.compare(discordCommand):
                    appCommand = await self.http.commands(discordCommand.id, discordCommand.guild_id).patch(command.asJson())
                else:
                    appCommand = discordCommand
                registered.pop(command.name)
            else:
                # register the command fresh
                appCommand = await self.http.commands(guildID=command.guildID).post(command.asJson())
            self.commands[appCommand.name] = wing
    
    async def collectCallbacks(self, wing: Wing):
        for callbackName in wing.callbacks:
            self.callbacks[callbackName] = wing
    
    async def trigger(self, event: str, *args, **kwargs):
        await super().trigger(event, *args, **kwargs)
        for wing in self.wings:
            await wing.trigger(event, *args, **kwargs)
    
    @Listen(events.onInteractionCreate)
    async def onInteractionCreate(self, interaction: Interaction):
        data = interaction.data
        #print(f"recieved interaction: {data.name if data.name else data.custom_id}")
        ixn = Ixn(self.id, interaction.id, interaction.token, interaction.type, self.http, interaction.message, interaction.member, interaction.user, interaction.guild_id, interaction.channel_id)
        if interaction.type == interactionTypes.applicationCommand:
            wing = self.commands[data.name]
            await wing.trigger(data.name, ixn, **data.getOptions(data.resolved))
        elif interaction.type == interactionTypes.messageComponent:
            wing = self.callbacks[data.custom_id]
            await wing.trigger(data.custom_id, ixn)