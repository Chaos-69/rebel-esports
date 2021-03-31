from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command
from ..db import db
from discord import Embed
from datetime import datetime
from discord.ext.commands import has_any_role, has_role

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
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
		embed = Embed(title="Member Joined", description=f"{member.mention} __**AKA**__ {member.display_name}" ,color=0x06af00, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"ID {member.id}")
		await self.invite_log_channel.send(embed=embed)
		
		try:
			embed=Embed(description=f"Welcome to **{member.guild.name}!** Kindly cope with Discord's Terms Of Services and be sure to read <#820081277376921601>", color=0x000000)
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