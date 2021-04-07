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

# |CUSTOM|
embed_color = 0x000000
server_logo = "https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png"
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

		self.guild = None
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
				embed = Embed(description="**You are banned from using commands**", color=0x000000)
				await ctx.reply(embed=embed)

			elif not self.ready:
				await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

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
			embed = Embed(description="**Something went wrong!**",color=embed_color)
			await args[0].send(embed=embed, delete_after=60)

		embed = Embed(description="**An error occurred!**",color=embed_color)
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
			embed=Embed(description="**One or more required arguments are missing!**",color=0xffec00)
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
				await ctx.send("**I do not have permission to do that**", delete_after=10)

			else:
				raise exc.original

		else:
			raise exc
	
	
	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(803028981698789407) #SERVER ID HERE
			self.config_channel = self.get_channel(826442024927363072) #CHANNEL ID HERE
			self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=0, minute=0, second=10))
			self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)
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
			statuses = ["Chad Stuff",f"{len(self.guilds)} Servers",f"{len(self.users)} Members", "Over Ghost Pings", "Over Other Bots" ,  "?help" , "Over Chads' Den", "Over The Mods", "ModMail", "Version 0.0.1", "Developed By Chad", "Chads","The World Burn", "9/11",
			"Join ESM丨CODM", "Join RES", "discord.gg/esm"]
			while not self.is_closed():
				status = random.choice(statuses)
				
				await bot.change_presence(status=discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name=status))

				await asyncio.sleep(10)

			self.loop.create_task(status())
			
		else:
			print("Something Went Wrong, Bot Is Reconnecting...")	
	
	#PING BOT
	async def on_message(self, message):
		if self.user.mentioned_in(message) and message.content.startswith("<") and message.content.endswith(">"):
			if not self.user == message.author:
				if message.channel.id == (803031892235649044) or (803033569445675029):
					prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
					embed=Embed(title="<:cheemsThink:821795532385157173> You Pinged Me", color=0x000000, timestamp=datetime.utcnow())
					fields = [("Prefix", f"My current prefix for this guild is `{prefix}`", False),
						("Tip", "If you dont remember my prefix, you can mention me with the comand instead! \nFor example, ```@CHAD丨BӨT#9795 help - @CHAD丨BӨT#9795 flip```" , False),
						("Help", "Need help? just use the `?help` command " , False),
						("More Info", "For more info about me, use the command `?info`" , False)]
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)			
					embed.set_footer(text=f"Requested By {message.author.display_name}", icon_url=message.author.avatar_url)
					embed.set_thumbnail(url=server_logo)
					await message.delete(delay=120)
					await message.channel.send(f"||{message.author.mention}||",embed=embed, delete_after=120)
				
				else:
					embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention} **Is blacklisted for pings, please ping me in <#803031892235649044> instead**", color=0x000000)
					await ctx.reply(embed=embed)	
			
		#MODMAIL SYSTEM
		if not message.author.bot:
			if isinstance(message.channel, DMChannel):
				if len(message.content) < 40:
					embed= Embed(title="ModMail Error", description=":exclamation: Your message needs to be **atleast 40** characters in length\n Refrain from spamming and abusing the ModMail system", color=0x000000)
					await message.channel.send(embed=embed)

				else:			
					embed=Embed(title="New ModMail Received", color=0xfd0000, timestamp=datetime.utcnow())
					embed.set_thumbnail(url=message.author.avatar_url)
						
					fields = [("Message By", f"{message.author.mention} __**AKA**__ {message.author.display_name}", False),
						("Message Content",message.content, False)]
					
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					
					mod_channel = self.get_channel(823133054078943272) #YOUR CHANNEL HERE
					await mod_channel.send(embed=embed)
					embed= Embed(title=":white_check_mark: ModMail Sent Successfully",color=0x000000)
					fields = [("Message Sent", "Your message has been relayed to moderators. \nWe will get back to you shortly", False),
						("ModMail Abuse",":exclamation: Refrain from abusing and spamming ModMail system or it will result in a mute", False),
						("Notice",":exclamation: Attachments such as images, files and videos are not supported **yet** in the ModMail system", False)]
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)					
					await message.channel.send(embed=embed)

			else:
				await self.process_commands(message)

bot = Bot()