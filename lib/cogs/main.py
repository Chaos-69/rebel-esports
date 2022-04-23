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
from discord_components import *
from discord_slash import SlashCommand

# |CUSTOM|
embed_color = 0xBC0808
# |CUSTOM|

class Main(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ddb = DiscordComponents(self.bot)
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
	@command(name="av", brief="Avatar", help="Displays user avatar, its literally in the name")
	@cooldown(3, 60, BucketType.user)
	async def display_avatar(self, ctx, target: Optional[Member]):
			target = target or ctx.author
			embed = Embed(title=f"{target.display_name}'s Avatar",url=f"{target.avatar_url}",color=0xBC0808)
			embed.set_image(url=f"{target.avatar_url}")
			embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
			await ctx.reply(embed = embed)

	#DM COMMAND
	@command(name="dm", brief="Dm people", help="Literally dms people, what else were you expecting you dumbfuck")
	@cooldown(3, 30, BucketType.user)
	@has_any_role(847565615329574913, 848311479941726288, 860287157418721311)
	async def dm(self, ctx, targets: Greedy[Member], *, message):
		for target in targets:
			if target != ctx.author:
				if target != self.bot.user:	
					try:
						await target.send(f"{message}")
						await ctx.message.delete()
						return await ctx.reply(f"I dmed **{target.name}#{target.discriminator}** with the message **{message}**", delete_after=10)
						
					except:
						await ctx.message.delete()
						return await ctx.reply(f"I am unable to dm **{target.name}#{target.discriminator}**")
				else:
					await ctx.message.delete()
					return await ctx.reply("How tf do i dm myself?")
			else:
				await ctx.message.delete()
				return await ctx.reply("Why should i dm you <:cringe:789523123389202452>")				
	
	#URBAN COMMAND
	@command(name="urban", brief="Urban Dictionary Search", help="Idk what this does, urban it or something")
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

	@command(name="translate", aliases = ["t"], brief="Translator", help="Does exactly what you expect it to do")
	async def translate(self, ctx, lang, *sentence):
	    lang = lang.lower()
	    if lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:
	        await ctx.send("tf is that <:cringe:789523123389202452>")

	    else:
		    text = ' '.join(sentence)
		    this = await ctx.send("Translating <a:redstar:802810542233485323>")
		    translator = Translator()
		    text_translated = translator.translate(text, dest= lang)
		    await this.delete()
		    await ctx.send(text_translated.text)

	#8BALL COMMAND    
	@command(name="8ball", brief="8Ball", help="Ask 8ball questions and depend your life decisions on this puppy")
	@cooldown(3, 60, BucketType.user)
	async def _8ball(self,ctx,*question):
		question = "  ".join(question)
		embed = Embed(description=f"**{randchoice(self.ball)}**", color=0xBC0808)
		await ctx.message.delete(delay=120)
		return await ctx.reply(embed=embed, delete_after=120)


	#STOPWATCH COMAND
	@command(name="stopwatch", brief="Stopwatch", help="Starts a timer, works like you expect it to")
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
	@command(name="membercount", aliases=["mc"], brief="Member Count", help="Gives the number of gays who are dumb enough to join this stupid server")
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
	@command(name="aembed",brief="Announcement Embeds",help="Send announcement embeds through the bot.", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 860287157418721311)
	async def say_announcement_embed(self, ctx, *, message):	
		embed=Embed(description=f"{message}",color=embed_color)
		embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
		await ctx.send(embed=embed)
		await ctx.message.delete()
	

	#SEND EMBEDS COMMAND
	@command(name="embed",brief="Plain Embeds",help="Send embeds through the bot.", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 860287157418721311)
	async def say_embed(self, ctx, *, message):	
		embed=Embed(description=f"{message}",color=embed_color)
		await ctx.send(embed=embed)
		await ctx.message.delete()


    #SEND MESSAGES COMMAND
	@command(name="say",brief="Send Messages",help="Send a message through the bot\n \n**Required Roles** \n<@&776069302045769759> and above", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 860287157418721311)
	async def say_message(self, ctx,*, message):		
		await ctx.send(f"{message}")
		await ctx.message.delete()

	def convert(self, time):
		pos = ["s","m","h","d"]

		time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

		unit = time[-1]

		if unit not in pos:
			return -1
		try:
			val = int(time[:-1])
		except:
			return -2

		return val * time_dict[unit]
	
	# #CALLOUT COMMAND
	# @command(name="callout", brief="RES Callouts", help="Call out lineup members to play")
	# @has_any_role(848311479941726288, 860287157418721311, 859087645547954209, 808955841599766529 )
	# async def callouts(self, ctx):
		
	# 	start_embed = Embed(title="<:salute:846442658263203880> Callout Initiated", description=f"Let's start with this callout! \n Answer these questions within **60 seconds**! \n Reply with `{ctx.prefix}cancel` if you wish to cancel this process anytime",color=embed_color)
	# 	start_message = await ctx.send(embed=start_embed)
		
	# 	role_embed = Embed(title="<:res:860644959241240576>  RES Role",description=f"Which lineup **role** would you like to send a callout for? \nFor example `S` , `3` , `X` or `Y` \n **Note:** Do not add `RES |` before the role name", color=embed_color)
	# 	role_embed.set_footer(text=f"Question 1/5")
		
	# 	time_embed = Embed(title=":watch: Time",description="Lets decide a **time** for the callout\n When do you want players to come? \n For example in `2h`, `30m` , `5h` , `45m` \n **Note:** Only add `s`, `m` or `h` after the integer", color=embed_color)
	# 	time_embed.set_footer(text=f"Question 2/5")

	# 	mode_embed = Embed(title="<a:pepe_pew:782343942745489448>  Gamemode", description="Which **gamemode** do you want to post a callout for? \n Mention a gamemode like `Scrims`, `Tourney`, `Ranked`, `Inners`", color=embed_color)
	# 	mode_embed.set_footer(text=f"Question 3/5")

	# 	slots_embed = Embed(title="<:RES_cheemsThiccMhm:823612526775238666> Slots", description="How many **slots** are avaliable?", color=embed_color)
	# 	slots_embed.set_footer(text=f"Question 4/5")		

	# 	message_embed = Embed(title=":scroll: Message", description="What is your **message** for the callout? \n **Note:** You can include the room link aswell", color=embed_color)
	# 	message_embed.set_footer(text=f"Question 5/5")

	# 	questions = [role_embed , time_embed , mode_embed, slots_embed, message_embed,]

	# 	answers = []
		
	# 	def check(m):
	# 		return m.author == ctx.author and m.channel == ctx.channel
		
	# 	for i in questions:
	# 		await ctx.send(f"||{ctx.author.mention}||", embed=i)

	# 		try:
	# 			msg = await self.bot.wait_for('message', timeout=60.0, check=check)
			
	# 		except asyncio.TimeoutError:
	# 			embed = Embed(title=":exclamation: Process Canceled", description="You didn\'t answer in the given time!\nPlease answer in under **60 seconds** next time!",color=0x000000)
	# 			await ctx.send(embed = embed,delete_after=10)
	# 			return
			
	# 		else:
	# 			if msg.content == f"{ctx.prefix}cancel":
	# 				embed = Embed(title=":exclamation: Process Canceled",description="Process has been canceled sucessfully", color=0x000000)
	# 				await ctx.send(embed = embed,delete_after=10)
	# 				return
	# 			answers.append(msg.content)

	# 	role = answers[0]
	# 	role_mention = "<@&857698644291485766>"
	# 	role_name = "RES | Y"

	# 	if role == "s" or role == "S":
	# 		role_mention = "<@&857698639169978379>"
	# 		role_name = "RES | S"
		
	# 	elif role == "3":
	# 		role_mention = "<@&857698642638798890>"
	# 		role_name = "RES | 3"
		
	# 	elif role == "x" or role == "X":
	# 		role_mention = "<@&857698643308970004>"
	# 		role_name = "RES | X"
		
	# 	elif role == "y" or role == "Y":
	# 		role_mention == "<@&857698644291485766>"
	# 		role_name = "RES | Y"

	# 	else:
	# 		embed = Embed(title=":exclamation: Process Canceled",description=f"You didn\'t answer with a proper role! Use either `S`, `3`, `X` or `Y`", color=0xBC0808)
	# 		await ctx.send(embed=embed)
	# 		return

	# 	time = self.convert(answers[1])
	# 	display_time = answers[1]
		
	# 	if time == -1:
	# 		embed = Embed(title=":exclamation: Process Canceled",description=f"You didn\'t answer with a proper unit! Use either **(s|m|h|d)**\n For example `2h` , `4d` , `30m`", color=0xBC0808)
	# 		await ctx.send(embed=embed,delete_after=10)
	# 		return
		
	# 	elif time == -2:
	# 		embed = Embed(title=":exclamation: Process Canceled", description=f"The time must be an integer. Please enter an integer next time.",color=0xBC0808)
	# 		await ctx.send(embed =embed,delete_after=10)
	# 		return
		
	# 	mode = answers[2]
	# 	slots = answers[3]
	# 	message = answers[4]
		
	# 	await ctx.channel.purge(limit=12)

	# 	try:
	# 		embed = Embed(title="<a:Check:856282490670284802> Callout Posted", description=f"**Your callout has been posted in {self.callout_channel.mention}** \n I will remind **{role_name}** before the match!",color=embed_color)
	# 		await ctx.author.send(embed=embed)
		
	# 	except:
	# 		embed = Embed(title="<a:Check:856282490670284802> Callout Posted", description=f"**Your callout has been posted in {self.callout_channel.mention}** \n I will remind **{role_name}** before the match! \n On a side note, enable your dms noob",color=embed_color)
	# 		await ctx.channel.send(embed=embed)
		
	# 	embed = Embed(title = "Callout",color = ctx.author.color, timestamp=datetime.utcnow())
		
	# 	fields = [("Time", f"Match starting in {display_time}", False),
	# 			("Gamemode", mode, False),
	# 			("Available Slots", slots, False),
	# 			("Message", message, False)]
	# 	for name , value, inline in fields:
	# 		embed.add_field(name=name, value=value, inline=inline)
		
	# 	embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/I_vJq0oj4jpiz4DszZU4LTAlhQKWgBwWSMEPVLWVdlE/%3Fv%3D1/https/cdn.discordapp.com/emojis/851381516700221450.png")
	# 	embed.set_footer(text = f"Called By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")

	# 	my_msg = await self.callout_channel.send(f"{role_mention}",embed=embed)

	# 	await my_msg.add_reaction(":halal:834154424393531392")
	# 	await my_msg.add_reaction(":haram:834154339392028692")


	# 	await asyncio.sleep(time-5*60)

	# 	embed = Embed(title=f"Match Reminder!", 
	# 		description=f"**{mode}** match will start in **5 minutes** \n **Avaliable Slots:** {slots} \n Contact {ctx.author.mention} for room link",
	# 		color=embed_color)
	# 	embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/I_vJq0oj4jpiz4DszZU4LTAlhQKWgBwWSMEPVLWVdlE/%3Fv%3D1/https/cdn.discordapp.com/emojis/851381516700221450.png")
	# 	await self.callout_channel.send(f"{role_mention}", embed=embed)
	# 	try:
	# 		await ctx.author.send(f"__**Reminder**__ \n **{mode}** match for **{role_name}** is starting in **5 minutes** \n Send the room link in <#840353352466038814>")
		
	# 	except:
	# 		await ctx.channel.send(f"{ctx.author.mention} Please send the room link")
		

	# 	await asyncio.sleep(5*60)

	# 	embed = Embed(title=f"Match Starting Soon!", 
	# 		description=f"**{mode}** match is about to start! \n **Avaliable Slots:** {slots} \n {ctx.author.mention} will provide the room link soon \n Good Luck nibbas <a:pet:801495732233961492> ",
	# 		color=embed_color)
	# 	embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/I_vJq0oj4jpiz4DszZU4LTAlhQKWgBwWSMEPVLWVdlE/%3Fv%3D1/https/cdn.discordapp.com/emojis/851381516700221450.png")
	# 	await self.callout_channel.send(f"{role_mention}", embed=embed)
	# 	try:
	# 		await ctx.author.send(f"__**Reminder**__ \n **{mode}** match for **{role_name}** is starting soon! \n Send the room link in <#840353352466038814> asap! \n Good Luck!")
	# 	except:
	# 		await ctx.channel.send(f"{ctx.author.mention} Please send the room link")
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			# self.callout_channel = self.bot.get_guild(803028981698789407).get_channel(840353352466038814)
			self.bot.cogs_ready.ready_up("main")

def setup(bot):
	bot.add_cog(Main(bot))
