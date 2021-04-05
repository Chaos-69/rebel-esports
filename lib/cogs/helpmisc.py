from typing import Optional
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_role
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role

# |CUSTOM|
embed_color = 0x000000
server_logo = "https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png"
# |CUSTOM|

def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

	params = " ".join(params)
	
	return f"```{cmd_and_aliases} {params}```"

class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		 826442024927363072, 818444886243803216)

		super().__init__(data, per_page=3)
    

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)
		embed= Embed(title=f"Miscellaneous Help",
    		description=f"Welcome to the **CHΛD丨BӨT** Miscellaneous Help dialog. React to the arrows below in order to navigate through the panel!",
    		color=embed_color)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png")		
		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands")

		for name, value in fields: 
			embed.add_field(name=name, value=value, inline=False)
		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			fields.append((entry.brief or "No description", syntax(entry)))

		return await self.write_page(menu, fields)

class Helpmisc(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command("help")

	async def cmd_help(self, ctx, command):
			embed = Embed(title=f"Details for `{command}` command",
			         description=syntax(command),
			         color=embed_color)
			embed.add_field(name="Command description", value=command.help)
			embed.set_footer(text =f"Requested By {ctx.author.display_name}",
							 icon_url=f"{ctx.author.avatar_url}")
			await ctx.send(ctx.author.mention,embed=embed, delete_after=60)

	#GENERAL HELP COMMAND
	@command(name="help", brief="Help Categories", help="Displays all the categories assigned with commands.")
	@cooldown(3, 60, BucketType.user)
	async def show_help(self, ctx, cmd: Optional[str]):
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		 826442024927363072, 818444886243803216)
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			if cmd is None:
					embed=Embed(title="Help Categories", description="Below are all the categories assigned to specific commands.", color=0x000000)
					embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png")
					embed.set_footer(text =f"Requested By {ctx.author.display_name}",
									 icon_url=f"{ctx.author.avatar_url}")
					fields = [("Total Commands",f"**CHΛD丨BӨT** has a total of **{len(self.bot.commands)}** commands" , False),
								("Miscellaneous","To view all the miscellaneous commands, use the following syntax ```?helpmisc ```" , False),
								("Moderation","To view all the moderation commands, use the following syntax ```?helpmod ```" , False),
								("Individual Commands", "To view help for individual commands, use the following syntax ```?help <command>```", False)]
					for name , value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					await ctx.reply(embed=embed)
			
			else:
				if (command := get(self.bot.commands, name=cmd)):
					await self.cmd_help(ctx, command)

				else:
					embed=Embed(description="**That command does not exist.**",color=embed_color)
					await ctx.reply(embed=embed)	


	#MISC HELP COMMAND
	@command(name="helpmisc", brief="Help For Miscellaneous Commands", help="Provides Help For Miscellaneous Commands", hidden=True)
	@cooldown(3, 60, BucketType.user)
	async def show_help_misc(self, ctx, cmd: Optional[str]):
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		 826442024927363072, 818444886243803216)
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			if cmd is None:
				commands_to_always_hide = ["help", "helpmisc", "helpmod", "commands"]
				commands = []
				for command in self.bot.commands:
					if not command.hidden and not command.name in commands_to_always_hide:
							commands.append(command)
					menu = MenuPages(source=HelpMenu(ctx, list(commands)),
									delete_message_after=True,
									timeout=60.0)
				await ctx.send(f"||{ctx.author.mention}||")
				await menu.start(ctx)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("helpmisc")


def setup(bot):
	bot.add_cog(Helpmisc(bot))