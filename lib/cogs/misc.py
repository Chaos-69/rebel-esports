from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, Greedy
from ..db import db
from discord.ext.commands import cooldown, BucketType
from discord import Embed
from discord.ext.commands import has_role, has_any_role, MissingRequiredArgument, Greedy, is_owner
from discord import Member
import asyncio
import discord
from discord.ext.commands.errors import MissingAnyRole

# |CUSTOM|
embed_color = 0xBC0808
# |CUSTOM|

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (830188895374278686,771083740217999371)

	# CHANGE PREFIX COMMAND
	@command(name="prefix", brief="Change Guild Prefix",help="Changes the guild prefix.", hidden=True)
	@has_any_role(806886607541633045)
	async def change_prefix(self, ctx, new: str):
		if len(new) > 5:
			embed = Embed(text=":exclamation: The prefix can not be more than 5 characters in length.", color=0xffec00)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed, delete_afer=10)

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new , ctx.guild.id)
			embed = Embed(description=f"Guild prefix has been changed to **{new}**" , color=0xBC0808)
			await ctx.send("@everyone")
			await ctx.reply(embed=embed)
	
	
	#ADD BAN COMMAND
	@command(name="addban",brief="Ban Users From Using Commands", help="Blacklists users from being able to use bot commands", hidden=True)
	@has_any_role(806886607541633045)
	async def addban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0xBC0808)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)

		else:
			for target in targets:
				if not target.id in self.bot.banlist:
					if target == self.bot or ctx.author:
						embed = Embed(description="**You cannot ban yourself or the bot**", color=0xBC0808)
						await ctx.reply(embed=embed, delete_after=10)
						await ctx.message.delete(delay=15)
						
					else:
						self.bot.banlist.extend([t.id for t in targets])
						embed = Embed(description=f"**Added {target.mention} to banlist**", color=0xBC0808)
						await ctx.reply(embed = embed)
						
				
				else:
					embed = Embed(description="**That user is already banned**", color=0xBC0808)
					await ctx.reply(embed=embed, delete_after=10)
					await ctx.message.delete(delay=15)


	
	#DELETE BAN COMMAND
	@command(name="delban",brief="Unban Users From Commands", help="Removes blacklisted users from being able to use bot commands", hidden=True)
	@has_any_role(806886607541633045)
	async def delban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

		else:
			for target in targets:
				if target.id in self.bot.banlist:
					if target == self.bot or ctx.author:
						embed = Embed(description="**You cannot unban yourself or the bot**", color=0xBC0808)
						await ctx.message.delete(delay=15)
						await ctx.reply(embed=embed, delete_after=10)
						
					else:
						self.bot.banlist.remove(target.id)
						embed = Embed(description=f"**Removed {target.mention} from banlist**", color=0xBC0808)
						await ctx.reply(embed = embed)
						
				else:
					embed = Embed(description="**That user is already unbanned**", color=0xBC0808)
					await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
    
	
	#TOGGLE COMMAND
	@command(name="toggle", brief="Enable or Disable Commands", help="Enables or Disables commands for all users", hidden=True)
	@has_any_role(806886607541633045)
	async def toggle(self, ctx, *, command):
		command = self.bot.get_command(command)

		if command is None:
			embed = Embed(description="**That command does not exist**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

		elif ctx.command == command:
			embed = Embed(description="**You cannot disable that command**", color=0xBC0808)
			await ctx.reply(embed=embed,delete_after=10)

		else:
			command.enabled = not command.enabled
			ternary = "enabled" if command.enabled else "disabled"
			embed = Embed(description=f"**I have successfully {ternary} {command.qualified_name}**", color=0xBC0808)
			await ctx.reply(embed=embed)	

	#SLOW MODE COMMAND
	@command(name="slowmode", brief="Set Slowmode", help="Sets slowmode for a desired channel in seconds", hidden=True)
	@has_any_role(806886607541633045, "RES | Executives", "RES | Management")
	async def slowmode(self, ctx, seconds: int):
			guild = self.bot.get_guild(736258866504925306)
			for channels in guild.channels:
				if seconds != 0:
					await ctx.channel.edit(slowmode_delay=seconds)
					embed = Embed(description=f"**Slowmode for {ctx.channel.mention} has been set to {seconds} seconds**", color=0xBC0808)
					return await ctx.send(embed=embed)
				else:
					await ctx.channel.edit(slowmode_delay=seconds)
					embed = Embed(description=f"**Slowmode for {ctx.channel.mention} has been removed**", color=0xBC0808)
					return await ctx.send(embed=embed)
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")


def setup(bot):
	bot.add_cog(Misc(bot))