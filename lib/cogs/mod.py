import aiofiles
import discord
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import has_permissions, bot_has_permissions
from discord import Embed, Member
from datetime import datetime, timedelta
from typing import Optional
from discord.ext.commands import command
from ..db import db
from asyncio import sleep
from re import search
from better_profanity import profanity
import asyncio
from discord.ext.commands import has_role
profanity.load_censor_words_from_file("./data/profanity.txt")
import re
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
from discord.errors import Forbidden

class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.links_allowed = [(830188895374278686)]
		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		self.images_allowed = (830188895374278686)
		self.ping_not_allowed_channels = (827960572330377233,759470480981229598,822428365351944214,761567095133306880,822428198989725727,830567374180319263,751057537280901162)
		self.allowed_channels = (830188895374278686,771083740217999371)
	
	#KICK COMMAND
	@command(name="kick", brief="Kick Members", help="Kicks members from the current guild.", hidden=True)
	@bot_has_permissions(kick_members=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def kick_members(self, ctx, targets: Greedy[Member], * , reason: Optional[str] = "No reason provided."):
		guild = self.bot.get_guild(736258866504925306)
		if not len(targets):
			embed=Embed(title="Kick",description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
			
			fields = [("Syntax", "```?kick | @member | reason```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
			
		for target in targets:
			if target == guild.me:
	  			embed = Embed(description="**:x: You cannot kick the bot**", color=0xffec00)
	  			message = await ctx.reply(embed=embed,delete_after=10)
	  			await ctx.message.delete(delay=15)
	  			return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
			
			elif target == ctx.author:
				embed = Embed(description="**:x: You cannot kick yourself**", color=0xffec00)
				message = await ctx.reply(embed=embed, delete_after=10)
				await ctx.message.delete(delay=15)
				return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
			
			else:
				for target in targets:
					if (ctx.author.top_role.position >= target.top_role.position
						and not target.guild_permissions.administrator):
						
						try:

							target_embed= Embed(title="Kick Report", description=f"You have been **kicked** from {target.guild.name}\n**Reason:** {reason}", color=0xBC0808)
							await target.send(embed=target_embed)
						
						except Forbidden:
							pass
						
						await target.kick(reason=reason)
						embed=Embed(title="Member Kicked", color=0xff0000, timestamp=datetime.utcnow())
						embed.set_thumbnail(url=target.avatar_url)
						fields = [("Member", f"{target.mention} __**AKA**__ {target.display_name}", False),
								("Actioned By", f"{ctx.author.mention} __**AKA**__ {ctx.author.display_name}" , False),
								("Reason", reason , False)]
						for name , value, inline in fields:
							embed.add_field(name=name, value=value, inline=inline)
						await self.mod_log_channel.send(embed=embed)
						
						embed=Embed(description=f"***:white_check_mark: {target.display_name} has been kicked***.", color=0x43b581)
						await ctx.message.delete()
						await ctx.send(embed=embed)		
						
					else:
						await ctx.message.delete(delay=15)
						embed=Embed(title="Task Unsuccessful", description=f":x: **You are unable to kick {target.display_name}**", color=0xffec00)
						await ctx.message.delete(delay=15)
						await ctx.reply(embed=embed,delete_after=10)
	

	#BAN COMMAND
	@command(name="ban", brief="Ban Members", help="Bans members from the current guild.", hidden=True)
	@bot_has_permissions(ban_members=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def ban_members(self, ctx, targets: Greedy[Member], * , reason: Optional[str] = "No reason provided."):
		guild = self.bot.get_guild(736258866504925306)
		if not len(targets):
			embed=Embed(title="Ban",description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
			
			fields = [("Syntax", "```?ban | @member | reason```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
		
		for target in targets:
			if target == guild.me:
	  			embed = Embed(description="**:x: You cannot ban the bot**", color=0xffec00)
	  			message = await ctx.reply(embed=embed,delete_after=10)
	  			await ctx.message.delete(delay=15)
	  			return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
			
			elif target == ctx.author:
				embed = Embed(description="**:x: You cannot ban yourself**", color=0xffec00)
				message = await ctx.reply(embed=embed, delete_after=10)	
				await ctx.message.delete(delay=15)
				return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
			
			else:
				for target in targets:
						if (ctx.author.top_role.position >= target.top_role.position
							and not target.guild_permissions.administrator):
							
							try:
							
								embed= Embed(title="Ban Report", description=f"You have been **banned** from {target.guild.name}\n**Reason:** {reason}", color=0xBC0808)
								await target.send(embed=embed)
							
							except Forbidden:
								pass
							
							await target.ban(reason=reason)
							embed=Embed(title="Member Banned", color=0xff0000, timestamp=datetime.utcnow())
							embed.set_thumbnail(url=target.avatar_url)
							fields = [("Member", f"{target.mention} __**AKA**__ {target.display_name}", False),
									("Actioned By",f"{ctx.author.mention} __**AKA**__ {ctx.author.display_name}" , False),
									("Reason", reason , False)]
							for name , value, inline in fields:
								embed.add_field(name=name, value=value, inline=inline)
							await self.mod_log_channel.send(embed=embed)
							
							embed=Embed(description=f"***:white_check_mark: {target.display_name} has been banned***.", color=0x43b581)
							await ctx.message.delete()
							await ctx.send(embed=embed)
						
						else:
							embed=Embed(title="Task Unsuccessful", description=f":x: **You are unable to ban {target.display_name}**.", color=0xffec00)
							await ctx.message.delete(delay=15)
							await ctx.reply(embed=embed,delete_after=10)
	

	#PURGE COMMAND
	@command(name="purge", brief="Purge Messages",help="Deletes optional number of messages.", hidden=True)
	@bot_has_permissions(manage_messages=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def clear_messages(self, ctx, limit: Optional[int] = 10):
		with ctx.channel.typing():
			await ctx.message.delete()
			deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14))
			embed=Embed(title="Action Successful", description=f":white_check_mark: Successfully deleted **{len(deleted):,}** messages.", color=0x43b581)
			await ctx.send(embed=embed, delete_after=3)


	#MUTE COMMAND
	@command(name="mute", brief="Mute Members", help="Mutes members for a specific amount of time in the guild." ,hidden=True)
	@bot_has_permissions(manage_roles=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def mute_members(self, ctx, targets: Greedy[Member], minutes: Optional[int], *, reason: Optional[str] = "No reason provided"):
		guild = self.bot.get_guild(736258866504925306)
		if not len(targets):
			embed=Embed(title="Mute",description=":x: One or more arguments are missing, use the below provided syntax.", color=0xffec00)
			fields = [("Syntax", "```?mute <targets> [minutes] [reason]```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)

		for target in targets:
			if target == guild.me:
	  			embed = Embed(description="**:x: You cannot mute the bot**", color=0xffec00)
	  			message = await ctx.reply(embed=embed, delete_after=10)
	  			await ctx.message.delete(delay=15)
	  			return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
			
			elif target == ctx.author:
				embed = Embed(description="**:x: You cannot mute yourself**", color=0xffec00)
				message = await ctx.reply(embed=embed, delete_after=10)	
				await ctx.message.delete(delay=15)
				return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
			
			else:
				unmutes = []

				for target in targets:
					if not self.mute_role in target.roles:
						if ctx.author.top_role.position >= target.top_role.position:
							role_ids = ",".join([str(r.id) for r in target.roles])
							end_time = datetime.utcnow() + timedelta(minutes=minutes) if minutes else None

							db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
										target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())

							await target.edit(roles=[self.mute_role])
							embed=Embed(title="Member Muted", color=0xff0000, timestamp=datetime.utcnow())
							embed.set_thumbnail(url=target.avatar_url)
							
							fields = [("Member", f"{target.mention} __**AKA**__ {target.display_name}", False),
								("Actioned By",f"{ctx.author.mention} __**AKA**__ {ctx.author.display_name}" , False),
								("Duration",f"{minutes:,} minute(s)" if minutes else "Indefinite", False),
								("Reason", reason , False)]
							for name , value, inline in fields:
								embed.add_field(name=name, value=value, inline=inline)
							await self.mod_log_channel.send(embed=embed)
							
							try:
								embed= Embed(title="Mute Report", description=f"You have been **muted** in {target.guild.name}\n**Reason:** {reason}", color=0xBC0808)
								await target.send(embed=embed)
							
							except Forbidden:
								pass
							
							embed=Embed(description=f":white_check_mark: ***{target.display_name} has been muted***.", color=0x43b581)
							await ctx.send(ctx.author.mention,embed=embed)
							await self.gulag_channel.send(f"**Welcome to the gulag {target.mention} \n If you survive you earn you freedom\n ||Tag any @RES | Moderater or @RES | Staff to be freed||**")
							if minutes:
								unmutes.append(target)
						
						else:
							embed=Embed(title="Task Unsuccessful", description=f":x: **You are unable to mute {target.display_name}**.", color=0xffec00)
							await ctx.message.delete(delay=15)
							await ctx.reply(embed=embed,delete_after=10)

					else:
						embed=Embed(title="Task Unsuccessful", description=f":x: **{target.display_name} is already muted**", color=0xffec00)
						await ctx.message.delete(delay=15)
						await ctx.reply(embed=embed,delete_after=10)

				
				if len(unmutes):
					await sleep(minutes*60)
					await self.unmute(ctx, targets)								

	
	async def unmute(self, ctx, targets, *, reason="Mute time expired."):
		for target in targets:
			if target != self.bot or ctx.author:
				if self.mute_role in target.roles:
					role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
					roles = [ctx.guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

					db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

					await target.edit(roles=roles)
					embed=Embed(title="Member Unmuted", color=0x11ff00, timestamp=datetime.utcnow())
					embed.set_thumbnail(url=target.avatar_url)
							
					fields = [("Member", f"{target.mention} __**AKA**__ {target.display_name}", False),
					("Reason", reason , False)]
					
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					await self.mod_log_channel.send(embed=embed)
					
					try:

						embed= Embed(title="Unmute Report", description=f"You have been **unmuted** in {target.guild.name}\n**Reason:** {reason}", color=0xBC0808)
						await target.send(embed=embed)
					
					except Forbidden:
						pass

					embed=Embed(description=f":white_check_mark: ***{target.display_name} has been unmuted***.", color=0x43b581)
					await ctx.message.delete()
					await ctx.send(embed=embed)
				
				else:
					embed=Embed(title="Task Unsuccessful", description=f":x: **{target.display_name} is already Unmuted**", color=0xffec00)
					await ctx.message.delete(delay=15)
					await ctx.reply(embed=embed,delete_after=10)
			else:
				embed = Embed(description="**You cannot kick yourself or the bot**", color=0xBC0808)
				await ctx.reply(embed=embed, delete_after=10)
				await ctx.message.delete(delay=15)
	
	#UNMUTE COMMAND
	@command(name="unmute", brief="Unmute Members", help="Unmutes members which were muted previously", hidden=True)
	@bot_has_permissions(manage_roles=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def unmute_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided"):
			if not len(targets):
				embed=Embed(title="Unmute",description=":x: One or more arguments are missing, use the below provided syntax.", color=0xffec00)
				fields = [("Syntax", "```unmute <targets> [reason]```", False)]
				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				await ctx.message.delete(delay=15)
				await ctx.reply(embed=embed,delete_after=10)

			else:
				await self.unmute(ctx, targets, reason=reason)

	
#	#ADD BLACKLIST WORDS COMMAND
#	@command(name="addprofanity", brief="Add Blacklisted Words", help="Adds blacklisted words for the current guild", hidden=True)
#	@has_any_role(806886607541633045)
#	async def add_profanity(self, ctx, *words):
#		with open("./data/profanity.txt", "a",encoding="utf-8") as f:
#			f.write("".join([f"{w}\n" for w in words]))
#		
#		profanity.load_censor_words_from_file("./data/profanity.txt")
#		
#		embed=Embed(title="Blacklist Words Added", description=":white_check_mark: Blacklist words have been successfully added. \n**Warn dialog will appear for confirmation.**", color=0x43b581)
#		await ctx.reply(embed=embed)	
#
#	
#	#DELETE BLACKLISTED WORDS COMMAND
#	@command(name="delprofanity", brief="Remove Blacklisted Words", help="Removes blacklisted words for the current guild",hidden=True)	
#	@has_any_role(806886607541633045)
#	async def remove_profanity(self, ctx, *words):
#		with open("./data/profanity.txt", "r", encoding="utf-8") as f:
#			stored = [w.strip() for w in f.readlines()]
#		
#		with open("./data/profanity.txt", "w",encoding="utf-8") as f:
#			f.write("".join([f"{w}\n" for w in stored if w not in words]))	
#		
#		profanity.load_censor_words_from_file("./data/profanity.txt")
#		
#		embed=Embed(title="Blacklist Words Removed.", description=":white_check_mark: Blacklist words have been successfully removed.", color=0x43b581)
#		await ctx.reply(embed=embed)	
#
#
#	#PROFANITY DETECTION
#	@Cog.listener()		
#	async def on_message(self, message):
#		if not message.author.bot:
#			if profanity.contains_profanity(message.content):
#				await message.delete()
#				embed=Embed(title="Blacklisted Word Found", description=f"**{message.author.display_name}** that word is blacklisted", color=0xff0000)
#				await message.channel.send(message.author.mention, delete_after=10)
#				await message.channel.send(embed=embed, delete_after=10)
#       
	
	@Cog.listener()	
	async def on_message_delete(self, message):
		guild = self.bot.get_guild(736258866504925306)
		if message.mentions and not message.content.startswith("?"):
			guild = self.bot.get_guild(736258866504925306)
			if not message.author == guild.me:
				for role in message.author.roles:
					if role in self.allowed_roles:
						return
				
				for channel in guild.channels:
					if message.channel.id in self.ping_not_allowed_channels:
						return
				for s in message.mentions:
					channel_embed=Embed(title="<:RES_cheemsPimg:823612649098575872> Ghost Ping Detected",
						description=f"**{s.mention} was ghost pinged by {message.author.mention}**",
						color=0xBC0808, 
						timestamp=datetime.utcnow())
					fields = [("Message", f"{message.content}", False)]
					for name, value, inline in fields:
						channel_embed.add_field(name=name, value=value, inline=inline)
					await message.channel.send(embed=channel_embed)
					log_embed=Embed(title="Ghost Ping",color=0xff0000, timestamp=datetime.utcnow())
					log_embed.set_thumbnail(url=f"{message.author.avatar_url}")
					fields = [("By", f"{message.author.name}#{message.author.discriminator}", True),
							("To", f"{s.name}#{s.discriminator}", False),
							("Channel", message.channel.mention , True),
							("Message", message.content , False)]
					for name, value, inline in fields:
						log_embed.add_field(name=name, value=value, inline=inline)
					await self.log_channel.send(embed=log_embed)

		
		#SNIPE COMMAND	
		global snipe_message_content
		global snipe_message_author
		global snipe_message_author_url
		global snipe_message_author_discriminator 
		
		snipe_message_content = message.content
		snipe_message_author = message.author.name
		snipe_message_author_url = message.author.avatar_url
		snipe_message_author_discriminator = message.author.discriminator
		await asyncio.sleep(120)
		snipe_message_author = None
		snipe_message_content = None
	
	@command(name="snipe",brief="Snipe Messages",help="Displays the most recent deleted message by any user in the guild",hidden=True)
	async def snipe(self, message):
		if message.author.bot or snipe_message_content == None:
			embed=Embed(description="**Nothing to snipe!**", color=0xBC0808)
			await message.channel.send(embed=embed)
		else:
			embed=Embed(description=f"{snipe_message_content}", color=0xBC0808)
			embed.set_footer(text=f"Requested By {message.author.display_name}", icon_url=message.author.avatar_url)
			embed.set_author(name=f"{snipe_message_author}#{snipe_message_author_discriminator}", icon_url=f"{snipe_message_author_url}")		
			await message.channel.send(embed=embed, delete_after=60)
			return

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.log_channel = self.bot.get_guild(736258866504925306).get_channel(761567095133306880) #YOUR CHANNEL HERE
			self.mute_role = self.bot.get_guild(736258866504925306).get_role(803885096666005514)  #MUTE ROLE HERE
			self.role = self.bot.get_guild(736258866504925306).get_role(751028081233494107)  #COMMUNITY ROLE HERE
			self.mod_log_channel = self.bot.get_channel(822428198989725727)
			self.allowed_roles = [self.bot.get_guild(736258866504925306).get_role(810854901055225907),self.bot.get_guild(736258866504925306).get_role(751028067446554704),self.bot.get_guild(736258866504925306).get_role(776069302045769759),self.bot.get_guild(736258866504925306).get_role(806886607541633045),self.bot.get_guild(736258866504925306).get_role(772521546191208488)]
			self.gulag_channel = self.bot.get_channel(751057537280901162)
			self.bot.cogs_ready.ready_up("mod")
			
def setup(bot):
	bot.add_cog(Mod(bot))