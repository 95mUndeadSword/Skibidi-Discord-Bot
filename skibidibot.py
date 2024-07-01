import discord
import os
import requests
import json
import random
import datetime
import asyncio
from datetime import timedelta
from discord.ext import commands
from discord.ui import Button, View
from discord.utils import get
print(discord.__version__)
#richard's ID: 562250979320528897
#markus chu's ID: 849157420957564968
#my ID: 877822920578174986


#List of commands: help, ping, dm, openchannel, mute, addrole, removerole, unmute, purge, userinfo, serverinfo, tictactoe, battlefield, listen(always active)

#both skibidi. and s. prefixes work
client = commands.Bot(command_prefix = commands.when_mentioned_or('skibidi.', 's.'), intents=discord.Intents.all())
client.remove_command("help")

#confirm message on console to make sure bot is active
@client.event
async def on_ready():
  print("skibidi activated")

#error control
@client.event
async def on_command_error(ctx, error):
    # Sends a message to the channel where the error occurred
    await ctx.send(f"An error occurred: {str(error)}")

#upgraded help command
@client.command()
async def help(ctx):
  file = discord.File("skibidi.jpeg",filename="skibidigman.png")
  desc = ""
  cmds = client.commands
  embed = discord.Embed(title="Available commands", color=discord.Color.random())
  embed.add_field(name="Moderation Commands", value="mute\nunmute", inline=False)
  embed.add_field(name="Utility Commands", value="ping\ndm\nopenhannel\npurge\nuserinfo\nserverinfo\naddrole\nremoverole", inline=False)
  embed.add_field(name="Fun Commands", value="N/A", inline=False)
  embed.add_field(name="Other Commands", value="invite\nhelp\nvc\njoinvc", inline=False)
  embed.add_field(name="Commands not yet implemented:",value="newestskibidi\nforms\npingmewhen\naddmusictoqueue\nremovemusicfromqueue\nplayqueue")
  embed.set_image(url="attachment://skibidigman.png")
  await ctx.reply(embed=embed,file=file)

#check for bad words (customizable with the array badwords)
@client.event
async def on_message(message):
  badwords = ["orn!cleanse","orn!ily","orn!echo","orn!pic","orn!question","orn!help","orn!ping","$buttons","-annoyjasoon","-say"]
  file = discord.File("skibidiwave.png",filename="scientistwave.png")
  embed=discord.Embed()
  embed.set_image(url="attachment://scientistwave.png")
  for word in badwords:
      if word in message.content:
            await message.channel.send("Not allowed.",file=file,embed=embed)
            break
  await client.process_commands(message)

#sends them a message when they join the server
@client.event
async def on_member_join(member):
  file = discord.File("skibidigreet.png",filename="policeskibidi.png")
  embed = discord.Embed()
  embed.set_image(url="attachment://policeskibidi.png")
  await member.send("Hello! Please be reminded that this is a skibidi server.",file=file,embed=embed)

#generates an invite
@client.command()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age=0, max_uses=0)
    await ctx.reply("New invite link generated: " + str(link))

#sends a link to the newest episode of skibidi toilet
@client.command()
async def newestepisode(ctx):
  file=discord.File("gmanyt.png",filename="gmanyt.png")
  embed=discord.Embed()
  embed.set_image(url="attachment://gmanyt.png")
  await ctx.reply("Here is the newest episode: https://www.youtube.com/watch?v=PLUhJmqHd1s",embed=embed,file=file)

#ping user specified in first argument
@client.command()
async def ping(ctx, user:discord.Member):
  file = discord.File("scientisttoilet.webp",filename="scientiststare.png")
  embed = discord.Embed()
  embed.set_image(url="attachment://scientiststare.png")
  await ctx.reply(f"{user.mention}, you have been summoned!",embed=embed,file=file)

#dm specified user with specified message
@client.command()
async def dm(user:discord.Member, *, message):
  msg=message
  await user.send(msg)

