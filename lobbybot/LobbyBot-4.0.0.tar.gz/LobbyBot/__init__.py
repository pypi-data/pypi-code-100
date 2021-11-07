"""
Hello Skids,
Today is Your Lucky Day!

I will Let You Take Whatever You want from This Code.
If You Want To Know How i Made Any of The Functions
Or How You Can implement Them Into Your Script
Just Join The Discord and Message anyone with The Highest Role!
https://discord.gg/VHtvszBAx3

P.S I dont Recommend You Skidding!
Its a bad crime and can get you into serious trouble.
You Should Only Skid My Projects Since I allow People Todo So!

People Spend Hours Coding These Scripts Just For You!
Not To Steal The Code But For You To Use The Service.
Some People Like Oli (Another Lobbybot Owner https://partybot.net)
had to put a really alarming message for the skids because he wanted
his work to be private!
I aspire to be like Gomashio(https://github.com/gomashio1596) or pdf(https://github.com/pdf114514)
where i help people in terms of coding. Or any technical problems.
Gomashio or PDF if you see this keep up the great work <3


I Spent Alot Of Time On This Bot So if You Could Support Me By Joining I would appreciate it!
    - Pirxcy
""" 
import fortnitepy
import traceback
import sanic
import logging
import PirxcyPinger
import json
import sys
import os
import asyncio
import aiohttp

from fortnitepy.ext import commands

loop = asyncio.get_event_loop()
app = sanic.Sanic("PirxcyBot")
logging.basicConfig(format='[PirxcyBot] [%(asctime)s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def clear():
  os.system('cls || clear')

async def get_items():
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="GET",
      url="https://fortnite-api.com/v2/cosmetics/br/"
      ) as r:
      main_ = await r.text()
  main = json.loads(main_)
  items = main['data']
  file = open("items.json", "w")
  json.dump(items, file, indent=2)
  file.close()
  logging.info('Cached All bot Items')
  return

async def get_settings():
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="GET",
      url="https://lobbybotconfiguration.pirxcyfinal.repl.co/blacklist"
      ) as r:
          main = await r.json()
  return main

async def post_blacklist(id):
  blacklist = await get_settings()
  blacklist['blocked_names'].append(id)
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="POST",
      url="https://lobbybotconfiguration.pirxcyfinal.repl.co/blacklist",
      json=(blacklist)
      ) as r:
      return

def open_config():
  with open('config.json') as f:
    try:
      data = json.load(f)
      return data
    except json.decoder.JSONDecodeError:
      print("An Json Decode Error Occured While Reading config.json (Contact Pirxcy for Help)")
      sys.exit()
    except FileNotFoundError:
      pass

def is_admin():
  async def predicate(ctx):
    config = open_config()
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
    owners.append(config['owner'])
    return ctx.author.id in owners
  return commands.check(predicate)

def load_cosmetics():
  with open('items.json') as f:
    try:
      data = json.load(f)
      return data
    except json.decoder.JSONDecodeError:
      print("An Json Decode Error Occured While Reading items.json (Contact Pirxcy for Help)")
      sys.exit()

response = input('Enter A Valid Authorization Code: ')
try:
  url = PirxcyPinger.get_url(platform='replit')
except:
  logging.error('Invalid Platform Please Use on Replit!')

if "redirectUrl" in response:
  response = json.loads(response)
  if "?code" not in response["redirectUrl"]:
    print('You Have Entered An Invalid Authorization Code!')
    sys.exit()
  code = response["redirectUrl"].split("?code=")[1]
else:
  if "https://accounts.epicgames.com/fnauth" in response:
    if "?code" not in response:
      print('You Have Entered An Invalid Authorization Code!')
      sys.exit()
    code = response.split("?code=")[1]
  else:
    code = response
    
async def code_to_auths(code):
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="POST",
      url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
      data=f"grant_type=authorization_code&code={code}",
      headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
      }
      ) as r:
      data_ = await r.text()
      data = json.loads(data_)
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="POST",            
      url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}/deviceAuth",
      headers={
        "Authorization": f"Bearer {data['access_token']}",
        "Content-Type": "application/json"
      }
    ) as r:
      data2 = await r.text()
      auths = json.loads(data2)
    auths['created'].pop('ipAddress')         
    return auths

