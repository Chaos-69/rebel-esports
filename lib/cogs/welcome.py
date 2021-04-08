from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command
from ..db import db
from discord import Embed
from datetime import datetime
from discord.ext.commands import has_any_role, has_role
from random import choice as randchoice
import discord

# |CUSTOM|
embed_color = 0x000000
server_logo = "https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png"
# |CUSTOM|

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.invite_log_channel = self.bot.get_channel(803038619794145280) #CHANNEL HERE
			self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
				826442024927363072, 818444886243803216)
			self.guild = self.bot.get_guild(803028981698789407)
			self.gateway = self.bot.get_channel(803029791249924147)
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
		embed = Embed(title="Member Joined", description=f"{member.mention} __**AKA**__ {member.display_name}" ,color=0x06af00, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"ID: {member.id}")
		await self.invite_log_channel.send(embed=embed)
		
		welcome_message = [f"{member.mention} Yo! Welcome to **The Chads' Den!**\nNow the server has **{self.guild.member_count}** members!\nBe sure to check out <#803029543686242344> in order to abide by the servers rules and regulations!\nContact <@&818567860976615444> for any queries", 
		f"{member.mention} We are happy to see you join **The Chads' Den!**\nNow the server has **{self.guild.member_count}** members !\nBe sure to check out <#803029543686242344> in order to abide by the servers rules and regulations!\nContact <@&818567860976615444> for any queries",
		f"{member.mention} Just joined **The Chads' Den!**\nNow the server has **{self.guild.member_count}** members!\nBe sure to check out <#803029543686242344> in order to abide by the servers rules and regulations!\nContact <@&818567860976615444> for any queries"]

		embed = Embed(description=f"{randchoice(welcome_message)}", color=0x000000, timestamp=datetime.utcnow())
		embed.set_thumbnail(url= f"{member.avatar_url}")
		embed.set_author(name=f"Welcome {member.display_name}!", icon_url=f"{self.guild.icon_url}")
		embed.set_footer(text=f"ID: {member.id}")
		await self.gateway.send(embed=embed)
		try:
			embed=Embed(description=f"**Welcome to {member.guild.name}! Kindly cope with Discord's Terms Of Services and be sure to read <#803029543686242344>**", color=0x000000)
			await member.send(embed=embed)

		except Forbidden:
			pass
		
		await member.add_roles(member.guild.get_role(826575568794943550))
                                                       #VERIFICATION PENDING
	@Cog.listener()
	async def on_member_remove(self, member):
		db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
		embed = Embed(title="Member Left",description= f"{member.mention} __**AKA**__ {member.display_name}" ,color=0x919191, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"ID {member.id}")
		await self.invite_log_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Welcome(bot))