#open a channel (only works for category without a space in name)
@client.command()
async def openchannel(ctx, channel_name: str, *, category_name: str):
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        category = discord.utils.get(ctx.guild.categories, name=category_name.replace('"',""))
    if category:
        guild = ctx.guild
        channel = await guild.create_text_channel(name=channel_name, category=category)
        await channel.send(f"{channel_name} channel created in category: {category.name}")
    else:
        await ctx.send("Category not found.")

#mute user specified in first argument for duration specified in second argument
@client.command()
async def mute(ctx, member: discord.Member, *, duration:str):
  realduration=""
  realdurationint=0
  for i in range(len(duration)):
    if duration[i]=="d" or duration[i]=="h" or duration[i]=="m" or duration[i]=="s":
      realduration+=duration[i]
    else:
      realdurationint=realdurationint*10+int(duration[i])
  await member.timeout(timedelta(days=realdurationint, hours=realdurationint, minutes=realdurationint, seconds=realdurationint))
  await ctx.reply(f"{member.mention} has been muted for {duration}.")

#add a role to specified user with specified rolename
@client.command()
async def addrole(ctx, user:discord.Member, role_name: str):
    role = await ctx.guild.create_role(name=role_name, permissions=discord.Permissions(permissions=0), colour=discord.Color.green())
    await user.add_roles(role)
    await ctx.send(f"Role {role_name} created and assigned to {user.display_name}.")

#remove a role from specified user with specified rolename
@client.command()
async def removerole(ctx, user:discord.Member, role_name: str):
  role = discord.utils.get(ctx.guild.roles, name=role_name)
  await user.remove_roles(role)
  await ctx.send(f"Role {role_name} removed from {user.display_name}.")

#unmute user specified in first argument
@client.command()
async def unmute(ctx, user:discord.Member):
  await user.timeout(None)
  await ctx.reply(f"{user.mention} has been unmuted.")


#purge a specified number of messages
@client.command()
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"{amount} messages have been purged.")
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)

#get user info
@client.command()
async def userinfo(ctx, *, user: discord.Member):
  if user is None:
      user = ctx.author      
  date_format = "%a, %d %b %Y %I:%M %p"
  embed = discord.Embed(color=0xdfa3ff, description=user.mention,title=f"Info of {user}:")
  embed.set_author(name=str(user), icon_url=user.avatar)
  embed.set_thumbnail(url=user.avatar)
  joined_at = user.joined_at.strftime(date_format) if user.joined_at else "N/A"
  created_at = user.created_at.strftime(date_format) if user.created_at else "N/A"
  embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
  members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
  embed.add_field(name="Join Position", value=str(members.index(user)+1))
  embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
  if len(user.roles) > 1:
      role_string = ' '.join([r.mention for r in user.roles][1:])
      embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
  perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
  embed.add_field(name="Guild permissions", value=perm_string, inline=False)
  embed.set_footer(text='ID: ' + str(user.id))
  return await ctx.send(embed=embed)

#get server info
@client.command()
async def serverinfo(ctx):
  total_text_channels=len(ctx.guild.text_channels)
  total_voice_channels=len(ctx.guild.voice_channels)
  embed = discord.Embed(title = f"{ctx.guild.name} Info", description = "Information of this Server", color = discord.Colour.blue())
  embed.add_field(name = 'Server ID', value = f"{ctx.guild.id}", inline = True)
  embed.add_field(name = 'Creation Date', value = ctx.guild.created_at.strftime("%b %d %Y"), inline = True)
  embed.add_field(name = 'Owner', value = f"{ctx.guild.owner}", inline = True)
  embed.add_field(name = 'Members', value = f'{ctx.guild.member_count} Members', inline = True)
  embed.add_field(name = 'Channels', value = f'{total_text_channels} Text | {total_voice_channels} Voice', inline = True)
  embed.set_thumbnail(url = ctx.guild.icon)
  embed.set_footer(text = "skibidi dop dop dop yes yes")    
  await ctx.send(embed=embed)

