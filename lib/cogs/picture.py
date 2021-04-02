from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, Greedy
from ..db import db
from discord.ext.commands import cooldown, BucketType
from discord import Embed, Member
from typing import Optional
from datetime import datetime
from discord.ext.commands import has_role
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
from PIL import Image
from io import BytesIO
import discord

class Picture(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)

	@command(name="wanted", brief="Wanted Command", help="Displays the user as wanted")
	@cooldown(3, 60, BucketType.user)
	async def wanted(self, ctx, user: discord.Member = None):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			if user == None:
				user = ctx.author

			wanted = Image.open("wanted.jpg")

			asset  = user.avatar_url_as(size = 128)
			data = BytesIO(await asset.read())
			pfp = Image.open(data)

			pfp = pfp.resize((199,199))
			wanted.paste(pfp,(112,202))
			wanted.save("profile.png")

			await ctx.reply(file= discord.File("profile.png"))


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("picture")


def setup(bot):
	bot.add_cog(Picture(bot))