from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from ..db import db
from discord.ext.commands import cooldown, BucketType
from discord import Embed, Member
from typing import Optional
from datetime import datetime
from discord.ext.commands import has_role
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role

class Info(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)
		
	@command(name="userinfo", aliases =["ui"], help="Displays info for a specific member in the guild.", brief="User Information")
	@cooldown(3, 60, BucketType.user)
	async def user_info(self, ctx, target: Optional[Member]):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention} **Is blacklisted for bot commands, please use <@&803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			target = target or ctx.author
			roles = [role for role in reversed(target.roles[1:])]

			embed = Embed(title=f"**{str(target.display_name)}'s Information**", 
							color =embed_color, timestap=datetime.utcnow())

			fields = [("Name", f"{target.mention} __AKA__ {str(target.display_name)}", False),
						("ID", f"ID {target.id}", False),				
						(f"Roles [{len(roles)}]", ("  ".join(([role.mention for role in roles]))), False),
						("Joined at", target.joined_at.strftime("%d/%m/%Y | %H:%M:%S"), True),
						("Create at", target.created_at.strftime("%d/%m/%Y | %H:%M:%S"), True),									
						("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''} ", False),
						("Boosted", bool(target.premium_since), True),
						("Status", str(target.status).title(), True)]
						
			embed.set_thumbnail(url=target.avatar_url)
			
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await ctx.reply(embed=embed)

	
	@command(name="serverinfo", aliases=["guildinfo", "si", "gi"], help="Displays detailed server info", brief="Server Information")
	@cooldown(3, 60, BucketType.user)
	async def server_info(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention} **Is blacklisted for bot commands, please use <@&803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			embed = Embed(title=f"**{ctx.guild.name}**", 
							color =embed_color, timestap=datetime.utcnow())

			embed.set_thumbnail(url=ctx.guild.icon_url)
			embed.set_footer(text=f"ID {ctx.guild.id}")
			statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
						len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
						len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
						len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

			fields = [("Owner", ctx.guild.owner, True),
					("Region", ctx.guild.region, True ),
					("Statuses", f"**Online** {statuses[0]} **Idle** {statuses[1]} **DnD** {statuses[2]} **Offline** {statuses[3]}", False),				
					("Members", len(ctx.guild.members), True),
					("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
					("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
					("Created at", ctx.guild.created_at.strftime("%d/%m/%Y | %H:%M:%S"), False),				
					("Text Channels", len(ctx.guild.text_channels), True),
					("Voice Channels", len(ctx.guild.voice_channels), True),
					("Categories", len(ctx.guild.categories), True),
					("Roles", len(ctx.guild.roles), True),
					("Invites", len(await ctx.guild.invites()), True)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await ctx.reply(embed=embed)
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("info")


def setup(bot):
	bot.add_cog(Info(bot))