#join vc
@client.command()
async def vc(ctx):
  if ctx.author.voice is None:
    await ctx.reply("You are not in a voice channel.")
    return
  voice_channel = ctx.author.voice.channel
  if ctx.voice_client is not None:
    await ctx.voice_client.move_to(voice_channel)
  else:
    await voice_channel.connect()

  await ctx.reply(f"Joined the voice channel: {voice_channel.name}")

#leave vc
@client.command()
async def leavevc(ctx):
    if ctx.voice_client is None:
        await ctx.reply("I am not in a voice channel.")
        return
    await ctx.voice_client.disconnect()
    await ctx.reply("I have left the voice channel.")


class TicTacToeButton(Button):
  def __init__(self, x, y, player1, player2):
      super().__init__(style=discord.ButtonStyle.grey, label=".", row=y)
      self.x = x
      self.y = y
      self.player1 = player1
      self.player2 = player2
      self.value = "."

  async def callback(self, interaction):
      if interaction.user == self.player1:
          sign = "X"
          self.style = discord.ButtonStyle.green
      else:
          sign = "O"
          self.style = discord.ButtonStyle.blurple

      self.value = sign
      self.label = sign
      self.disabled = True
      await interaction.response.defer()
      await self.view.update(self.x, self.y, sign)

class TicTacToe(View):
  def __init__(self, ctx, player1, player2):
      super().__init__(timeout=None)
      self.ctx = ctx
      self.player1 = player1  #X
      self.player2 = player2  #O
      if random.randint(1, 2) == 1:
          self.turn = player1
      else:
          self.turn = player2
      self.turns = 0

      self.board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

      for x in range(3):
          for y in range(3):
              btn = TicTacToeButton(x, y, player1, player2)
              self.add_item(btn)

  def check(self):
      for i in range(3):  #check rows
          if self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2] and self.board[i][0] != ".":
              return self.board[i][0]
      for i in range(3):  #check columns
          if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and self.board[2][i] != ".":
              return self.board[0][i]
      if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != ".":
          return self.board[0][0]
      if self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2] and self.board[0][2] != ".":
          return self.board[2][0]
      return False

  async def update(self, x, y, sign):
      self.turns += 1
      self.board[x][y] = sign
      if self.turn == self.player1:  #change the turn
          self.turn = self.player2
      else:
          self.turn = self.player1

      res = self.check()
      if res:
          for item in self.children:
              item.disabled = True #disable all buttons, game over
      if res=="X":
          await self.my_msg.edit(content=f"{self.player1.mention} wins! what a discord mod!", view=self)
          self.stop()
      elif res=="O":
          await self.my_msg.edit(content=f"{self.player2.mention} wins! what a discord mod!", view=self)
          self.stop()
      else:
          if self.turns == 9:
              await self.my_msg.edit(content="wow.. a tie... how boring", view=self)
              self.stop()
          else:
              await self.my_msg.edit(content=f"It's {self.turn.mention}'s turn!", view=self)

  async def interaction_check(self, interaction):
      if interaction.user.id != self.turn.id:
          await interaction.response.send_message("Not your time. Piss off.",ephemeral=True)
          return False
      return True


@client.command(aliases = ["ttt"])
async def tictactoe(ctx, member: discord.Member = None):
  if member is None:
      await ctx.reply("@ a person to play with bro")
      return
  if member==ctx.author:
      await ctx.reply("You can't play with yourself, dumbass")
      return
  if member.bot:
      await ctx.reply("You can't play with bots bruh")
      return

  view = TicTacToe(ctx, ctx.author, member)
  view.my_msg = await ctx.reply(f"It's {view.turn.mention}'s turn!", view=view)

  @client.command()
  async def poll(ctx,)


