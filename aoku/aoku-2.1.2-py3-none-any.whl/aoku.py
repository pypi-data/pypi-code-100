import os
import ast
import random
import json

import string
import logging
import discord

from discord.ext import commands
from discord.utils import get
from discord_components import *

import youtube_dl
from datetime import datetime, timedelta
import subprocess

import time
import requests

class newCommandir:

	"""
	Writes commands to a list for further storage
	"""

	aokuCommands = []

	def __init__(self, name: str = None, code: list = None):
		self.name = name
		self.code = code
		self.split = ";."

		newCommandir.aokuCommands.append(self)

class aokuBot(newCommandir):
	def __init__(self, intents: bool = None, selfbot: bool = None):
		"""
		create aokuBot for future use
		:param (bool) intents: turn on or turn off intents
		:param (bool) selfbot: turn on or turn off selfbot
		"""
		self.intents = intents
		self.selfbot = selfbot
		if self.intents == True and self.selfbot == True:
			self.client = commands.Bot(command_prefix = "aoku!", intents = discord.Intents.all(), self_bot = True)
		elif self.intents == False and self.selfbot == False:
			self.client = commands.Bot(command_prefix = "aoku!")
		elif self.intents == False and self.selfbot == True:
			self.client = commands.Bot(command_prefix = "aoku!", self_bot = True)
		elif self.intents == True and self.selfbot == False:
			self.client = commands.Bot(command_prefix = "aoku!", intents = discord.Intents.all())

	def onReady(self, text):
		@self.client.event
		async def on_ready():
			"""
			Prints a message to the screen when the bot is ready to use
			"""
			DiscordComponents(self.client)
			print(text)

	def newCommand(self, name: str = None, code: list = None):
		"""
		create a new command
		:param (str) name: commandName
		:param (list) code: code of your command
		"""
		commandName = name
		commandCode = code

		newCommandir.aokuCommands.append([commandName, commandCode])

	def onMessage(self):
		"""
		Allows the bot to use commands
		"""
		newCommandir.aokuCommands = [*newCommandir.aokuCommands]

		@self.client.event
		async def on_message(message):
			if not message.author.bot:
				for aokuinfo in newCommandir.aokuCommands:
					aokuname = aokuinfo[0]
					aokucode = aokuinfo[1]

					if str(message.content).startswith(aokuname):

						channel = message.channel

						codestatus = {
							"onlyForIDs": False,
							"onlyAdmin": False,
							"onlyForServers": False
						}

						embed = discord.Embed()
						botinfo = await self.client.application_info()

						logger = logging.getLogger(__name__)
						c_handler = logging.StreamHandler()
						c_handler.setLevel(logging.ERROR)
						c_format = logging.Formatter('%(name)s -> %(levelname)s -> %(message)s')
						c_handler.setFormatter(c_format)

						logger.addHandler(c_handler)

						while "$aokuEval[" in aokucode:
							yacoder = aokucode.split("$aokuEval[")[1].split("]")[0]
							aokucode = aokucode.replace(f"$aokuEval[{yacoder}]", yacoder)
							break

						while "$message[" in aokucode:
							index = int(aokucode.split("$message[")[1].split("]")[0])
							aokucode = aokucode.replace(f"$message[{index}]", str("{0}".format(message.content.lstrip(f"{aokuname}").split()[index-1])))
							break

						while "$message" in aokucode:
							aokucode = aokucode.replace("$message", str("{0}".format(message.content.lstrip(f"{aokuname}"))))
							break

						while "$authorID" in aokucode:
							aokucode = aokucode.replace("$authorID", str(message.author.id))
							break

						while "$authorName" in aokucode:
							aokucode = aokucode.replace("$authorName", str(message.author.name))
							break

						while "$onlyForIDs[" in aokucode:
							onlyusers = aokucode.split("$onlyForIDs[")[1].split("]")[0]
							if str(message.author.id) in onlyusers.split(";")[:-1]:
								codestatus["onlyForIDs"] = False
								aokucode = aokucode.replace(f"$onlyForIDs[{onlyusers}]", f"")
							else:
								await channel.send(onlyusers.split(";")[-1])
								codestatus["onlyForIDs"] = True
								aokucode = aokucode.replace(f"$onlyForIDs[{onlyusers}]", f"")
							break

						while "$onlyAdmin[" in aokucode:
							onlyadmins = aokucode.split(f"$onlyAdmin[")[1].split("]")[0]
							if message.author.guild_permissions.administrator:
								codestatus["onlyAdmin"] = False
								aokucode = aokucode.replace(f"$onlyAdmin[{onlyadmins}]", f"")
							elif not message.author.guild_permissions.administrator:
								codestatus["onlyAdmin"] = True
								await channel.send(onlyadmins)
								aokucode = aokucode.replace(f"$onlyAdmin[{onlyadmins}]", f"")
							break

						while "$onlyForServers[" in aokucode:
							onlyservers = aokucode.split("$onlyForServers[")[1].split("]")[0]
							if str(message.guild.id) in onlyservers.split(";")[:-1]:
								codestatus["onlyForServers"] = False
								aokucode = aokucode.replace(f"$onlyForServers[{onlyservers}]", f"")
							else:
								await channel.send(onlyservers.split(";")[-1])
								codestatus["onlyForServers"] = True
								aokucode = aokucode.replace(f"$onlyForServers[{onlyservers}]", f"")
							break


						while "$jsonRequest[" in aokucode:
							request = aokucode.split("$jsonRequest[")[1].split("]")[0].split(";")
							try:
								aokucode = aokucode.replace(f"$jsonRequest[{request[0]};{request[1]};{request[2]}]", f"{json.dumps(requests.get(request[0]).json()[request[1]], indent = 2, ensure_ascii = False)}")
							except KeyError as e:
								aokucode = aokucode.replace(f"$jsonRequest[{request[0]};{request[1]};{request[2]}]", f"{request[2]}")
								logger.error(f"$jsonRequest: {request[2]}")
								break

						def insert_returns(body):
							if isinstance(body[-1], ast.Expr):
								body[-1] = ast.Return(body[-1].value)
								ast.fix_missing_locations(body[-1])
								if isinstance(body[-1], ast.If):
									insert_returns(body[-1].body)
									insert_returns(body[-1].orelse)
									if isinstance(body[-1], ast.With):
										insert_returns(body[-1].body)

						while "$ping" in aokucode: #--------------ПРОВЕРЕНО--------------
							aokucode = aokucode.replace("$ping", f"{round(self.client.latency*1000)}")
							break

						while "$uptime" in aokucode: #--------------ПРОВЕРЕНО--------------
							aokucode = aokucode.replace("$uptime", f"<t:{(int(time.time()))}:R>")
							break

						while "$channelID" in aokucode: #--------------ПРОВЕРЕНО--------------
							aokucode = aokucode.replace("$channelID", str(message.channel.id))
							break

						while "$clientID" in aokucode:
							aokucode = aokucode.replace("$clientID", str(self.client.user.id))
							break

						while "$userBanner[" in aokucode:
							try:
								bannerid = aokucode.split("$userBanner[")[1].split("]")[0]
								bannerurl = requests.get(f"https://cryptons.ga/api/v1/userbanner?id={bannerid}").json()['url']
								aokucode = aokucode.replace(f"$userBanner[{bannerid}]", bannerurl)
							except:
								aokucode = aokucode.replace(f"$userBanner[{bannerid}]", "```userBanner: It user hasn't profile banner yet```")
								break

						while "$funcUsage[" in aokucode:
							usplit = aokucode.split("$funcUsage[")[1].split("]")[0]
							ures = requests.get(f"https://aokuapi.herokuapp.com/api/func/{usplit}").json()['usage']
							aokucode = aokucode.replace(f"$funcUsage[{usplit}]", ures)
							break

						while "$funcDescription[" in aokucode:
							dsplit = aokucode.split("$funcDescription[")[1].split("]")[0]
							dres = requests.get(f"https://aokuapi.herokuapp.com/api/func/{dsplit}").json()['description']
							aokucode = aokucode.replace(f"$funcDescription[{dsplit}]", str("{0}".format(dres)))
							break


						while "$dpyEval[" in aokucode:
							dpycode = aokucode.split("$dpyEval[")[1].split("]")[0]
							ctx = await self.client.get_context(message)
							try:
								fn_name = "_eval_expr"
								cmd = dpycode.strip("` ")
								cmd = "\n".join(f" {i}" for i in cmd.splitlines())
								body = f"async def {fn_name}():\n{cmd}"
								parsed = ast.parse(body)
								body = parsed.body[0].body
								insert_returns(body)
								env = {
									"bot":self.client,
									'discord': discord,
									'commands': commands,
									'ctx': ctx,
									'__import__': __import__
								}
								exec(compile(parsed, filename="<ast>", mode="exec"), env)
								result = (await eval(f"{fn_name}()", env))
								aokucode = aokucode.replace(f"$dpyEval[{dpycode}]", "")
							except Exception as e:
								aokucode = aokucode.replace(f"$dpyEval[{dpycode}]", e)
								break

						while "$authorAvatar" in aokucode:
							aokucode = aokucode.replace("$authorAvatar",f"{message.author.avatar_url}")
							break

						while "$botOwnerID" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$botOwnerID", str(botinfo.owner.id))
							break


						while "$userAvatar[" in aokucode: # -----------ПРОВЕРЕНО------------------
							avatarkaa = aokucode.split("$userAvatar[")[1].split("]")[0]
							user = await self.client.fetch_user(avatarkaa)
							aokucode = aokucode.replace(f"$userAvatar[{avatarkaa}]"), str(user.avatar_url)
							break

						while "$botGuilds" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$botGuilds", f"{len(self.client.guilds)}")
							break

						while "$findUserName[" in aokucode: # -----------ПРОВЕРЕНО------------------
							try:
								finduserid = aokucode.split("$findUserName[")[1].split("]")[0]
								kvas = await self.client.fetch_user(finduserid)
								aokucode = aokucode.replace(f"$findUserName[{finduserid}]", f"{kvas.name}#{kvas.discriminator}")
							except Exception as e:
								aokucode = aokucode.replace(f"$findUserName[{finduserid}]", f"```findUserName: Incorrect UserID in $findUserName[{finduserid}]```")
								logger.error(f"$findUserName: Incorrect UserID in $findUserName[{finduserid}]")
								break

						while "$findUserID[" in aokucode: # -----------ПРОВЕРЕНО------------------
							try:
								finduserid = aokucode.split("$findUserID[")[1].split("]")[0]
								strelkarak = discord.utils.get(message.guild.members, name=finduserid)
								aokucode = aokucode.replace(f"$findUserID[{finduserid}]", f"{strelkarak.id}")
							except Exception as e:
								aokucode = aokucode.replace(f"$findUserID[{finduserid}]", f"findUserID: Incorrect UserID in $findUser[{finduserid}]")
								logger.error(f"findUserID: Incorrect UserID in $findUserШВ[{finduserid}]")
								break

						while "$guildID" in aokucode:
							try:
								guildname = aokucode.split("$guildID[")[1].split("]")[0]
								ayeguild = discord.utils.get(self.client.guilds, name = guildname)
								aokucode = aokucode.replace(f"$guildID[{guildname}]", f"{ayeguild.id}")
							except Exception as e:
								aokucode = aokucode.replace(f"$guildID[{guildname}]", f"```Error while running this function\n{e}```")
								logger.error(f"$guildID: {e}")
								break

						while "$setBotStatus[" in aokucode:
							botstat = aokucode.split("$setBotStatus[")[1].split("]")[0].split(";")
							if "online" in botstat[0]:
								await self.client.change_presence(status = discord.Status.online, activity = discord.Activity(name=f'{botstat[1]}', type = discord.ActivityType.watching))
								aokucode = aokucode.replace(f"$setBotStatus[{botstat[0]};{botstat[1]}]", f"")
							if "dnd" in botstat[0]:
								await self.client.change_presence(status = discord.Status.dnd, activity = discord.Activity(name=f'{botstat[1]}', type = discord.ActivityType.watching))
								aokucode = aokucode.replace(f"$setBotStatus[{botstat[0]};{botstat[1]}]", f"")
							if "idle" in botstat[0]:
								await self.client.change_presence(status = discord.Status.idle, activity = discord.Activity(name=f'{botstat[1]}', type = discord.ActivityType.watching))
								aokucode = aokucode.replace(f"$setBotStatus[{botstat[0]};{botstat[1]}]", f"")
							else:
								aokucode = aokucode.replace(f"$setBotStatus[{botstat[0]};{botstat[1]}]", "```setBotStatus: Invalid usage```")
								break

						while "$charCount[" in aokucode: # -----------ПРОВЕРЕНО------------------
							text = aokucode.split("$charCount[")[1].split("]")[0]
							aokucode = aokucode.replace(f"$charCount[{text}]", str(len(text)))
							break

						while "$reverseText[" in aokucode: # -----------ПРОВЕРЕНО------------------
							exe = aokucode.split("$reverseText[")[1].split("]")[0]
							result = exe[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
							aokucode = aokucode.replace(f"$reverseText[{exe}]", result)
							break

						while "$guildOwner" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$guildOwner", str(message.guild.owner))
							break

						while "$guildOwnerID" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$guildOwnerID", str(message.guild.owner.id))
							break

						while "$randomUserID" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$randomUserID", str(random.choice(message.guild.members).id))
							break

						while "$randomUserMention" in aokucode: # -----------ПРОВЕРЕНО------------------
							ae = random.choice(message.guild.members).mention
							aokucode = aokucode.replace("$randomUserMention", ae)
							break

						while "$randomUserName" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$randomUserName", str(random.choice(message.guild.members).name))
							break

						while "$randomChannelID" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$randomChannelID", str(random.choice(message.guild.channels).id))
							break

						while "$randomChannelMention" in aokucode: # -----------ПРОВЕРЕНО------------------
							ae = random.choice(message.guild.channels).mention
							aokucode = aokucode.replace("$randomChannelMention", ae)
							break

						while "$randomChannelName" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$randomChannelName", str(random.choice(message.guild.channels).name))
							break

						while "$randomRoleID" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$randomRoleID", str(random.choice(message.guild.roles).id))
							break

						while "$randomRoleMention" in aokucode: # -----------ПРОВЕРЕНО------------------
							ae = random.choice(message.guild.roles).mention
							aokucode = aokucode.replace("$randomRoleMention", ae)
							break

						while "$randomRoleName" in aokucode: # -----------ПРОВЕРЕНО------------------
							aokucode = aokucode.replace("$randomRoleName", str(random.choice(message.guild.roles).name))
							break


						while "$botCount" in aokucode: # -----------ПРОВЕРЕНО------------------
							aller = []
							for m in message.guild.members:
								if m.bot:
									aller.append(m.bot)
							aokucode = aokucode.replace("$botCount", str(len(aller)))
							break

						while "$round[" in aokucode: #--------------ПРОВЕРЕНО--------------
							try:
								plavayu = float(aokucode.split("$round[")[1].split("]")[0])
								aokucode = aokucode.replace(f"$round[{plavayu}]", str(round(plavayu)))
							except:
								aokucode = aokucode.replace(f"$round[{plavayu}]", f"```round: Only float numbers```")
								logger.error("$round: Only float numbers")
								break

						while "$toLowerCase[" in aokucode: #--------------ПРОВЕРЕНО--------------
							lowertext = aokucode.split("$toLowerCase[")[1].split("]")[0]
							aokucode = aokucode.replace(f"$toLowerCase[{lowertext}]", str(lowertext.lower()))
							break

						while "$toUpperCase[" in aokucode: #--------------ПРОВЕРЕНО--------------
							uppertext = aokucode.split("$toUpperCase[")[1].split("]")[0]
							aokucode = aokucode.replace(f"$toUpperCase[{uppertext}]", str(uppertext.upper()))
							break

						while "$channelCount" in aokucode: #----------ПРОВЕРЕНО-----------
							spis = []
							for c in message.guild.text_channels:
								spis.append(c)
							print(spis)
							aokucode = aokucode.replace("$channelCount", str(len(spis)))
							break

						while "$roleCount" in aokucode:
							wes = []
							for r in message.guild.roles:
								wes.append(r)
							del wes[0]
							await message.channel.send(f"{len(wes)}")
							aokucode = aokucode.replace("$roleCount", f"")
							break

						while "$channelTopic[" in aokucode: # -----------ПРОВЕРЕНО------------------
							try:
								chanId = aokucode.split("$channelTopic[")[1].split("]")[0]
								if "$channelID" in chanId:
									aokucode = aokucode.replace(f"$channelTopic[$channelID]", str(message.channel.topic))
								else:
									c = await self.client.fetch_channel(int(chanId))
									aokucode = aokucode.replace(f"$channelTopic[{chanId}]", str(c.topic))
							except:
								aokucode = aokucode.replace(f"$channelTopic[{chanId}]", f"```channelTopic: Incorrect Channel ID in $channelTopic[{chanId}]```")
								logger.error(f"$channelTopic: Incorrect Channel ID in $channelTopic[{chanId}]")
								break

						while "$setChannelCooldown" in aokucode:
							try:
								chan = aokucode.split("$setChannelCooldown[")[1].split("]")[0].split(";")
								reschan = await self.client.fetch_channel(chan[0])
								await reschan.edit(slowmode_delay = chan[1])
								aokucode = aokucode.replace(f"$setChannelCooldown[{chan[0]};{chan[1]}]", str(""))
							except Exception as e:
								aokucode = aokucode.replace(f"$setChannelCooldown[{chan[0]};{chan[1]}]", str("```setChannelCooldown: Failed to change cooldown```"))
								logger.error("$setChannelCooldown: Failed to change cooldown")
								break

						while "$guildBanner" in aokucode:
							try:
								aokucode = aokucode.replace("$guildBanner", str(message.guild.banner_url))
							finally:
								aokucode = aokucode.replace("$guildBanner", str("```guildBanner: Failed to get banner```"))
								logger.error("$guildBanner: Failed to get banner")
								break

						while "$highestRoleName[" in aokucode:
							try:
								usersea = aokucode.split("$highestRoleName[")[1].split("]")[0]
								userkvas = discord.utils.get(message.guild.members, id = int(usersea))
								if "$authorID" in usersea:
									aokucode = aokucode.replace(f"$highestRoleName[$authorID]", f"{message.author.roles[-1].name}")
								else:
									aokucode = aokucode.replace(f"$highestRoleName[{usersea}]", f"{userkvas.roles[-1].name}")
							except Exception as e:
								aokucode = aokucode.replace(f"$highestRoleName[{usersea}]", str("The user hasn't roles yet"))
								logger.error(f"$highestRoleName: The user hasn't roles yet")
								break

						while "$highestRoleID[" in aokucode:
							try:
								usersea = aokucode.split("$highestRoleID[")[1].split("]")[0]
								userkvas = discord.utils.get(message.guild.members, id = int(usersea))
								if "$authorID" in usersea:
									aokucode = aokucode.replace(f"$highestRoleID[{usersea}]", f"{message.author.roles[-1].id}")
								else:
									aokucode = aokucode.replace(f"$highestRoleID[{usersea}]", f"{userkvas.roles[-1].id}")
							except Exception as e:
								aokucode = aokucode.replace(f"$highestRoleID[{usersea}]", str(""))
								break

						while "$allMembersCount" in aokucode:
							aokucode = aokucode.replace("$allMembersCount", str(len(message.guild.members)))
							break

						while "$addReactions[" in aokucode: #-----------ПРОВЕРЕНО---------------
							try:
								zer = aokucode.split("$addReactions[")
								zer = zer[1].split("]")
								zer = zer[0].split(";")

								for zer in zer:
									await message.add_reaction(zer)
									aokucode = aokucode.replace(f"$addReactions[{zer}]", str(""))

							except Exception as e:
								aokucode = aokucode.replace(f"$addReactions[{zer}]", str(e))
								break

						if "$exec[" in aokucode: #-----------ПРОВЕРЕНО---------------
							try:
								text = aokucode.split("$exec[")[1].split("]")[0]
								resultt = subprocess.check_output(f"{text}", shell=True).decode('utf-8')
								aokucode = aokucode.replace(f"$exec[{text}]", str(f"{resultt}"))
							except Exception as e:
								aokucode = aokucode.replace(f"$exec[{text}]", f"```{e}```")

						while "$aokuVersion" in aokucode: #-----------ПРОВЕРЕНО---------------
							aokucode = aokucode.replace("$aokuVersion", "2.0.0")
							break

						while "$isBot[" in aokucode: #-----------ПРОВЕРЕНО---------------
							try:
								iduser = int(aokucode.split('$isBot[')[1].split("]")[0])
								akkuser = await self.client.fetch_user(iduser)
								if akkuser.bot:
									aokucode = aokucode.replace(f"$isBot[{iduser}]", f"True")
								else:
									aokucode = aokucode.replace(f"$isBot[{iduser}]", f"True")
							except Exception as e:
								await channel.send("```isBot: Invalid id```")
								print(e)
								break

						while "$randomNumber[" in aokucode: #-----------ПРОВЕРЕНО---------------
							randnumber = aokucode.split("$randomNumber[")[1].split("]")[0].split(";")
							try:
								resrandnumber = random.randint(int(randnumber[0]),int(randnumber[1]))
								aokucode = aokucode.replace(f"$randomNumber[{int(randnumber[0])};{int(randnumber[1])}]","{0}".format(resrandnumber))
							except:
								aokucode = aokucode.replace(f"$randomNumber[{int(randnumber[0])};{int(randnumber[1])}]", f"```randomNumber: Error in $random[{int(randnumber[0])};{int(randnumber[1])}]```")
								logger.error(f"```$randomNumber: Error in $randomNumber[{int(randnumber[0])};{int(randnumber[1])}]```")
								break

						while "$randomText[" in aokucode: #-----------ПРОВЕРЕНО---------------
							randtext = aokucode.split("$randomText[")[1].split("]")[0]
							try:
								rand = random.choice(randtext.split(";"))
								aokucode = aokucode.replace(f"$randomText[{randtext}]", str(rand))
							except:
								aokucode = aokucode.replace(f"$randomText[{randtext}]", f"```randomText: Error in $randomText[{randtext}]```")
								logger.error(f"$randomText: Error in $randomText[{randtext}]")
							break

						while "$fetchMessage[" in aokucode: #-----------ПРОВЕРЕНО---------------
							try:
								chanid = aokucode.split("$fetchMessage[")[1].split("]")[0].split(";")
								resi = await self.client.get_channel(int(chanid[0])).fetch_message(int(chanid[1]))
								aokucode = aokucode.replace(f"$fetchMessage[{chanid};{msgid}]", str(resi.content))
							except IndexError:
								aokucode = aokucode.replace(f"$fetchMessage[{chanid};{msgid}]", str("```fetchMessage: Incorrect parameters```"))
								logger.error("$fetchMessage: Incorrect parameters")
								break

						while "$deletecommand" in aokucode: #-----------ПРОВЕРЕНО---------------
							aokucode = aokucode.replace(f"$deletecommand", f"")
							try:
								await message.delete()
							except Exception as e:
								aokucode = aokucode.replace(f"$deletecommand", f"```deletecommand: Failed to delete command```")
								logger.error("$deletecommand: Failed to delete command")
								break

						while "$time[" in aokucode: #-----------ПРОВЕРЕНО---------------
							try:
								taim = aokucode.split("$time[")[1].split("]")[0]
								alltime = (datetime.utcnow() + timedelta(hours=3)).strftime(taim)
								aokucode = aokucode.replace(f"$time[{taim}]", alltime)
							except:
								aokucode = aokucode.replace(f"$time[{taim}]", f"```time: Error in $time[{taim}]```")
								logger.error(f"$time: Error in $time[{taim}]")
								break

						while "$math[" in aokucode: #-----------ПРОВЕРЕНО---------------
							try:
								primer = aokucode.split("$math[")[1].split("]")[0]
								aokucode = aokucode.replace(f"$math[{primer}]", str(eval(primer)))
							except Exception as e:
								aokucode = aokucode.replace(f"$math[{primer}]", f"```math: Error in $math[{primer}]```")
								logger.error(f"$math: Error in $math[{primer}]")
								break


						while "$createVar[" in aokucode: #----------ПРОВЕРЕНО-----------
							disboto = aokucode.split("$createVar[")[1].split("]")[0].split(";")
							with open("variables.json", "r+", encoding = "utf-8") as f:
								try:
									data = json.load(f)
								except:
									data = {}

								if disboto[0] in data:
									aokucode = aokucode.replace(f"$createVar[{disboto[0]};{disboto[1]}]", f"```createVar: Variable '{disboto[0]}' already exist```")
									logger.error(f"$createVar: Variable '{disboto[0]}' already exist")
								else:
									data[disboto[0]] = disboto[1]

									with open("variables.json", "w+", encoding="utf-8") as f:
										json.dump(data, f, sort_keys=True, ensure_ascii=False, indent = 2)
										aokucode = aokucode.replace(f"$createVar[{disboto[0]};{disboto[1]}]", str(""))
										break

						while "$getVar[" in aokucode:
							try:
								varname = aokucode.split("$getVar[")[1].split("]")[0]
								with open("variables.json", "r+", encoding = "utf-8") as f:
									varsname = json.loads(f.read())
									aokucode = aokucode.replace(f"$getVar[{varname}]", str(varsname[varname]))
							except:
								aokucode = aokucode.replace(f"$getVar[{varname}]", f"```updateVar: Variable '{varname}' is not exist```")
								logger.error(f"$updateVar: Variable '{varname}' is not exist")
								break

						while "$updateVar[" in aokucode: #----------ПРОВЕРЕНО-----------
							try:
								varname = aokucode.split("$updateVar[")[1].split("]")[0].split(";")

								with open("variables.json", "r+", encoding = "utf-8") as f:
									f_json = json.load(f)
									if varname[0] in f_json:
										f_json[varname[0]] += varname[1]

										with open("variables.json", "r+", encoding = "utf-8") as f:
											json.dump(f_json, f, sort_keys=True, ensure_ascii=False, indent=2)
											aokucode = aokucode.split(f"$updateVar[{varname[0]};{varname[1]}]", str(""))
									else:
										aokucode = aokucode.split(f"$updateVar[{varname[0]};{varname[1]}]", f"```updateVar: Variable '{varname[0]}' is not exist```")
							except TypeError:
								logger.error(f"$updateVar: Variable '{varname[0]}' is not exist")

						while "$openVars" in aokucode:
							try:
								with open("variables.json", "r+", encoding = "utf-8") as f:
									aokucode = aokucode.replace("$openVars", f"```py\n{f.read()}```")
							except:
								aokucode = aokucode.replace("$openVars", "openVars: error")
								logger.error("$openVars: fileError")

						while "$isAdmin" in aokucode:
							aokucode = aokucode.replace("$isAdmin", f"{message.author.guild_permissions.administrator}")
							break

						while "$serverNames" in aokucode:
							text = ""
							for guild in self.client.guilds:
								text += str(guild.name) + "\n"
							aokucode = aokucode.replace("$serverNames", text)
							break

						while "$giveRole[" in aokucode:
							userandrole = aokucode.split("$giveRole[")[1].split("]")[0].split(";")
							resmember = discord.utils.get(message.guild.members, id=int(userandrole[0]))
							resrole = discord.utils.get(message.guild.roles, id = int(userandrole[1]))
							try:
								await resmember.add_roles(resrole)
								aokucode = aokucode.replace(f"$giveRole[{userandrole[0]};{userandrole[1]}]", f"")
							except Exception as e:
								aokucode = aokucode.replace(f"$giveRole[{userandrole[0]};{userandrole[1]}]", "```giveRole: Failed to add role```")
								logger.error("$giveRole: Failed to give role")
								break

						while "$takeRole[" in aokucode:
							userandrole = aokucode.split("$takeRole[")[1].split("]")[0].split(";")
							resmember = discord.utils.get(message.guild.members, id=int(userandrole[0]))
							resrole = discord.utils.get(message.guild.roles, id = int(userandrole[1]))
							try:
								await resmember.remove_roles(resrole)
								aokucode = aokucode.replace(f"$takeRole[{userandrole[0]};{userandrole[1]}]", f"")
							except Exception as e:
								aokucode = aokucode.replace(f"$takeRole[{userandrole[0]};{userandrole[1]}]", "```takeRole: Failed to remove role```")
								logger.error("$takeRole: Failed to remove role")
								break


						if "$joinVC" in aokucode:
							try:
								channelvcc = message.author.voice.channel
								self.channelvcc = channelvcc
								voice_client = get(self.client.voice_clients, guild = message.guild)

								if voice_client and voice_client.is_connected():
									await voice_client.move_to(channelvcc)
									aokucode = aokucode.replace("$joinVC", str(""))
								else:
									voice_client = await channelvcc.connect()
									aokucode = aokucode.replace("$joinVC", str(""))
							except Exception as e:
								aokucode = aokucode.replace("$joinVC", "You must connect to any voice channels")
								logger.error(f"$joinVC: {e}")


						if "$playSong[" in aokucode: #----------ПРОВЕРЕНО-----------
							url = aokucode.split("$playSong[")[1].split("]")[0]
							if not url.startswith("https://www.youtube.com/"):
								req = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1&order=relevance&q={}&relevanceLanguage=en&safeSearch=moderate&type=video&videoDimension=2d&fields=items%2Fid%2FvideoId&key='.format(url) + "AIzaSyC_viihkRiUg3N5bv0DRvOrmaNdUNJ852U")
								aokucode = aokucode.replace(f"$playSong[{url}]", str(""))
								url = url.replace(url, "https://www.youtube.com/watch?v={}".format(req.json()['items'][0]['id']['videoId']))
							else:
								url = url
								aokucode = aokucode.replace(f"$playSong[{url}]", str(""))


							ydl_opts = {
								'format': 'bestaudio/best',
								'noplaylist': False,
								'postprocessors': [{
									'key': 'FFmpegExtractAudio',
									'preferredcodec': 'mp3',
									'preferredquality': '192'
								}],
							}

							ffmpeg_opts = {
								'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
								'options': '-vn'
							}
							
							try:
								voice_client = get(self.client.voice_clients, guild = message.guild)
								with youtube_dl.YoutubeDL(ydl_opts) as ydl:
									file = ydl.extract_info(url, download=False)
									self.musicFile = file
									# кончил от лица пики
									path = file['formats'][0]['url']
									voice_client.play(discord.FFmpegPCMAudio(source = path, **ffmpeg_opts))
									voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
							except Exception as e:
								aokucode = aokucode.replace(f"$playSong[{url}]", "You may not be connected to a voice channel")
								logger.error(f"$playSong: {e}")

						while "$songTitle" in aokucode:
							try:
								aokucode = aokucode.replace("$songTitle", f"{self.musicFile['title']}")
							except AttributeError:
								aokucode = aokucode.replace("$songTitle", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songPicture" in aokucode:
							try:
								aokucode = aokucode.replace("$songPicture", f"https://i.ytimg.com/vi/{self.musicFile['id']}/maxresdefault.jpg")
							except AttributeError:
								aokucode = aokucode.replace("$songPicture", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songAuthor" in aokucode:
							try:
								aokucode = aokucode.replace("$songAuthor", f"{self.musicFile['uploader']}")
							except AttributeError:
								aokucode = aokucode.replace("$songAuthor", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songDuration" in aokucode:
							try:
								minutes, seconds = divmod(int(self.musicFile['duration']), 60)
								dura = f"{minutes}:{seconds}"
								aokucode = aokucode.replace("$songDuration", f"{dura}")
							except AttributeError:
								aokucode = aokucode.replace("$songDuration", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songViews" in aokucode:
							try:
								aokucode = aokucode.replace("$songViews", f"{self.musicFile['view_count']:,}")
							except AttributeError:
								aokucode = aokucode.replace("$songViews", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songURL" in aokucode:
							try:
								aokucode = aokucode.replace("$songURL", f"{self.musicFile['webpage_url']}")
							except AttributeError:
								aokucode = aokucode.replace("$songURL", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songIsLive" in aokucode:
							try:
								aokucode = aokucode.replace("$songIsLive", f"{self.musicFile['is_live']}")
							except AttributeError:
								aokucode = aokucode.replace("$songIsLive", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songLikes" in aokucode:
							try:
								aokucode = aokucode.replace("$songLikes", f"{self.musicFile['like_count']:,}")
							except AttributeError:
								aokucode = aokucode.replace("$songLikes", f"```aokuMusicError: Song is not playing now```")
							break

						while "$songDislikes" in aokucode:
							try:
								aokucode = aokucode.replace("$songDislikes", f"{self.musicFile['dislike_count']:,}")
							except AttributeError:
								aokucode = aokucode.replace("$songDislikes", f"```aokuMusicError: Song is not playing now```")
							break

						if "$leaveVC" in aokucode: #----------ПРОВЕРЕНО-----------
							try:
								voice_client = get(self.client.voice_clients, guild = message.guild)
								if voice_client and voice_client.is_connected():
									await voice_client.disconnect()
									aokucode = aokucode.replace("$leaveVC", str(""))
								else:
									abewe = await voice_client.leave()
									aokucode = aokucode.replace("$leaveVC", str(""))
							except Exception as e:
								aokucode = aokucode.replace("$leaveVC", str(f"```leaveVC: Error while running this command\n\n{str(e)}```"))
								logger.error(f"$leaveVC: {e}")

						if "$dm[" in aokucode: #----------ПРОВЕРЕНО-----------
							try:
								qwer = aokucode.split("$dm[")[1].split("]")[0].split(";")[0]
								usercontent = aokucode.split("$dm[")[1].split("]")[0].split(";")[1]
								ss = await self.client.fetch_user(int(qwer))
								await ss.send(usercontent)
								aokucode = aokucode.replace(f"$dm[{int(qwer)};{usercontent}]", str(""))
							except Exception as e:
								aokucode = aokucode.replace(f"$dm[{int(qwer)};{usercontent}]", str("```dm: Failed to dm user```"))
								logger.error(f"$dm: {e}")

						if "$repeatMessage[" in aokucode:
							howmuchrepeat = aokucode.split("$repeatMessage[")[1].split("]")[0].split(";")
							for x in range(int(howmuchrepeat[0])):
								await channel.send(f"{howmuchrepeat[1]}")
							aokucode = aokucode.replace(f"$repeatMessage[{int(howmuchrepeat)[0]};{howmuchrepeat[1]}]", str(""))

						if "$createButton[" in aokucode: #----------ПРОВЕРЕНО-----------
							def check(m):
								return m.author == m.message.author and m.channel == m.channel

							buttmsg = aokucode.split("$createButton[")[1].split("]")[0].split(";")

							if buttmsg[1] == "random":
								randcolor = [ButtonStyle.blue, ButtonStyle.green, ButtonStyle.red]

								endcolor = random.choice(randcolor)
								knopki = await channel.send(
									buttmsg[0],
									components = [
										Button(style = endcolor, label = buttmsg[2], id = "em1")]
								)


							res = await self.client.wait_for(
								"button-click",
								check=check,
								timeout = 300
							)

							aokucode = aokucode.replace(f"$createButton[{buttmsg};{buttcolor};{buttlabel}]", str(knopki))

						if "$createSelectMenu[" in aokucode: #----------ПРОВЕРЕНО-----------
							try:
								menus = aokucode.split("$createSelectMenu[")[1].split("]")[0].split(";")
								select_menu = await channel.send(
									menus[0],
									components = [
										Select(
											placeholder = menus[1],
											options = [
												SelectOption(emoji = menus[2], label = menus[3], description = menus[4], value = "e1")
											]
										)
									]
								)
								res = await self.client.wait_for("select_option")
								await res.respond(content = f"Вы выбрали: {res.component.emoji}")
								aokucode = aokucode.replace(f"$createSelectMenu[{menus[0]};{menus[1]};{menus[2]};{menus[3]};{menus[4]}]", str(select_menu))
							except IndexError as e:
								aokucode = aokucode.replace(f"$createSelectMenu[{menus[0]};{menus[1]};{menus[2]};{menus[3]};{menus[4]}])", "```createSelectMenu: Incorrect parameters```")
								logger.error("$createSelectMenu: Incorrect parameters")

						if "$setTitle[" in aokucode:
							title = aokucode.split("$setTitle[")[1].split("]")[0]
							embed.title = title
							aokucode = aokucode.replace(f"$setTitle[{title}]", str(""))
						
						if "$setDescription[" in aokucode:
							descr = aokucode.split("$setDescription[")[1].split("]")[0]
							embed.description = descr
							aokucode = aokucode.replace(f"$setDescription[{descr}]", str(""))

						if "$setColor[" in aokucode:
							colar = aokucode.split("$setColor[")[1].split("]")[0]
							if colar == "random":
								embed.color = discord.Color.random()
								aokucode = aokucode.replace(f"$setColor[random]", str(""))
							else:
								embed.color = eval(f"0x{str(colar)}")
								aokucode = aokucode.replace(f"$setColor[{colar}]", str(""))


						if "$setFooter[" in aokucode:
							try:
								fo = aokucode.split("$setFooter[")[1].split("]")[0].split(";")
								if "$authorAvatar" in fo[1]:
									aokucode = aokucode.replace(f"$setFooter[{fo[0]};$authorAvatar]", str(""))
									embed.set_footer(text = fo[0], icon_url = message.author.avatar_url)
								elif "$botAvatar" in fo[1]:
									aokucode = aokucode.replace(f"$setFooter[{fo[0]};$botAvatar]", str(""))
									embed.set_footer(text=fo[0], icon_url = self.client.user.avatar_url)
								else:
									aokucode = aokucode.replace(f"$setFooter[{fo[0]};{fo[1]}]", str(""))
									embed.set_footer(text = fo[0], icon_url = fo[1])
							except Exception as e:
								foer = aokucode.split("$setFooter[")[1].split("]")[0]
								aokucode = aokucode.replace(f"$setFooter[{foer}]", str(""))
								embed.set_footer(text = foer)
								logger.error(f"$setFooter: {e}")


						if "$setThumbnail[" in aokucode:
							yser = aokucode.split("$setThumbnail[")[1].split("]")[0]
							if "$authorAvatar" in yser:
								aokucode = aokucode.replace(f"$setThumbnail[{yser}]", str(""))
								embed.set_thumbnail(url = message.author.avatar_url)
							elif "$botAvatar" in yser:
								aokucode = aokucode.replace(f"$setThumbnail[{yser}]", str(""))
								embed.set_thumbnail(url = self.client.user.avatar_url)
							else:
								aokucode = aokucode.replace(f"$setThumbnail[{yser}]", str(""))
								embed.set_thumbnail(url = yser)


						if "$setAuthor[" in aokucode:
							try:
								kote = aokucode.split("$setAuthor[")[1].split("]")[0].split(";")
								if "$authorAvatar" in kote[1]:
									aokucode = aokucode.replace(f"$setAuthor[{kote[0]};$authorAvatar]", str(""))
									embed.set_author(name=kote[0], icon_url = message.author.avatar_url)
								elif "$botAvatar" in kote[1]:
									aokucode = aokucode.replace(f"$setAuthor[{kote[0]};$botAvatar]", str(""))
									embed.set_author(name = kote[0], icon_url = self.client.user.avatar_url)
								else:
									aokucode = aokucode.replace(f"$setAuthor[{kote[0]};{kote[1]}]", str(""))
									embed.set_author(name = kote[0], icon_url = kote[1])
							except:
								kote = aokucode.split("$setAuthor[")[1].split("]")[0]
								aokucode = aokucode.replace(f"$setAuthor[{kote}]", str(""))
								embed.set_author(name = kote)


						if "$addField[" in aokucode:
							try:
								aine = aokucode.split("$addField[")[1].split("]")[0].split(";")
								aokucode = aokucode.replace(f"$addField[{aine[0]};{aine[1]}]", str(""))
								embed.add_field(name = aine[0], value = aine[1])
							except IndexError:
								aokucode = aokucode.replace(f"$addField[{aine[0]};{aine[1]}]", "```addField: Incorrect parameters```")
								logger.error("$addField: Incorrect Parameters")

						if "$setImage[" in aokucode:
							tea = aokucode.split("$setImage[")[1].split("]")[0]
							if "$authorAvatar" in tea:
								aokucode = aokucode.replace("$setImage[$authorAvatar]", str(""))
								embed.set_image(url = message.author.avatar_url)
							elif "$botAvatar" in tea:
								aokucode = aokucode.replace("$setImage[$botAvatar]", str(""))
								embed.set_image(url = self.client.user.avatar_url)
							else:
								aokucode = aokucode.replace(f"$setImage[{tea}]", str(""))
								embed.set_image(url = tea)

						if "$botLeave[" in aokucode: #----------ПРОВЕРЕНО-----------
							try:
								servid = aokucode.split("$botLeave[")[1].split("]")[0]
								server = await self.client.fetch_guild(int(servid))
								aokucode = aokucode.replace(f"$botLeave[{servid}]", str(""))
								await server.leave()
							except:
								aokucode = aokucode.replace("$botLeave", "botLeave: Failed to leave the server")
								raise aokuCodeError("In function $botLeave raised an error")

						if "$botLeave" in aokucode:
							aokucode = aokucode.replace("$botLeave", f"")
							await message.guild.leave()

						if codestatus['onlyForIDs'] == True:
							break

						if codestatus["onlyAdmin"] == True:
							break

						if codestatus['onlyForServers'] == True:
							break

						try:
							await message.channel.send(aokucode, embed=embed)
						except Exception as e:
							try:
								await message.channel.send(aokucode)
							except Exception as e:
								pass

	def start(self, token, selfbot: bool = None):
		try:
			if selfbot == False:
				self.client.run(token)
			elif selfbot == True:
				self.client.run(token, bot = False)
		except Exception as e:
			print("Ошибка подключения к Discord!\n\n{0}".format(str(e)))