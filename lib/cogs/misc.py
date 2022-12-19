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

embed_color = 0xBC0808

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (830188895374278686,771083740217999371)


	#CHANGE PREFIX COMMAND
	@command(name="prefix", brief="Change Guild Prefix",help="Why do you even want me to explain this ffs", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 839423177793077248)
	async def change_prefix(self, ctx, new: str):
		if len(new) > 5:
			embed = Embed(text=":exclamation: The prefix can not be more than 5 characters in length.", color=0xffec00)
			await ctx.reply(embed=embed, delete_afer=60)

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new , ctx.guild.id)
			embed = Embed(description=f"Guild prefix has been changed to **{new}**" , color=0xBC0808)
			await ctx.reply("@here", embed=embed)
	
	
	#ADD BAN COMMAND
	@command(name="addban",brief="Ban Users From Using Commands", help="Prevents users from using bot commands, i can bet my life this aint gonna be used until im alive", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 839423177793077248)
	async def addban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0xBC0808)
			await ctx.reply(embed=embed,delete_after=60)

		else:
			for target in targets:
				if not target.id in self.bot.banlist:	
					self.bot.banlist.extend([t.id for t in targets])
					embed = Embed(description=f"**Added {target.mention} to banlist**", color=0xBC0808)
					await ctx.reply(embed = embed)
						
				else:
					embed = Embed(description="**That user is already banned**", color=0xBC0808)
					await ctx.reply(embed=embed, delete_after=60)

	
	#DELETE BAN COMMAND
	@command(name="delban",brief="Unban Users From Commands", help="Removes previously blacklisted users from using bot commands, another useless command yes", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 839423177793077248)
	async def delban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=60)

		else:
			for target in targets:
				if target.id in self.bot.banlist:
					self.bot.banlist.remove(target.id)
					embed = Embed(description=f"**Removed {target.mention} from banlist**", color=0xBC0808)
					await ctx.reply(embed = embed)
						
				else:
					embed = Embed(description="**That user is already unbanned**", color=0xBC0808)
					await ctx.reply(embed=embed, delete_after=60)
    
	
	#TOGGLE COMMAND
	@command(name="toggle", brief="Enable or Disable Commands", help="Enables or Disables commands, idk why u would want to do that but ok", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 839423177793077248)
	async def toggle(self, ctx, *, command):
		command = self.bot.get_command(command)

		if command is None:
			embed = Embed(description="**That command does not exist**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=60)

		elif ctx.command == command:
			embed = Embed(description="**You cannot disable that command**", color=0xBC0808)
			await ctx.reply(embed=embed,delete_after=60)

		else:
			command.enabled = not command.enabled
			ternary = "enabled" if command.enabled else "disabled"
			embed = Embed(description=f"**I have successfully {ternary} `{command.qualified_name}`**", color=0xBC0808)
			await ctx.reply(embed=embed)	

	#SLOW MODE COMMAND
	@command(name="slowmode", brief="Set Slowmode", help="You can definitely do the same thing from channel settings but using the bot is apparently a flex so sure", hidden=True)
	@has_any_role(847565615329574913, 848311479941726288, 860287157418721311)
	async def slowmode(self, ctx, seconds: int):
			guild = self.bot.get_guild(736258866504925306)
			for channels in guild.channels:
				if seconds < 21600:
					if seconds != 0:
						await ctx.channel.edit(slowmode_delay=seconds)
						embed = Embed(description=f"**Slowmode for {ctx.channel.mention} has been set to {seconds} seconds**", color=0xBC0808)
						return await ctx.send(embed=embed)
					else:
						await ctx.channel.edit(slowmode_delay=seconds)
						embed = Embed(description=f"**Slowmode for {ctx.channel.mention} has been removed**", color=0xBC0808)
						return await ctx.send(embed=embed)
				else:
					embed = Embed(description=f"**Slowmode cannot be greater than 6 hours**", color=0xBC0808)
					return await ctx.send(embed=embed)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")


def setup(bot):
	bot.add_cog(Misc(bot))