from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, Greedy
from ..db import db
from discord.ext.commands import cooldown, BucketType
from discord import Embed
from discord.ext.commands import has_role, has_any_role
from discord import Member

# |CUSTOM|
embed_color = 0x000000
server_logo = "https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png"
# |CUSTOM|

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)

	# CHANGE PREFIX COMMAND
	@command(name="prefix", brief="Change Guild Prefix",help="Changes the guild prefix.", hidden=True)
	@has_any_role('Chad', 'Admin')
	async def change_prefix(self, ctx, new: str):
		if len(new) > 5:
			embed = Embed(text=":exclamation: The prefix can not be more than 5 characters in length.", color=0xffec00)
			await ctx.reply(ctx.author.mention, delete_after=60)
			await ctx.reply(embed=embed, delete_afer =60)

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new , ctx.guild.id)
			embed = Embed(title="Prefix Changed", description=f"Guild prefix has been changed to **{new}**" , color=0x000000)
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png")
			await ctx.send("@everyone")
			await ctx.reply(embed=embed)

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title=":x: You dont have permissions to do that.", color=0x002eff)
			await ctx.reply(embed=embed,delete_after=10)
	
	
	#ADD BAN COMMAND
	@command(name="addban",brief="Ban Users From Using Commands", help="Blacklists users from being able to use bot commands", hidden=True)
	@has_any_role('Chad', 'Admin')
	async def addban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0x000000)
			await ctx.reply(embed=embed,delete_after=10)

		else:
			self.bot.banlist.extend([t.id for t in targets])
			embed = Embed(description=f"**Added {target.mention} to banlist**", color=0x000000)
			await ctx.reply(embed = embed)
	
	@addban_command.error
	async def addban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.message.delete(delay=60)
			await ctx.reply(embed=embed,delete_after=10)

	#DELETE BAN COMMAND
	@command(name="delban",brief="Unban Users From Commands", help="Removes blacklisted users from being able to use bot commands", hidden=True)
	@has_any_role('Chad', 'Admin')
	async def delban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0x000000)
			await ctx.reply(embed=embed,delete_after=10)

		else:
			for target in targets:
				self.bot.banlist.remove(target.id)
				embed = Embed(description=f"**Removed {target.mention} to banlist**", color=0x000000)
			await ctx.reply(embed = embed)
	
	@delban_command.error
	async def delban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.message.delete(delay=60)
			await ctx.reply(ctx.author.mention,embed=embed,delete_after=10)
    
	#TOGGLE COMMAND
	@command(name="toggle", description="Enable or Disable Commands", help="Enables or Disables commands for all users", hidden=True)
	@has_any_role('Chad', 'Admin')
	async def toggle(self, ctx, *, command):
		command = self.bot.get_command(command)

		if command is None:
			embed = Embed(description="**That command does not exist**", color=0x000000)
			await ctx.reply(embed=embed,delete_after=10)

		elif ctx.command == command:
			embed = Embed(description="**You cannot disable that command**", color=0x000000)
			await ctx.reply(embed=embed,delete_after=10)

		else:
			command.enabled = not command.enabled
			ternary = "enabled" if command.enabled else "disabled"
			embed = Embed(description=f"**I have successfully {ternary} {command.qualified_name}**", color=0x000000)
			await ctx.reply(embed=embed)
	
	@toggle.error
	async def toggle_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.message.delete(delay=60)
			await ctx.reply(embed=embed,delete_after=10)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")


def setup(bot):
	bot.add_cog(Misc(bot))