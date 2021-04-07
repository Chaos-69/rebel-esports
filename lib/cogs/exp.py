from datetime import datetime, timedelta
from random import randint
from typing import Optional
import math
from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import cooldown, BucketType
from ..db import db
from discord.ext.commands import has_any_role, has_role

class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=10)

	async def write_page(self, menu, offset, fields=[]):
		len_data = len(self.entries)

		embed = Embed(title="XP Leaderboard",
					  colour=0x000000)
		embed.set_thumbnail(url=self.ctx.guild.icon_url)
		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} Members")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		offset = (menu.current_page*self.per_page) + 1

		fields = []
		table = ("\n\n".join(f"**{idx+offset}.** {self.ctx.bot.guild.get_member(entry[0]).mention} \n XP: **{entry[1]}** | Level: **{entry[2]}**"
				for idx, entry in enumerate(entries)))

		fields.append(("Ranks", table))

		return await self.write_page(menu, offset, fields)


class Exp(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def process_xp(self, message):
		xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)

		if datetime.utcnow() > datetime.fromisoformat(xplock):
			if message.channel.id == (803028981698789410):
				await self.add_xp(message, xp, lvl)
			else:
				return
	
	async def add_xp(self, message, xp, lvl):
		xp_to_add = randint(5, 15)
		new_lvl = int(((xp+xp_to_add)//42) ** 0.45)

		db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
				   xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=1)).isoformat(), message.author.id)

		if new_lvl > lvl:
			await self.levelup_channel.send(f"🎉 Congrats {message.author.mention} \nYou reached level **{new_lvl:,}**!")
			await self.check_lvl_rewards(message, new_lvl)

	async def check_lvl_rewards(self, message, lvl):

		#Level 100 = 816781972386873355 [God-Tier]
		#Level 90 = 816815889177116722 [Supreme]
		#Level 80 = 816781981601497178 [Peerless]
		#Level 70 = 816781991650787410 [Titan]
		#Level 60 = 816782007782342729 [Mythic]
		#Level 50 = 816782023846395934 [Legendary]
		#Level 40 = 816782039906517002 [Meme-Lord]
		#Level 30 = 803735334948569118 [Master]
		#Level 20 = 803734111507841024 [Pro]
		#Level 10 = 808302510871019550 [Rookie]
			
		if lvl >= 100: # God-Tier [Level 100]
			if (new_role := message.guild.get_role(816781972386873355)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(816815889177116722))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816781972386873355> role! GG")
		
		elif 90 <= lvl < 99: # Supreme [Level 90]
			if (new_role := message.guild.get_role(816815889177116722)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(816781981601497178))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816815889177116722> role! GG")
		
		elif 80 <= lvl < 90: # Peerless [Level 80]
			if (new_role := message.guild.get_role(816781981601497178)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(816781991650787410))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816781981601497178> role! GG")
		
		elif 70 <= lvl < 80: # Titan [Level 70]
			if (new_role := message.guild.get_role(816781991650787410)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(816782007782342729))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816781991650787410> role! GG")
		
		elif 60 <= lvl < 70: # Mythic [Level 60]
			if (new_role := message.guild.get_role(816782007782342729)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(816782023846395934))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816782007782342729> role! GG")
		
		elif 50 <= lvl < 60: # Legendary [Level 50]
			if (new_role := message.guild.get_role(816782023846395934)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(816782039906517002))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816782023846395934> role! GG")
		
		elif 40 <= lvl < 50: # Meme-Lord [Level 40]
			if (new_role := message.guild.get_role(816782039906517002)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(803735334948569118))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&816782039906517002> role! GG")
		
		elif 30 <= lvl < 40: # Master [Level 30]
			if (new_role := message.guild.get_role(803735334948569118)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(803734111507841024))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&803735334948569118> role! GG")

		elif 20 <= lvl < 30: # Pro [Level 20]
			if (new_role := message.guild.get_role(803734111507841024)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await message.author.remove_roles(message.guild.get_role(808302510871019550))
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&803734111507841024> role! GG")

		elif 10 <= lvl < 20: # Rookie [Level 10]
			if (new_role := message.guild.get_role(808302510871019550)) not in message.author.roles:
				await message.author.add_roles(new_role)
				await self.levelup_channel.send(f"Ayyy {message.author.mention} you just recieved the <@&808302510871019550>  role! GG")
	
	@command(name="rank",aliases=["r"], brief="Xp Rank", help="Gives the rank, level and current xp of a provided user")
	@cooldown(3, 30, BucketType.user)
	async def display_level(self, ctx, target: Optional[Member]):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
			
		else:
			target = target or ctx.author

			xp, lvl = db.record("SELECT XP, Level FROM exp WHERE UserID = ?", target.id) or (None, None)
			ids = db.column("SELECT UserID FROM exp ORDER BY XP DESC")
 
			if lvl is not None:
				required_xp = (math.ceil((lvl + 1) ** (1/.55)) * 42)
				embed = Embed(title=f"{target.display_name}'s Rank",color=0x000000)
				fields = [("Username", f"{target.mention} • **{target.display_name}**",False),
						("Level", f"{lvl:,}" , False),
						("XP", f"{xp:,} / {required_xp:,}" , False),
						("Rank", f"{ids.index(target.id)+1} of {len(ids)} Members" , False)]
				for name , value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				embed.set_thumbnail(url = target.avatar_url)
				await ctx.reply(embed=embed)

			else:
				embed = Embed(description="**That member is not tracked by the experience system**",color=0x000000)
				await ctx.reply(embed=embed)

	@command(name="leaderboard", aliases=["lb"],brief="Xp Leaderboard", help="View top users in xp leaderbaord")
	@cooldown(3, 30, BucketType.user)
	async def display_leaderboard(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed, delete_after=10)
			await ctx.message.delete(delay=15)
		
		else:
			records = db.records("SELECT UserID, XP, Level FROM exp ORDER BY XP DESC")

			menu = MenuPages(source=HelpMenu(ctx, records),
							 clear_reactions_after=True,
							 timeout=60.0)
			await ctx.send(f"||{ctx.author.mention}||")
			await menu.start(ctx)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.levelup_channel = self.bot.get_channel(827297851116748871)
			self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)
			self.bot.cogs_ready.ready_up("exp")

	@Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			await self.process_xp(message)


def setup(bot):
	bot.add_cog(Exp(bot))