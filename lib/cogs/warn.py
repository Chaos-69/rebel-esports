import discord
import aiofiles
from discord.ext.commands import Cog
from discord.ext.commands import command,has_permissions, MissingPermissions, has_any_role
from typing import Optional
from discord import Embed
from discord.ext.commands import CheckFailure
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
from datetime import datetime
import datetime as dt

class Warn(Cog):
	def __init__(self, bot):
		self.bot = bot
		intents = discord.Intents.default()
		intents.members = True
		self.warnings = {}
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)

	
	@Cog.listener()
	async def on_ready(self):
		self.bot.cogs_ready.ready_up("warn")
		for guild in self.bot.guilds:
			self.warnings[guild.id] = {}
			self.mod_log_channel = self.bot.get_channel(816751322581303306)
			for guild in self.bot.guilds:

				async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
					pass

				async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
					lines = await file.readlines()

					for line in lines:
						data = line.split(" ")
						member_id = int(data[0])
						admin_id = int(data[1])
						reason = " ".join(data[2:]).strip("\n")
						time = datetime.utcnow()

						try:
							self.warnings[guild.id][member_id][0] += 1
							self.warnings[guild.id][member_id][1].append((admin_id, reason, time))

						except KeyError:
							self.warnings[guild.id][member_id] = [1, [(admin_id, reason, time)]]
	
	@Cog.listener()
	async def on_guild_join(self, guild):
		self.warnings[guild.id] = {}


    #WARN COMMAND
	@command(name="warn", brief="Warn Command", help="Warns users and adds it to the user profile", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive', 'Management', 'Moderator')
	async def warn(self, ctx, member: discord.Member=None, *, reason: Optional[str] = "No reason provided"):
		if member is None:
			embed = Embed(title="Warn", description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
			fields = [("Syntax", "```?warn <target> [reason]```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)			
			return await ctx.reply(embed=embed,delete_after=10)

		try:
			first_warning = False
			for time in self.warnings:
				time = datetime.utcnow()
			self.warnings[ctx.guild.id][member.id][0] += 1
			self.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason, time))

		except KeyError:
			first_warning = True
			for time in self.warnings:
				time = datetime.utcnow()
			self.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason, time)]]

		count = self.warnings[ctx.guild.id][member.id][0]

		async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
			await file.write(f"{member.id} {ctx.author.id} {reason} {time}\n")
		embed = Embed(description=f"***{member.mention} has been warned***", color=0xff0000)
		await ctx.send(embed=embed, delete_after=120)
		member_embed= Embed(title="Warn Report", description=f"You have been **warned** in {member.guild.name} due to __**{reason}**__", color=0xff0000)
		await member.send(embed=member_embed)

		embed=Embed(title="Member Warned", color=0xff0000, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
		
		fields = [("Member", f"{member.mention} __**AKA**__ {member.display_name}", False),
			("Actioned By",f"{ctx.author.mention} __**AKA**__ {ctx.author.display_name}" , False),
			("Reason", reason , False)]
		for name , value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await self.mod_log_channel.send(embed=embed)
	
	@warn.error
	async def warn_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.reply(embed=embed,delete_after=10)

    #WARNINGS COMMAND
	@command(name="warnings", brief="Check Warnings Command",help="Displays all of the users warnings", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive', 'Management', 'Moderator')
	async def warnings(self, ctx, member: discord.Member=None):
		if member is None:
			embed = Embed(title="Warnings", description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
			fields = [("Syntax", "```?warnings <target>```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)			
			await ctx.reply(embed=embed,delete_after=10)	    		
		
		try:
			count = self.warnings[ctx.guild.id][member.id][0]
			
			embed = discord.Embed(title=f"Warnings For {member.name} [{count}] ", description="", colour=0xff0000)
			i = 1
			for admin_id, reason, time in self.warnings[ctx.guild.id][member.id][1]:
				admin = ctx.guild.get_member(admin_id)
				time = time
				embed.description += f"**__Warning {i}__** \n**Moderator**:- {admin.mention}  \n**Reason**:- `{reason}`\n**Time**:- {time.strftime('%d/%m/%Y')} \n \n"
				i += 1
				embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
			await ctx.reply(embed=embed)

		except KeyError:
			embed = Embed(description="**This user has no warnings**", color=0x000000)
			await ctx.reply(embed=embed,delete_after=10)

	@warnings.error
	async def warnings_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.reply(embed=embed,delete_after=10)
	
	#DELETE WARN COMMAND
	@command(name="delwarn", brief="Delete Warn Command", help="Deletes previously added warnings for users", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive', 'Management', 'Moderator')
	async def del_warn(self, ctx, member: discord.Member=None, index=None):
		index = int(index) - 1

		if index > len(self.warnings[ctx.guild.id][member.id]) and index is not None:
			embed = Embed(description="**Bad Index Given**", color=0x000000)
			return await ctx.reply(embed=embed,delete_after=10)
		
		else:
			self.warnings[ctx.guild.id][member.id][0] -= 1
			self.warnings[ctx.guild.id][member.id][1].pop(index)
		
			async with aiofiles.open(str(ctx.guild.id)+".txt", mode="w") as file:
				for member_id in self.warnings[ctx.guild.id]:
					count, data = self.warnings[ctx.guild.id][member_id]
					for admin_id, reason, time in data:
						admin = ctx.guild.get_member(admin_id)
						time = time
						await file.write(f"{member_id} {admin_id} {reason} {time}\n")
						embed=Embed(title="Member Warn Removed", color=0xff0000, timestamp=datetime.utcnow())
						embed.set_thumbnail(url=member.avatar_url)
						
						fields = [("Member", f"{member.mention} __**AKA**__ {member.display_name}", False),
								("Actioned By",f"{admin.mention} __**AKA**__ {admin.display_name}" , False)]
						for name , value, inline in fields:
							embed.add_field(name=name, value=value, inline=inline)
						await self.mod_log_channel.send(embed=embed)
						member_embed= Embed(title="Warn Report", description=f"Your warn has been **removed** in {member.guild.name}", color=0xff0000)
						await member.send(embed=member_embed)
						embed = Embed(description=f"***Warning removed for {member.mention}***", color=0x000000)
						return await ctx.reply(embed=embed)

		if self.warnings[ctx.guild.id][member.id][0] == 0:
			self.warnings[ctx.guild.id].pop(member.id)
			embed = Embed(description="**This user has no warnings**", color=0x000000)
			await ctx.reply(embed=embed,delete_after=10)

	@del_warn.error
	async def del_warn_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed= Embed(title="Permission Not Granted", description=":x: **Insufficient permissions to perform that task**", color=0x002eff)
			await ctx.reply(embed=embed,delete_after=10)
		else:
			raise exc

def setup(bot):
	bot.add_cog(Warn(bot))
