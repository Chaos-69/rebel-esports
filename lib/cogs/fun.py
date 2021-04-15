from random import choice, randint
from typing import Optional
from aiohttp import request
from discord.ext.commands import BadArgument
from discord import Member, Embed
from discord.errors import HTTPException
from discord.ext.commands import command, cooldown, has_permissions, has_any_role, has_role, CheckFailure, Cog, BucketType, is_owner
import discord
from datetime import datetime
import asyncio
from discord.ext import commands, menus
import random
import aiohttp
import asyncio
import discord
from random import choice as randchoice
import time
from datetime import timedelta

# |CUSTOM|
embed_color = 0xBC0808
server_logo = "https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png"
# |CUSTOM|

class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.session = aiohttp.ClientSession()
		self.ball = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely", "Outlook good",
			"Sources point to yes", "Without a doubt", "Yes", "Yes – definitely", "You may rely on it", "Reply hazy, try again",
			"Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
			"Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
		self.allowed_channels = (830188895374278686,771083740217999371)
		self.stopwatches = {}
	
	#AV COMMAND
	@command(name="av", brief="View User Avatar", help="Displays user avatar")
	@cooldown(3, 60, BucketType.user)
	async def display_avatar(self, ctx, target: Optional[Member]):
			target = target or ctx.author
			embed = Embed(title=f"{target.display_name}'s Avatar", color=0xBC0808)
			embed.set_image(url=f"{target.avatar_url}")
			embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
			await ctx.reply(embed = embed)
	
	
	#URBAN COMMAND
	@command(name="urban", brief="Urban Dictionary Search", help="Gets definitions of provided words from urban dictionary")
	@cooldown(3, 60, BucketType.user)
	async def urban(self, ctx, *, search_terms : str):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			search_terms = search_terms.split(" ")
			search_terms = "+".join(search_terms)
			search = "http://api.urbandictionary.com/v0/define?term=" + search_terms
			try:
				async with aiohttp.ClientSession() as a:
					async with a.get(search) as r:
						result = await r.json()
				if result["list"] != []:
					definition = result['list'][0]['definition']
					example = result['list'][0]['example']
					a = definition.replace("[", "")
					b = example.replace("]", "")
					embed = Embed(title=f"Search Results For {search_terms}", color=0x000000)
					fields = [("Defination", a.replace("]", ""), False),
							("Example", b.replace("[","") , False)]
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
						embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
					await ctx.reply(embed=embed)
				else:
					await ctx.reply("Your search terms gave no results.", delete_after=10)
			except:
				await ctx.reply("The API retured nothing!", delete_after=10)
	

	#8BALL COMMAND    
	@command(name="8ball", brief="Ask 8Ball Questions", help="Ask 8ball any question you want")
	@cooldown(3, 60, BucketType.user)
	async def _8ball(self,ctx,*question):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			question = "  ".join(question)
			embed = Embed(description=f"**{randchoice(self.ball)}**", color=0xBC0808)
			await ctx.message.delete(delay=120)
			return await ctx.reply(embed=embed, delete_after=120)


	#STOPWATCH COMAND
	@command(name="stopwatch", brief="Start A Timer", help="Record your of any task through stopwatch")
	@cooldown(6, 60, BucketType.user)
	async def stopwatch(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			author = ctx.message.author
			if not author.id in self.stopwatches:
				self.stopwatches[author.id] = int(time.perf_counter())
				embed = Embed(description="**Stopwatch Started!**", color=0xBC0808)
				await ctx.reply(embed=embed)
			
			else:
				tmp = abs(self.stopwatches[author.id] - int(time.perf_counter()))
				tmp = str(timedelta(seconds=tmp))
				embed = Embed(description= author.mention  + " Stopwatch stopped! Time: **" + str(tmp) + "**", color=0xBC0808)
				await ctx.reply(embed=embed)
				self.stopwatches.pop(author.id, None)

	#MEMBER COUNT COMMAND
	@command(name="membercount", brief="Member Count", help="Displays the number of members present in the server")
	@cooldown(3, 60, BucketType.user)
	async def member_count(self,ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0xBC0808, timestamp=datetime.utcnow())
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			embed = Embed(title="Member Count", color=0xBC0808)
			fields = [("Members", len(ctx.guild.members), False),
					("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))),False),
					("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), False)]
			for name , value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_thumbnail(url=ctx.guild.icon_url)
			await ctx.reply(embed=embed)


	#SEND EMBEDS COMMAND
	@command(name="embed",brief="Send Embeds",help="Send embeds throught the bot.", hidden=True)
	@has_any_role(806886607541633045, 776069302045769759)
	async def say_embed(self, ctx, *, message):	
		embed=Embed(description=f"{message}",color=embed_color)
		await ctx.send(embed=embed)
		await ctx.message.delete()


    #SEND MESSAGES COMMAND
	@command(name="say",brief="Send Messages",help="Send a message throught the bot\n \n**Required Roles** \n<@&776069302045769759> and above", hidden=True)
	@has_any_role(806886607541633045,776069302045769759)
	async def say_message(self, ctx,*, message):		
		await ctx.send(f"{message}")
		await ctx.message.delete()
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun") #IMPORTANT! - ("Fun") is the FILE NAME, NOT print name. 

def setup(bot):
	bot.add_cog(Fun(bot))
