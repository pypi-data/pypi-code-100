from discord.ext import commands

def register_commands(bot, *, ignore: list = []):
	lst = ['chess','hangman','madlib','ttt']
	for cog in lst:
		if cog not in ignore:
			bot.load_extension(cog)
