from random import choice, randint
from typing import Optional
from aiohttp import request
from discord.ext.commands import BadArgument
from discord import Member, Embed
from discord.errors import HTTPException
from discord.ext.commands import command, Greedy, cooldown, has_permissions, has_any_role, has_role, CheckFailure, Cog, BucketType, is_owner
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
import googletrans
from googletrans import Translator
from discord.errors import Forbidden

# |CUSTOM|
embed_color = 0xBC0808
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
	
	# #NUKE COMMAND
	# @command(name="nuke",brief="Nuke the server", help="Nukes the server completely, **obv**")
	# @has_any_role(812817220752900157,751028067446554704,806886607541633045,810854901055225907)
	# async def nuke(self, ctx):
	# 	first = await ctx.channel.send(":warning::warning: **Nuke initiated** :warning::warning:")
	# 	second = await first.edit(content="Retrieving server information.")
	# 	third = await second.edit(content="Retrieving server information..")
	# 	fourth = await third.edit(content="Retrieving server information...")
	# 	fifth = await fourth.edit(content="Collecting members information.")
	# 	sixth = await fifth.edit(content="Collecting members information..")
	# 	seventh = await sixth.edit(content="Collecting members information...")
	# 	eighth = await seventh.edit(content="Successfully retrieved all information\nInitiating protocol 69")
	# 	nineth = await eighth.edit(content="Breaching protocol 420\nApplying protocol 69")
	# 	tenth = await nineth.edit(content="Success")
	# 	eleventh = await tenth.edit(content="Detecting server owner")
	# 	twelveth = await eleventh.edit(content="<@478815409177362432> gay ass detected as **current** server owner\n||ima end this gays whole career, hold my chapal||")
	# 	thirteenth = await twelveth.edit(content="Switching ownership to <@726480855689724105> chad\n*bows in respect*")
	# 	fourteenth = await thirteenth.edit(content="Successfully granted server ownership to <@726480855689724105> [||chad||] and denied from <@478815409177362432> [||gay||]")
	# 	await fourteenth.edit(content="em too lazy to complete the nuke, ill do it later smh")
	
	# @command(name="spam")
	# @has_any_role(848311479941726288)
	# async def spam(self,ctx,*, message):
	# 	for i in range(10000000000):
	# 		await ctx.send(message)

	#AV COMMAND
	@command(name="av", brief="View User Avatar", help="Displays user avatar")
	@cooldown(3, 60, BucketType.user)
	async def display_avatar(self, ctx, target: Optional[Member]):
			target = target or ctx.author
			embed = Embed(title=f"{target.display_name}'s Avatar",url="https://pornhub.com/",color=0xBC0808)
			embed.set_image(url=f"{target.avatar_url}")
			embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
			await ctx.reply(embed = embed)

	#DM COMMAND
	@command(name="dm")
	@cooldown(3, 30, BucketType.user)
	@has_any_role(847565615329574913, 848311479941726288)
	async def dm(self, ctx, form, targets: Greedy[Member], *, message):
		for target in targets:
			if target != ctx.author:
				if target != self.bot.user:	
					if form == "embed" or form == "Embed":
						try:
							embed = Embed(description= f"{message}", color=0xBC0808)
							await target.send(embed=embed)
							embed = Embed(description=f"I dmed **{target.name}#{target.discriminator}** with the message **{message}**", color=0xBC0808)
							return await ctx.reply(embed=embed)

						except:
							embed = Embed(description=f"I am unable to dm **{target.name}#{target.discriminator}**", color=0xBC0808)
							await ctx.reply(embed=embed)
					else:
						try:
							await target.send(f"{message}")
							return await ctx.reply(f"I dmed **{target.name}#{target.discriminator}** with the message **{message}**")
						
						except:
							return await ctx.reply(f"I am unable to dm **{target.name}#{target.discriminator}**")
				else:
					return await ctx.reply("How tf do i dm myself?")
			else:
				return await ctx.reply("Why should i dm you <:cringe:789523123389202452>")				
	
	#URBAN COMMAND
	@command(name="urban", brief="Urban Dictionary Search", help="Gets definitions of provided words from urban dictionary")
	@cooldown(3, 60, BucketType.user)
	async def urban(self, ctx, *, search_terms : str):
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
				embed = Embed(title=f"Search Results For {search_terms}", color=0xBC0808)
				fields = [("Defination", a.replace("]", ""), False),
						("Example", b.replace("[","") , False)]
				for name , value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
					embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
				await ctx.reply(embed=embed)
			else:
				await ctx.reply("Your search terms gave no results.", delete_after=10)
		except:
			await ctx.reply("The API returned nothing!", delete_after=10)

	@command(name="translate", aliases = ["t"])
	async def translate(self, ctx, lang_to, *args):
	    lang_to = lang_to.lower()
	    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
	        await ctx.send("tf is that <:cringe:789523123389202452>")

	    else:
		    text = ' '.join(args)
		    this = await ctx.send("Translating <a:redstar:802810542233485323>")
		    translator = Translator()
		    text_translated = translator.translate(text, dest= lang_to)
		    await this.delete()
		    await ctx.send(text_translated.text)

	#8BALL COMMAND    
	@command(name="8ball", brief="Ask 8Ball Questions", help="Ask 8ball any question you want")
	@cooldown(3, 60, BucketType.user)
	async def _8ball(self,ctx,*question):
		question = "  ".join(question)
		embed = Embed(description=f"**{randchoice(self.ball)}**", color=0xBC0808)
		await ctx.message.delete(delay=120)
		return await ctx.reply(embed=embed, delete_after=120)


	#STOPWATCH COMAND
	@command(name="stopwatch", brief="Start A Timer", help="Stopwatch, works like you expect it to")
	@cooldown(6, 60, BucketType.user)
	async def stopwatch(self, ctx):
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
		embed = Embed(title="Member Count", color=0xBC0808)
		fields = [("Members", len(ctx.guild.members), False),
				("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))),False),
				("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), False)]
		for name , value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.reply(embed=embed)

	
	#SEND ANNOUNCEMENT EMBEDS COMMAND
	@command(name="aembed",brief="Send Embeds",help="Send announcement embeds through the bot.", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def say_announcement_embed(self, ctx, *, message):	
		embed=Embed(description=f"{message}",color=embed_color)
		embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
		await ctx.send(embed=embed)
		await ctx.message.delete()
	

	#SEND EMBEDS COMMAND
	@command(name="embed",brief="Send Embeds",help="Send embeds through the bot.", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def say_embed(self, ctx, *, message):	
		embed=Embed(description=f"{message}",color=embed_color)
		await ctx.send(embed=embed)
		await ctx.message.delete()


    #SEND MESSAGES COMMAND
	@command(name="say",brief="Send Messages",help="Send a message through the bot\n \n**Required Roles** \n<@&776069302045769759> and above", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def say_message(self, ctx,*, message):		
		await ctx.send(f"{message}")
		await ctx.message.delete()
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun") #IMPORTANT! - ("Fun") is the FILE NAME, NOT print name. 

def setup(bot):
	bot.add_cog(Fun(bot))
