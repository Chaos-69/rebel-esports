from datetime import datetime, timedelta
from platform import python_version
from time import time
import discord, datetime, time
from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version
from discord.ext.commands import Cog, cooldown, BucketType, has_role, CheckFailure
from discord.ext.commands import command
from psutil import Process
from ..db import db
from discord.ext.commands import cooldown, BucketType
start_time = time.time()
from discord.ext.commands import has_any_role, has_role
from discord.ext import tasks

class Meta(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (830188895374278686,771083740217999371)
	
	#PING COMMAND
	@command(name="ping", brief="Ping-Pong!", help="Displays the bots current latency")
	@cooldown(3, 60, BucketType.user)
	async def ping(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			start = time.time()
			embed = Embed(title="🏓 Pong!", description=f"DWSP latency: **{self.bot.latency*1000:,.0f} ms**",color=0xBC0808)
			message = await ctx.reply(embed=embed)
			end = time.time()
			embed = Embed(title="🏓 Pong!",description=f"DWSP latency: **{self.bot.latency*1000:,.0f} ms** \nResponse time: **{(end-start)*1000:,.0f} ms**", color=0xBC0808)
			await message.edit(embed=embed)

	#INFO COMMAND
	@command(name="info" ,brief="Bot Info And Stats", help="Displays bot info and stats")
	@cooldown(3, 3599, BucketType.user)
	async def info(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0xBC0808)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			current_time = time.time()
			difference = int(round(current_time - start_time))
			uptime = str(datetime.timedelta(seconds=difference))	
			embed = Embed(title="Rebel eSports Bot INFO", color=0xBC0808)	
			embed.set_thumbnail(url= ctx.guild.me.avatar_url)

			embed.set_footer(text =f"Requested By {ctx.author.display_name}",
								 icon_url=f"{ctx.author.avatar_url}")
			fields = [("Bot Tag", "Rebel eSports#8205", False),
					("Developer", "Lord Chaos#9958", False),
					("Prefix", ctx.prefix, False),
					("Servers",len(self.bot.guilds), True),
					("Users", f"{self.bot.guild.member_count:,}", True),
					("Versions", f"**Bot Version:** {self.bot.VERSION}\n**Python Version:** {python_version()}\n **Discord.py Version:** {discord_version}", False),
					("Uptime", uptime ,False),
					("Chads' Den Invite", "[Server Link](https://discord.gg/3J92CWNXCK)", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await ctx.reply(embed=embed)


	@command(name="shutdown",brief="Shutdown The Bot", help="Kills the bot like you expect it to")
	@has_any_role(806886607541633045)
	async def shutdown(self, ctx):
		embed = Embed(description="**Shutting Down...**", color=0xBC0808)
		await ctx.reply(embed = embed)

		with open("./data/banlist.txt", "w", encoding="utf-8") as f:
			f.writelines([f"{item}\n" for item in self.bot.banlist])

		db.commit()
		self.bot.scheduler.shutdown()
		await self.bot.logout()
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("meta")


def setup(bot):
	bot.add_cog(Meta(bot))