auths = loop.run_until_complete(code_to_auths(code))

bot = commands.Bot(
  command_prefix="!",
  case_insensitive=True,
  auth=fortnitepy.DeviceAuth(
    device_id=auths['deviceId'],
    account_id=auths['accountId'],
    secret=auths['secret']
  )
)

@app.route('/')
async def index(request):
  return sanic.response.text('Client Ready')

@bot.event
async def event_party_invite(invite):
  config = open_config()
  settings = await get_settings()
  owners = [i for i in settings['whitelist_id']]
  owners.append(config['owner'])
  if invite.sender.id in owners:
    try:
      await invite.accept()
    except Exception:
      pass
  else:
    await invite.decline()

@bot.event
async def event_ready():
  config = open_config()
  if config['owner'] == "":
    logging.info('You Haven\'t Filled Out The Config! (Expect Errors To Occur)')
  try:
    user = await bot.fetch_profile(config['owner'])
    if user.id in bot.friends:
      await user.invite()
    else:
      await bot.unblock_user(user.id)
      await bot.add_friend(user.id)
  except:
    pass
  await get_items()
  await bot.set_presence(config['status']) 
  clear()
  logging.info(f'Launched {bot.user.display_name}')
  try:
    await PirxcyPinger.post(f"https://{os.environ['REPL_ID']}.id.repl.co")
    logging.info('Uploaded URL To PirxcyPinger!')
  except PirxcyPinger.AlreadyPinging: #if url is already submitted
    logging.error('Already Pinging URL!')
  except:
    pass

@bot.event
async def event_party_member_join(member):
  config = open_config()
  settings = await get_settings()
  owners = [i for i in settings['whitelist_id']]
  owners.append(config['owner'])
  if member.id in owners:
    logging.info(f'{member.display_name} (An Admin) Has Joined!')
    await member.promote()
    await bot.party.send(config['join_message'])
    await bot.party.send("An Admin of This Bot Has Joined!")
  elif member.display_name in settings['blocked_names']:
    await post_blacklist(id=member.display_name)
    await member.block()
    await member.kick()
  else:
    logging.info(f'{member.display_name} Has Joined!')
    await bot.party.send(f"{config['join_message']}\nMade By Pirxcy")
    

@bot.event
async def event_friend_message(message):
  settings = await get_settings()
  if message.author.display_name in settings['blocked_names']:
    await message.author.block()
    await message.author.kick()
    logging.info(f'Blocked/Kicked {message.author.display_name}')
    await bot.process_commands(message)
  elif any(word.lower() in message.content.lower() for word in settings['blacklist_keywords']):
    await post_blacklist(id=message.author.id)
    logging.info(f'Added {message.author.display_name} to the blacklist!')
    await bot.process_commands(message)
  else:
    logging.info(f'[{message.author.display_name}] {message.content}')
    await bot.process_commands(message)

@bot.event
async def event_party_message(message):
  settings = await get_settings()
  if message.author.display_name in settings['blocked_names']:
    await message.author.block()
    await message.author.kick()
    logging.info(f'Blocked/Kicked {message.author.display_name}')
  elif any(word.lower() in message.content.lower() for word in settings['blacklist_keywords']):
    await post_blacklist(id=message.author.display_name)
    await message.author.block()
    await message.author.kick()
    logging.info(f'Added {message.author.display_name} to the blacklist!')
  else:
    logging.info(f'[{message.author.display_name}] {message.content}')

@bot.command()
async def hello(ctx):
  await ctx.send('Hello!')

