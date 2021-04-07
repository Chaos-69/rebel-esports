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
		self.links_allowed = [(818451301440028686)]
		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		self.images_allowed = (818451301440028686)
		self.ping_allowed_channels = (803028981698789410,816818936082989066,818530424196169759,818934074835730463,803143531405377557,804682925945520138,826442024927363072)
		self.allowed_channels = (827297851116748871 ,803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)
	
	#KICK COMMAND
	@command(name="kick", brief="Kick Members", help="Kicks members from the current guild.", hidden=True)
	@bot_has_permissions(kick_members=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def kick_members(self, ctx, targets: Greedy[Member], * , reason: Optional[str] = "No reason provided."):
		guild = self.bot.get_guild(803028981698789407)
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

							target_embed= Embed(title="Kick Report", description=f"You have been **kicked** from {target.guild.name} due to __**{reason}**__", color=0x000000)
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
	
	@kick_members.error
	async def kick_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
	

	#BAN COMMAND
	@command(name="ban", brief="Ban Members", help="Bans members from the current guild.", hidden=True)
	@bot_has_permissions(ban_members=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def ban_members(self, ctx, targets: Greedy[Member], * , reason: Optional[str] = "No reason provided."):
		guild = self.bot.get_guild(803028981698789407)
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
							
								embed= Embed(title="Ban Report", description=f"You have been **banned** from {target.guild.name} due to __**{reason}__**", color=0xff0000)
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
	
	@ban_members.error
	async def ban_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
	

	#PURGE COMMAND
	@command(name="purge", brief="Purge Messages",help="Deletes optional number of messages.", hidden=True)
	@bot_has_permissions(manage_messages=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def clear_messages(self, ctx, limit: Optional[int] = 10):
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14))
				embed=Embed(title="Action Successful", description=f":white_check_mark: Successfully deleted **{len(deleted):,}** messages.", color=0x43b581)
				await ctx.send(embed=embed, delete_after=3)
	
	@clear_messages.error
	async def clear_messages_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
	


	#MUTE COMMAND
	@command(name="mute", brief="Mute Members", help="Mutes members for a specific amount of time in the guild." ,hidden=True)
	@bot_has_permissions(manage_roles=True)
	@has_any_role('Chad', 'Admin', 'Executive', 'Management', 'Moderator')
	async def mute_members(self, ctx, targets: Greedy[Member], minutes: Optional[int], *, reason: Optional[str] = "No reason provided"):
		guild = self.bot.get_guild(803028981698789407)
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
								embed= Embed(title="Mute Report", description=f"You have been **muted** in {target.guild.name} due to __**{reason}**__", color=0xff0000)
								await target.send(embed=embed)
							
							except Forbidden:
								pass
							
							embed=Embed(description=f":white_check_mark: ***{target.display_name} has been muted***.", color=0x43b581)
							await ctx.message.delete()
							await ctx.send(ctx.author.mention,embed=embed)
							await self.gulag_channel.send(f"**Welcome to the gulag\nBeg for mercy now.\nIf you are confused, head out to <#829062770309070908>\n||{target.mention}||**")
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

	@mute_members.error
	async def mute_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)				

	
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

						embed= Embed(title="Unmute Report", description=f"You have been **unmuted** in {target.guild.name} due to **{reason}**", color=0x11ff00)
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
				embed = Embed(description="**You cannot kick yourself or the bot**", color=0x000000)
				await ctx.reply(embed=embed, delete_after=10)
				await ctx.message.delete(delay=15)
	
	#UNMUTE COMMAND
	@command(name="unmute", brief="Unmute Members", help="Unmutes members which were muted previously", hidden=True)
	@bot_has_permissions(manage_roles=True)
	@has_any_role('Chad', 'Admin', 'Executive', 'Management', 'Moderator')
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
	
	@unmute_members.error
	async def unmute_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

	
	#ADD BLACKLIST WORDS COMMAND
	@command(name="addprofanity", brief="Add Blacklisted Words", help="Adds blacklisted words for the current guild", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def add_profanity(self, ctx, *words):
		with open("./data/profanity.txt", "a",encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))
		
		profanity.load_censor_words_from_file("./data/profanity.txt")
		
		embed=Embed(title="Blacklist Words Added", description=":white_check_mark: Blacklist words have been successfully added. \n**Warn dialog will appear for confirmation.**", color=0x43b581)
		await ctx.reply(embed=embed)	

	@add_profanity.error
	async def add_profanity_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
	
	#DELETE BLACKLISTED WORDS COMMAND
	@command(name="delprofanity", brief="Remove Blacklisted Words", help="Removes blacklisted words for the current guild",hidden=True)	
	@has_any_role('Chad', 'Admin', 'Executive')
	async def remove_profanity(self, ctx, *words):
		with open("./data/profanity.txt", "r", encoding="utf-8") as f:
			stored = [w.strip() for w in f.readlines()]
		
		with open("./data/profanity.txt", "w",encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in stored if w not in words]))	
		
		profanity.load_censor_words_from_file("./data/profanity.txt")
		
		embed=Embed(title="Blacklist Words Removed.", description=":white_check_mark: Blacklist words have been successfully removed.", color=0x43b581)
		await ctx.reply(embed=embed)	
	
	@remove_profanity.error
	async def remove_profanity_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

	#PROFANITY DETECTION
	@Cog.listener()		
	async def on_message(self, message):
		if not message.author.bot:
			if profanity.contains_profanity(message.content):
				await ctx.message.delete()
				embed=Embed(title="Blacklisted Word Detected", description=f"<:D_stopOfficer:820756718648688660> **{message.author.display_name}** watch your language.", color=0xff0000)
				await message.channel.send(message.author.mention)
				await message.channel.send(embed=embed, delete_after=10)
        
	
	@Cog.listener()	
	async def on_message_delete(self, message):
		guild = self.bot.get_guild(803028981698789407)
		if message.mentions and not message.content.startswith("?"):
			guild = self.bot.get_guild(803028981698789407)
			if not message.author == guild.me:
				for role in message.author.roles:
					if role in self.allowed_roles:
						return
				
				for channel in guild.channels:
					if not message.channel.id in self.ping_allowed_channels:
						return
				
				channel_embed=Embed(title="<:cheemsGun:821807384246353981> Ghost Ping Detected", description=f"{message.content}", color=0x000000, timestamp=datetime.utcnow())
				channel_embed.set_footer(text=f"By {message.author.name}#{message.author.discriminator}",icon_url=f"{message.author.avatar_url}")
				await message.channel.send(embed=channel_embed, delete_after=10)
				log_embed=Embed(title="Ghost Ping",color=0xff0000, timestamp=datetime.utcnow())
				log_embed.set_thumbnail(url=f"{message.author.avatar_url}")
				fields = [("By", f"{message.author.name}#{message.author.discriminator}", True),
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
		await asyncio.sleep(60)
		snipe_message_author = None
		snipe_message_content = None
	
	@command(name="snipe",brief="Snipe Messages",help="Displays the most recent deleted message by any user in the guild",hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def snipe(self, message):
		if message.author.bot or snipe_message_content == None:
			embed=Embed(description="**Nothing to snipe!**", color=0x000000)
			await message.channel.send(embed=embed)
		else:
			embed=Embed(description=f"{snipe_message_content}", color=0x000000)
			embed.set_footer(text=f"Requested By {message.author.display_name}", icon_url=message.author.avatar_url)
			embed.set_author(name=f"{snipe_message_author}#{snipe_message_author_discriminator}", icon_url=f"{snipe_message_author_url}")		
			await message.channel.send(embed=embed, delete_after=60)
			return
	
	@snipe.error
	async def snipe_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
	

	#ROLES COMMAND
	@command(name="roles", brief="Roles Command", help="List all the roles present in the guild", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def roles(self, ctx):
		roles = [role for role in reversed(ctx.guild.roles[1:])]
		embed = Embed(title=f"All Roles in {ctx.guild} [{len(roles)}]",description=(" \n ".join(([role.mention for role in roles]))), color=0x000000)
		await ctx.message.delete(delay=15)
		await ctx.send(embed =embed, delete_after=60)

	@roles.error
	async def roles_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.log_channel = self.bot.get_guild(803028981698789407).get_channel(803038174057070602) #YOUR CHANNEL HERE
			self.mute_role = self.bot.get_guild(803028981698789407).get_role(803137120079839243)  #MUTE ROLE HERE
			self.role = self.bot.get_guild(795726142161944637).get_role(818950383216623696)  #COMMUNITY ROLE HERE
			self.mod_log_channel = self.bot.get_channel(816751322581303306)
			self.allowed_roles = [self.bot.get_guild(803028981698789407).get_role(818242893805912067), self.bot.get_guild(803028981698789407).get_role(803033298128338997), self.bot.get_guild(803028981698789407).get_role(803035805848436776)]
			self.gulag_channel = self.bot.get_channel(804682925945520138)
			self.bot.cogs_ready.ready_up("mod")
			
def setup(bot):
	bot.add_cog(Mod(bot))