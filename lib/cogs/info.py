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
		self.allowed_channels = (830188895374278686,771083740217999371, 803031892235649044)
		
	@command(name="userinfo", aliases =["ui","whois"], help="Sends you the social security number, address, passport and bank account info of a member", brief="User Information")
	@cooldown(3, 60, BucketType.user)
	async def user_info(self, ctx, target: Optional[Member]):
		target = target or ctx.author
		roles = [role for role in reversed(target.roles[1:])]
		role_mentions = "   ".join(([role.mention for role in roles]))

		embed = Embed(title=f"**{str(target.display_name)}'s Information**", 
						color =0xBC0808, timestap=datetime.utcnow())

		fields = [("Name", f"{target.mention}丨{target.name}#{target.discriminator}", False),
					("ID", f"{target.id}", False),				
					("Joined at", target.joined_at.strftime("%d/%m/%Y"), True),
					("Create at", target.created_at.strftime("%d/%m/%Y"), True),
					(f"Roles [{len(roles)}]", (role_mentions if len(role_mentions) < 1020 else "Too many roles to mention!" ), False),									
					("Activity",f"{target.activity.name if target.activity else 'N/A' } ", False),
					("Boost Status", bool(target.premium_since), True),
					("Status", str(target.status).title(), True)]
					
		embed.set_thumbnail(url=target.avatar_url)
		embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
		
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await ctx.reply(embed=embed)

	
	@command(name="serverinfo", aliases=["si"], help="Displays some random shit about the server no one cares about", brief="Server Information")
	@cooldown(3, 60, BucketType.user)
	async def server_info(self, ctx):
		embed = Embed(title=f"**{ctx.guild.name}**", 
						color =0xBC0808, timestap=datetime.utcnow())

		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text=f"ID : {ctx.guild.id}")
		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("Owner", ctx.guild.owner, True),
				("Region", ctx.guild.region, True ),
				#("Statuses", f"🟩 **Online:** {statuses[0]}\n🟧 **Idle:** {statuses[1]}\n🟥 **DnD:** {statuses[2]}\n⬜ **Offline:** {statuses[3]}", False),				
				("Members", len(ctx.guild.members), False),
				("Creation Date", ctx.guild.created_at.strftime("%d/%m/%Y"), False),				
				("Roles", len(ctx.guild.roles), True),				
				("Channels", f"**Text Channels:** {len(ctx.guild.text_channels)}\n **Voice Channels:** {len(ctx.guild.voice_channels)}\n **Categories:** {len(ctx.guild.categories)}", False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		await ctx.reply(embed=embed)
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("info")


def setup(bot):
	bot.add_cog(Info(bot))