@bot.command()
async def skin(ctx, *, content = None):
  logging.info(f'{ctx.author} Excecuted The Skin command')
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !skin ikonik')    
    elif content.upper().startswith('CID_'):
      await bot.party.me.set_outfit(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('CID_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

      if result == []:
        await ctx.send('No Result Found')      

      elif len(result) == 1:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await bot.party.me.set_outfit(asset=result[0]['id'])                    
        skinname = result[0]['name']
        await ctx.send(f"Equiped {skinname}")                
        del result[0]

      else:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await ctx.send(
          f"Result For {content}\n"
          +
          "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
        )
        def check(m): 
          return m.author.id == ctx.author.id
        msg = await bot.wait_for("party_message", check=check)
               
        await bot.party.me.set_outfit(asset=result[int(msg.content)]['id'])
        skinname = result[int(msg.content)]['name']
        await ctx.send(f'Equiped {skinname}')
        del result[int(msg.content)]
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')

@bot.command()
async def emote(ctx, *, content = None):
  logging.info(f'{ctx.author} Excecuted The Emote command')
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !emote scenario')    
    elif content.upper().startswith('EID_'):
      await bot.party.me.set_emote(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('EID_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

      if not result:
        await ctx.send('No Result Found')
        return    

      elif len(result) == 1:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await bot.party.me.set_emote(asset=result[0]['id'])                    
        skinname = result[0]['name']
        await ctx.send(f"Equiped {skinname}")                
        del result[0]
        return

      else:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await ctx.send(
          f"Result For {content}\n"
          +
          "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
        )
        def check(msg): 
          return msg.author == ctx.author
        
        msg = await bot.wait_for("party_message", check=check)                  
        await bot.party.me.set_emote(asset=result[int(msg.content)]['id'])
        skinname = result[int(msg.content)]['name']
        await ctx.send(f'Equiped {skinname}')
        del result[int(msg.content)]
        return
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')
  
@bot.command()
async def backpack(ctx, *, content = None):
  logging.info(f'{ctx.author} Excecuted The Backpack command')
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !backpack black shield')    
    elif content.upper().startswith('BID_'):
      await bot.party.me.set_backpack(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('BID_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

        if not result:
          await ctx.send('No Result Found')      

        elif len(result) == 1:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await bot.party.me.set_backpack(asset=result[0]['id'])                    
          skinname = result[0]['name']
          await ctx.send(f"Equiped {skinname}")                
          del result[0]

        else:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await ctx.send(
            f"Result For {content}\n"
            +
            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
          )
          def check(msg): 
            return msg.author == ctx.author
          
          msg = await bot.wait_for("party_message", check=check)                  
          await bot.party.me.set_backpack(asset=result[int(msg.content)]['id'])
          skinname = result[int(msg.content)]['name']
          await ctx.send(f'Equiped {skinname}')
          del result[int(msg.content)]
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')

@bot.command()
async def pickaxe(ctx, *, content = None):
  logging.info(f'{ctx.author} Excecuted The Pickaxe command')
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !backpack black shield')    
    elif content.upper().startswith('Pickaxe_'):
      await bot.party.me.set_pickaxe(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('Pickaxe_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

        if not result:
          await ctx.send('No Result Found')      

        elif len(result) == 1:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await bot.party.me.set_pickaxe(asset=result[0]['id'])                    
          skinname = result[0]['name']
          await ctx.send(f"Equiped {skinname}")                
          del result[0]

        else:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await ctx.send(
            f"Result For {content}\n"
            +
            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
          )
          def check(msg): 
            return msg.author == ctx.author and msg.content
          
          msg = await bot.wait_for("party_message", check=check)                  
          await bot.party.me.set_pickaxe(asset=result[int(msg.content)]['id'])
          skinname = result[int(msg.content)]['name']
          await ctx.send(f'Equiped {skinname}')
          del result[int(msg.content)]
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')

#most commands below are stolen from xensis all credits to him
#i have modified most of these commands

@bot.command()
async def pinkghoul(ctx):
  logging.info(f'{ctx.author} Excecuted pinkghoul')
  await bot.party.me.set_outfit(
    asset='CID_029_Athena_Commando_F_Halloween',
    variants=bot.party.me.create_variants(
      material=3
    )
  )
  await ctx.send('Equiped Pink Ghoul Trooper')

@bot.command()
async def checkeredrenegade(ctx):
  logging.info(f'{ctx.author} Excecuted checkeredrenegade')
  await bot.party.me.set_outfit(
    asset='CID_028_Athena_Commando_F',
    variants=bot.party.me.create_variants(
      material=2
    )
  )
  await ctx.send('Equiped Checkered Renegade Raider')

@bot.command()
async def purpleportal(ctx):
  logging.info(f'{ctx.author} Excecuted purpleportal')
  await bot.party.me.set_backpack(
    asset='BID_105_GhostPortal',
    variants=bot.party.me.create_variants(
      item='AthenaBackpack',
      particle_config='Particle',
      particle=1
    )
  )
  await ctx.send('Equiped Purple Ghost Portal')

@bot.command()
async def purpleskull(ctx):
  logging.info(f'{ctx.author} Excecuted purpleskull')
  await bot.party.me.set_outfit(
    asset='CID_030_Athena_Commando_M_Halloween',
    variants=bot.party.me.create_variants(
      clothing_color=1
    )
  )
  await ctx.send('Equiped Purple Skull Trooper')

@bot.command()
async def goldpeely(ctx):
  logging.info(f'{ctx.author} Excecuted goldpeely')
  await bot.party.me.set_outfit(
    asset='CID_701_Athena_Commando_M_BananaAgent',
    variants=bot.party.me.create_variants(
      progressive=4
    ),
    enlightenment=(
      2, 
      350
    )
  )
  await ctx.send('Equiped Gold Peely')

@bot.command()
async def hatlessrecon(ctx):
  logging.info(f'{ctx.author} Excecuted hatlessrecon')
  await bot.party.me.set_outfit(
    asset='CID_022_Athena_Commando_F',
    variants=bot.party.me.create_variants(
      parts=2
    )
  )
  await ctx.send('Equiped Hatless recon')

@bot.command()
async def hologram(ctx):
  logging.info(f'{ctx.author} Excecuted hologram')
  await bot.party.me.set_outfit(
    asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
  )
  await ctx.send('Equiped hologram')

@bot.command()
async def ready(ctx):
  logging.info(f'{ctx.author} Excecuted ready')
  await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
  await ctx.send('Bot is Ready!')

@bot.command()
async def unready(ctx):
  logging.info(f'{ctx.author} Excecuted unready')
  await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
  await ctx.send('Bot is Unready!')

@bot.command()
async def sitin(ctx):
  logging.info(f'{ctx.author} Excecuted sitin')
  await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
  await ctx.send('Sitting in')

@bot.command()
async def sitout(ctx):
  logging.info(f'{ctx.author} Excecuted sitout')
  await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
  await ctx.send('Sitting out')

@bot.command()
async def tier(ctx, tier = None):
  logging.info(f'{ctx.author} Excecuted tier')
  if tier is None:
    await ctx.send('Try !tier 1942') 
  else:
    await bot.party.me.set_battlepass_info(
      has_purchased=True,
      level=tier
    )
  await ctx.send(f'Set tier to {tier}')

@bot.command()
async def level(ctx, level = None):
  logging.info(f'{ctx.author} Excecuted level')
  if level is None:
    await ctx.send(f'Try !level 1942')
  else:
    await bot.party.me.set_banner(season_level=level)
    await ctx.send(f'Set level to {level}')

@bot.command()
@is_admin()
async def say(ctx, *, message = None):
  logging.info(f'{ctx.author} Excecuted say')
  if message is not None:
    await bot.party.send(message)
    await ctx.send(f'Message Sent.')
  else:
    await ctx.send(f'Try !say Hi')

@bot.command()
@is_admin()
async def status(ctx, *, status = None):
  if status is None:
    await ctx.send('Try !status 1942')
  else:
    await bot.set_presence(status) 
    await ctx.send(f'Status set')

@bot.command()
@is_admin()
async def leave(ctx):
  await ctx.send('Bye.')
  await bot.party.me.set_emote(asset='EID_Wave')
  await asyncio.sleep(1.5)
  await bot.party.me.leave()

@bot.command()
@is_admin()
async def join(ctx, *, member = None):
  try:
    if member is None:
      user = await bot.fetch_profile(ctx.message.author.id)
      friend = bot.get_friend(user.id)
    elif member is not None:
      user = await bot.fetch_profile(member)
      friend = bot.get_friend(user.id)
      await friend.join_party()
      await ctx.send(f"Joined {friend.display_name}")
  except fortnitepy.Forbidden:
      await ctx.send("Party is Private :(")
  except fortnitepy.PartyError:
      await ctx.send("That user is already here.")
  except fortnitepy.HTTPException:
      await ctx.send("An Unknown Error Occured")
  except AttributeError:
      await ctx.send("I can not join that party. Are you sure I have them friended?")


loop.create_task(app.create_server(host='0.0.0.0', port=8080, return_asyncio_server=True,  access_log=True))
loop.create_task(bot.start())
loop.run_forever()