import discord
import aiofiles
from discord.ext.commands import Cog
from discord.ext.commands import command,has_permissions, MissingPermissions, has_any_role
from typing import Optional
from discord import Embed
from discord.ext.commands import CheckFailure
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role, is_owner
from datetime import datetime
import datetime as dt
from discord.errors import Forbidden
from discord.errors import NotFound

class Warn(Cog):
	def __init__(self, bot):
		self.bot = bot
		intents = discord.Intents.default()
		intents.members = True
		self.warnings = {}

	
	@Cog.listener()
	async def on_ready(self):
		self.bot.cogs_ready.ready_up("warn")
		for guild in self.bot.guilds:
			self.warnings[guild.id] = {}
			self.mod_log_channel = self.bot.get_channel(822428198989725727)
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
	@has_any_role(847565615329574913, 848311479941726288)
	async def warn(self, ctx, member: discord.Member=None, *, reason: Optional[str] = "No reason provided"):
		guild = ctx.guild #self.bot.get_guild(803028981698789407)
		if member == None:
				embed = Embed(title="Warn", description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
				fields = [("Syntax", "```?warn <target> [reason]```", False)]
				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)			
				await ctx.message.delete(delay=15)
				return await ctx.reply(embed=embed,delete_after=10)
		
		if member == guild.me:
			embed = Embed(description="**:x: You cannot warn the bot**", color=0xffec00)
			message = await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
			return await message.add_reaction("<:D_pepecringe~1:821795309784006678")
	
		if member == ctx.author:
			embed = Embed(description="**:x: You cannot warn yourself**", color=0xffec00)
			message = await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
			return await message.add_reaction("<:D_pepecringe~1:821795309784006678")

		if (ctx.author.top_role.position < member.top_role.position and member.guild_permissions.administrator):
			embed=Embed(title="Task Unsuccessful", description=f":x: **You are unable to warn {member.display_name}**.", color=0xffec00)
			await ctx.message.delete(delay=15)
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
		embed = Embed(description=f"***{member.mention} has been warned***", color=0x43b581)
		await ctx.send(embed=embed, delete_after=120)
		
		try:
		
			member_embed= Embed(title="Warn Report", description=f"You have been **warned** in {member.guild.name} due to __**{reason}**__", color=0xff0000)
			await member.send(embed=member_embed)
		
		except Forbidden:
			pass
			
		embed=Embed(title="Member Warned", color=0xff0000, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
			
		fields = [("Member", f"{member.mention} __**AKA**__ {member.display_name}", False),
		("Actioned By",f"{ctx.author.mention} __**AKA**__ {ctx.author.display_name}" , False),
		("Reason", reason , False)]
		for name , value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await self.mod_log_channel.send(embed=embed)

   
    #WARNINGS COMMAND
	@command(name="warnings", brief="Check Warnings Command",help="Displays all of the users warnings", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288)
	async def warnings(self, ctx, member: discord.Member=None):
		if member is None:
			embed = Embed(title="Warnings", description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
			fields = [("Syntax", "```?warnings <target>```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)			
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)	    		
		
		try:
			count = self.warnings[ctx.guild.id][member.id][0]
			
			embed = discord.Embed(title=f"Warnings For {member.name} [{count}] ", description="", colour=0xff0000)
			i = 1
			for admin_id, reason, time in self.warnings[ctx.guild.id][member.id][1]:
				admin = ctx.guild.get_member(admin_id)
				time = time
				embed.description += f"**__Warning {i}__** \n**Moderator**:- {admin.mention}  \n**Reason**:- `{reason}`\n**Date**:- {time.strftime('%d/%m/%Y')} \n \n"
				i += 1
				embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
			await ctx.reply(embed=embed)

		except KeyError:
			embed = Embed(description="**This user has no warnings**", color=0xBC0808)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
	
	#DELETE WARN COMMAND
	@command(name="delwarn", brief="Delete Warn Command", help="Deletes previously added warnings for users", hidden=True)
	@is_owner()
	async def del_warn(self, ctx, member: discord.Member=None, index=None):
		if member is None:
			embed = Embed(title="Delete Warn", description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
			fields = [("Syntax", "```?delwarn <target> [warn-number]```", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)			
			await ctx.message.delete(delay=15)
			return await ctx.reply(embed=embed,delete_after=10)

		if self.warnings[ctx.guild.id][member.id][0] != 0:
			index = int(index) - 1
			if index is not None and index < len(self.warnings[ctx.guild.id][member.id]):
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
									("Actioned By",f"{ctx.author.mention} __**AKA**__ {ctx.author.display_name}" , False)]
							for name , value, inline in fields:
								embed.add_field(name=name, value=value, inline=inline)
							await self.mod_log_channel.send(embed=embed)
							embed = Embed(description=f"***Warning removed for {member.mention}***", color=0x43b581)
							return await ctx.reply(embed=embed)
			else:
				embed = Embed(description="**Provide a valid warn number**", color=0xBC0808)
				await ctx.message.delete(delay=15)
				return await ctx.reply(embed=embed,delete_after=10)
				
		
		else:
			embed = Embed(description="**This user has no warnings**", color=0xBC0808)
			await ctx.message.delete(delay=15)
			return await ctx.reply(embed=embed,delete_after=10)

def setup(bot):
	bot.add_cog(Warn(bot))
