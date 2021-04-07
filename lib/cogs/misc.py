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
	@is_owner()
	async def change_prefix(self, ctx, new: str):
		if len(new) > 5:
			embed = Embed(text=":exclamation: The prefix can not be more than 5 characters in length.", color=0xffec00)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed, delete_afer=10)

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new , ctx.guild.id)
			embed = Embed(description=f"Guild prefix has been changed to **{new}**" , color=0x000000)
			await ctx.send("@everyone")
			await ctx.reply(embed=embed)

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title=":x: You dont have permissions to do that.", color=0x002eff)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)
	
	
	#ADD BAN COMMAND
	@command(name="addban",brief="Ban Users From Using Commands", help="Blacklists users from being able to use bot commands", hidden=True)
	@is_owner()
	async def addban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0x000000)
			await ctx.message.delete(delay=15)
			await ctx.reply(embed=embed,delete_after=10)

		else:
			for target in targets:
				if not target.id in self.bot.banlist:
					if target == self.bot or ctx.author:
						embed = Embed(description="**You cannot ban yourself or the bot**", color=0x000000)
						await ctx.reply(embed=embed, delete_after=10)
						await ctx.message.delete(delay=15)
						
					else:
						self.bot.banlist.extend([t.id for t in targets])
						embed = Embed(description=f"**Added {target.mention} to banlist**", color=0x000000)
						await ctx.reply(embed = embed)
						
				
				else:
					embed = Embed(description="**That user is already banned**", color=0x000000)
					await ctx.reply(embed=embed, delete_after=10)
					await ctx.message.delete(delay=15)
	
	@addban_command.error
	async def addban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

	
	#DELETE BAN COMMAND
	@command(name="delban",brief="Unban Users From Commands", help="Removes blacklisted users from being able to use bot commands", hidden=True)
	@is_owner()
	async def delban_command(self, ctx, targets: Greedy[Member]):
		if not targets:
			embed = Embed(description="**No targets specified**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

		else:
			for target in targets:
				if target.id in self.bot.banlist:
					if target == self.bot or ctx.author:
						embed = Embed(description="**You cannot unban yourself or the bot**", color=0x000000)
						await ctx.message.delete(delay=15)
						await ctx.reply(embed=embed, delete_after=10)
						
					else:
						self.bot.banlist.remove(target.id)
						embed = Embed(description=f"**Removed {target.mention} from banlist**", color=0x000000)
						await ctx.reply(embed = embed)
						
				else:
					embed = Embed(description="**That user is already unbanned**", color=0x000000)
					await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
	
	@delban_command.error
	async def delban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
    
	
	#TOGGLE COMMAND
	@command(name="toggle", brief="Enable or Disable Commands", help="Enables or Disables commands for all users", hidden=True)
	@is_owner()
	async def toggle(self, ctx, *, command):
		command = self.bot.get_command(command)

		if command is None:
			embed = Embed(description="**That command does not exist**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

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
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
	
	
	#NUKE COMAMND
	@command(name="nuke", brief="Nuke Channels", help="Nukes all messages in a channel", hidden=True)
	@is_owner()
	async def nuke(self, ctx, channel: discord.TextChannel = None):
		if channel == None:
			embed = Embed(description=f"**You did not mention a channel\n For example {ctx.channel.mention}**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
			return

		nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

		if nuke_channel is not None:
			new_channel = await nuke_channel.clone(reason="Has been Nuked!")
			await nuke_channel.delete()
			nuke_channel_embed = Embed(description="**This channel has been nuked**",color=0x000000)
			nuke_channel_embed.set_image(url="https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif")
			await new_channel.send(embed=nuke_channel_embed)
			embed=Embed(description=f"**{new_channel.mention}  Has been nuked sucessfully**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=200)

		else:
			emebd = Embed(description=f"**No channel named {channel.name} was found!**")
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

	@nuke.error
	async def nuke_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)	                			

	
	#ADD ROLE COMMAND
	@command(name="addrole", brief="Add Roles To Users", help="Adds the given role to the provided user", hidden=True)
	@has_any_role('Admin', 'Chad', 'Executive')
	async def add_role(self, ctx, role: discord.Role, targets: Greedy[Member]):
		for target in targets:
			if (ctx.author.top_role.position > target.top_role.position):
				if not role in target.roles:
					await target.add_roles(role)
					embed = Embed(description=f"Added {role.mention} to {target.mention}", color=0x000000)
					await ctx.reply(embed=embed)
			
				else:
					embed = Embed(description=f"**{target.mention} alreadys has {role.mention} role**")
					await ctx.reply(embed=embed, delete_after=10)
					await ctx.message.delete(delay=15)
			else:	
				embed=Embed(title="Task Unsuccessful", description=f":x: **You cannot edit roles for {target.mention}**.", color=0xffec00)
				await ctx.reply(embed=embed, delete_after=10)
				await ctx.message.delete(delay=15)		
		
	@add_role.error
	async def add_role_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)


	#ROMOVE ROLE COMMAND
	@command(name="removerole", brief="Remove Roles From Users", help="Removes the given role from the provided user", hidden=True)
	@has_any_role('Admin', 'Chad', 'Executive')
	async def remove_role(self, ctx, role:discord.Role = None, targets: Greedy[Member] = None):
		for target in targets:
			if (ctx.author.top_role.position > target.top_role.position):
				if role in target.roles:
					await target.remove_roles(role)
					embed = Embed(description=f"Removed {role.mention} from {target.mention}", color=0x000000)
					await ctx.reply(embed=embed)
			
				else:
					embed = Embed(description=f"**{target.mention} does not have {role.mention} role**")
					await ctx.reply(embed=embed, delete_after=10)
					await ctx.message.delete(delay=15)
			else:
				embed=Embed(title="Task Unsuccessful", description=f":x: **You cannot edit roles for {target.mention}**.", color=0xffec00)
				await ctx.reply(embed=embed, delete_after=10)
				await ctx.message.delete(delay=15)		
	
	@remove_role.error
	async def eremove_role_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")


def setup(bot):
	bot.add_cog(Misc(bot))