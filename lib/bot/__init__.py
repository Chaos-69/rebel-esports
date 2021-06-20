from asyncio import sleep
from datetime import datetime
from glob import glob
from discord.errors import HTTPException, Forbidden
from discord import Intents, DMChannel
from discord import Embed, File
from discord.ext.commands import Context
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, DisabledCommand, RoleNotFound, MemberNotFound, MissingAnyRole, NotOwner
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import when_mentioned_or, command, has_permissions
from ..db import db
import discord
from typing import Optional
import asyncio
import random
from prsaw import RandomStuff
from pathlib import Path
from discord.ext import tasks


# |CUSTOM|
embed_color = 0xBC0808
# |CUSTOM|

OWNER_IDS = [726480855689724105]
COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
	prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
	return when_mentioned_or(prefix)(bot, message)

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)
	
	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f"{cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.ready = False
		self.cogs_ready = Ready()

		self.guild = 736258866504925306
		self.scheduler = AsyncIOScheduler()
		
		try:
			with open("./data/banlist.txt", "r", encoding="utf-8") as f:
				self.banlist = [int(line.strip()) for line in f.readlines()]
		except FileNotFoundError:
			self.banlist = []

		db.autosave(self.scheduler)
		super().__init__(
			command_prefix=get_prefix,
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
		)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"{cog} cog loaded")

		print ("Setup Complete, Initializing Bot And Cogs....")

	def update_db(self):
		db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
					 ((guild.id,) for guild in self.guilds))

		db.multiexec("INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
					 ((member.id,) for guild in self.guilds for member in guild.members if not member.bot))

		to_remove = []
		stored_members = db.column("SELECT UserID FROM exp")
		for id_ in stored_members:
			if not self.guild.get_member(id_):
				to_remove.append(id_)

		db.multiexec("DELETE FROM exp WHERE UserID = ?",
					 ((id_,) for id_ in to_remove))

		db.commit()

	def run(self, version):
		self.VERSION = version

		print("Running Setup...")
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("Running Bot...")
		super().run(self.TOKEN, reconnect=True)
	
	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if message.author.id in self.banlist:
				embed = Embed(description="**You are banned from using commands due to your immense gayness**", color=0xBC0808)
				await ctx.reply(embed=embed)

			elif not self.ready:
				await ctx.send("I'm not ready to receive commands. Have some patience gay ass. Wait for a while.")

			else:
				await self.invoke(ctx)

	async def rules_reminder(self):
		embed=Embed(description="**Dont be gay please**",color=embed_color)
		await self.config_channel.send(embed=embed)

	async def on_connect(self):
		print("Bot Is Connecting...")

	async def on_disconnect(self):
		print("Bot Disconnected...")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			embed = Embed(description="**Something went wrong because of gay boiz gayness**",color=embed_color)
			await args[0].send(embed=embed, delete_after=60)

		embed = Embed(description="**An error occurred due to gay boi**",color=embed_color)
		await self.config_channel.send(embed=embed)
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, NotOwner):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		elif isinstance(exc, MissingAnyRole):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

		elif isinstance(exc, DisabledCommand):
			embed = Embed(description="**That command is disabled for now, try again later**", color=0xffec00)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed, delete_after=60)
		
		elif isinstance(exc, RoleNotFound):
			embed = Embed(description="**That role does not exist**", color=0xffec00)
			await ctx.reply(embed=embed, delete_after=60)
			await ctx.message.delete(delay=15)
		
		elif any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass
		
		elif isinstance(exc, MissingRequiredArgument):
			embed=Embed(description="**One or more required arguments are missing, just like gay boiz straightness**",color=0xffec00)
			await ctx.reply(embed=embed, delete_after=60)
			await ctx.message.delete(delay=15)
		
		elif isinstance(exc, CommandOnCooldown):
			cd = round(exc.retry_after)
			minutes = str(cd // 60)
			seconds = str(cd % 60)
			embed=Embed(description=f"That command is on **{str(exc.cooldown.type).split('.')[-1]} cooldown**... Try again in **{minutes}:{seconds}**",color=0xffec00)
			await ctx.reply(embed=embed, delete_after=60)
			await ctx.message.delete(delay=15)
		
		elif hasattr(exc, "original"):
			# if isinstance(exc.original, HTTPException):
			# 	await ctx.send("Unable to send message.")

			if isinstance(exc.original, Forbidden):
				await ctx.message.delete(delay=15)
				await ctx.send("**I do not have permission to do that altough i am still admin\nFuck you gay boi**", delete_after=10)

			else:
				raise exc.original

		else:
			raise exc
	
	
	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(736258866504925306) #SERVER ID HERE
			self.config_channel = self.get_guild(795726142161944637).get_channel(819349982305189898) #CHANNEL ID HERR
			self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=0, minute=0, second=10))
			self.allowed_channels = (830188895374278686)
			self.scheduler.start()

			self.update_db()
			
			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			print("All Cogs Loaded...")
			print("Bot Is Online!")
			print("Setting Up Bot Status...")
			print("Bot Is Ready!")
			embed = Embed(description="**Now Online**", color=embed_color) 
			await self.config_channel.send(embed=embed, delete_after=60)
			self.ready = True

			#CUSTOM BOT STATUSES
			prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", self.guild.id)
			statuses = [f"With {len(self.guilds)} Servers",f"With {len(self.users)} Members", "With Your Mom", "With Other Bots" ,  f"{prefix}help" , "Join Chads' Den", "With Gay Mods", "ModMail", "Version 0.0.1", "Developed By Chad",
			"Join ESM丨CODM", "discord.gg/esm", "Follow res_codm On Insta", "Insta: res_codm"]
			while not self.is_closed():
				status = random.choice(statuses)
				
				await bot.change_presence(status =discord.Status.online ,activity=discord.Activity(type=discord.ActivityType.playing, name=status))

				await asyncio.sleep(10)

			self.loop.create_task(status())
			
		else:
			print("Something Went Wrong, Bot Is Reconnecting...")	
	
	#PING BOT
	async def on_message(self, message):
		# if self.user.mentioned_in(message) and message.content.startswith("<@830535") and message.content.endswith("919673147452>"):
		# 	if not self.user == message.author:
		# 		for channel in self.guild.channels:
		# 			if message.channel.id == (819349982305189898) or (771083740217999371):
		# 				prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
		# 				embed=Embed(title="<:RES_cheemsPimg:823612649098575872>  Ping?", color=0xBC0808, timestamp=datetime.utcnow())
		# 				fields = [("Prefix", f"My current prefix for this guild is `{prefix}`", False),
		# 					("Help", f"Need help? just use the `{prefix}help` command " , False),
		# 					("More Info", f"For more info about me, use the command `{prefix}info`" , False)]
		# 				for name , value, inline in fields:
		# 					embed.add_field(name=name, value=value, inline=inline)			
		# 				embed.set_footer(text=f"Requested By {message.author.display_name}", icon_url=message.author.avatar_url)
		# 				embed.set_thumbnail(url = self.guild.me.avatar_url)
		# 				await message.delete(delay=120)
		# 				return await message.channel.send(embed=embed, delete_after=120)
				
		# 			else:
		# 				print("Blacklisted Channel")
			
		#MODMAIL SYSTEM
		if not message.author.bot:
			if isinstance(message.channel, DMChannel):
				guild = bot.get_guild(736258866504925306)
				prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", guild.id)
				
				if message.content == f"{prefix}verify":
					embed = Embed(title="Verification Help",
						description="For verification, head out to <#751028101584125984> and react to the verification message!",
						color=0xBC0808)
					embed.set_image(url = "https://media.discordapp.net/attachments/842232322320629780/856250663288569866/this.gif?width=733&height=473")
					
					return await message.channel.send(embed=embed)
				
				if message.content.startswith(f"{prefix}modmail"):
					if len(message.content) > 9:
						if len(message.content) > 29:
							if len(message.content) < 2030:
								modmail = message.content[9:]
								this_embed = Embed(title="Modmail Confirmation",
									description=f"**Message count:** {len(message.content[9:])} characters \n **Please confirm if you want to send this message** \n\t {modmail} \n \n **Reply with either `Yes` or `No`**",
									color=0xBC0808)
								this_embed.set_thumbnail(url = f"{guild.icon_url}")

								questions = [this_embed]
								answers = []
								
								def check(m):
									return m.author == message.author and m.channel == message.channel
								
								for i in questions:
									that = await message.channel.send(embed=i)
								
									try:
										msg = await bot.wait_for('message', timeout=60, check=check)
									except asyncio.TimeoutError:
										embed = Embed(description="You didn\'t answer in the given time!\nPlease answer in under **60 seconds** next time!",color=0xBC0808)
										await message.channel.send(embed = embed)
										return
									
									answers.append(msg.content)

								if answers[0] == "Yes" or answers[0] == "yes":
									embed = Embed(title="Modmail Received",
										description=f"**Message by {message.author.mention}丨{message.author.name}#{message.author.discriminator}** \n {modmail}",
										color=0xBC0808,
										timestamp=datetime.utcnow())
									embed.set_thumbnail(url = f"{message.author.avatar_url}")
									modmail_channel = self.get_guild(736258866504925306).get_channel(830567374180319263)
									await modmail_channel.send(embed=embed)
									
									embed = Embed(description="<a:Check:856282490670284802> **Your message has been relayed to moderators!**",
										color=0xBC0808)
									return await that.edit(embed=embed)
								
								else:
									ok = await message.channel.send("mf", delete_after=2)
									embed = Embed(description="**Process has been canceled successfully**", color=0xBC0808)
									await message.channel.send(embed = embed)
									return

							else:
								await message.channel.send("<:RES_cheemsThiccMhm:823612526775238666>")
								return await message.channel.send("Nice presidential debate")
						else:
							await message.channel.send("<a:pepe_seizure:790992973096812594>")
							return await message.channel.send("Your message needs to be at least **20** characters in length...")
					else:
						return await message.channel.send("Try providing a message next time?")

				if message.content == f"{prefix}apply":
					return await message.channel.send(":x: Applications are currently closed!")
				
				if message.content == f"{prefix}help":
					embed = Embed(title="<a:pet:801495732233961492> Help",
								description="",
								color=0xBC0808)
					embed.set_thumbnail(url = f"{guild.icon_url}")
					embed.set_footer(text="This message will auto-delete after 15 min")
					fields = [("Verification", f"For verification help, use the following syntax: \n ```{prefix}verify```" , False),
								("ModMail", f"For sending a modmail, use the following syntax: \n ```{prefix}modmail (Your message here)```" , False),
								("RES Recruitment", f"To send an application, use the following syntax: \n ```{prefix}apply```" , False)]
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					
					return await message.channel.send(embed = embed, delete_after=900)

				if "Hello" in message.content or "hello" in message.content or "Hi" in message.content or "hi" in message.content:
					return await message.channel.send(f"Look who slid into my dms :wink: \n Use `{prefix}help` for help")

			else:
				await self.process_commands(message)

bot = Bot()