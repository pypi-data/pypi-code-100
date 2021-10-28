import discord
from discord.ext import commands
import aiohttp

class MadLib:
    @commands.command()
    async def madlib(self, ctx, minimum='5', maximum='25'):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'http://madlibz.herokuapp.com/api/random?minlength={minimum}&maxlength={maximum}') as r:
                h = await r.json()
                lst = []
                for question in h['blanks']:
                    await ctx.send(f"Please send: {question}")
                    answer = await ctx.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    lst.append(answer.content)
                madlib = h['value']
                string = ''
                for i in range(len(madlib)-1):
                    smth += f'{madlib[i]}{lst[i] if len(lst)-1 >= i else ""}'
                await ctx.send(string)
