from discord.ext.commands import Cog
from discord import Forbidden
from discord.ext.commands import command
from discord import Embed
from datetime import datetime
import asyncio
from asyncio import sleep
from discord.ext.commands import has_any_role, has_role
from discord.ext.commands import cooldown, BucketType

class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.audit_log_channel= self.bot.get_channel(803038174057070602) # CHANNEL HERE
			self.invite_log_channel = self.bot.get_channel(803038619794145280) #CHANNEL HERE
			self.bot.cogs_ready.ready_up("log")

	# AVATAR UPDATED
	@Cog.listener()
	async def on_user_update(self, before, after):
		if before.avatar_url != after.avatar_url:
			embed= Embed(title="Avatar Changed", description=f"Avatar Changed for {after.mention} __AKA__ **{after.display_name}**  \n__**Image below is new**__\n  [Before]({before.avatar_url}) --> [After]({after.avatar_url})", color=0x002eff, timestap=datetime.utcnow())
			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)
			await self.audit_log_channel.send(embed=embed)

	# NAME UPDATED
	@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed= Embed(title="Name Changed", description=f"Nickname changed for  {after.mention} __AKA__ **{after.display_name}** ", color=0x002eff, timestap=datetime.utcnow())
			fields = [("Before", before.display_name, False),
						("After", after.display_name, False)]
			embed.set_thumbnail(url=after.avatar_url)
			
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await self.audit_log_channel.send(embed=embed)
		
		#ROLES UPDATED
		elif before.roles != after.roles:
			embed= Embed(title="Roles Updated", description=f"Roles Updated for  {after.mention} __AKA__ **{after.display_name}** ", color=0xffec00, timestap=datetime.utcnow())
			fields = [("Before", ("  ".join(([role.mention for role in before.roles]))), False),
						("After", ("  ".join(([role.mention for role in after.roles]))), False)]
			
			embed.set_thumbnail(url=after.avatar_url)
			
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			await self.audit_log_channel.send(embed=embed)

	
	#MESSAGE EDITED
	@Cog.listener()
	async def on_message_edit(self, before, after):
		if not after.author.bot:
			if before.content != after.content:
				embed = Embed(title="Message Edited",
							  description=f"Edited By {after.author.mention} __AKA__ **{after.author.display_name}**", colour=0xff0000,timestamp=datetime.utcnow())

				fields = [("Before", before.content, False),
						  ("After", after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				await self.audit_log_channel.send(embed=embed)


	
	#MESSAGE DELETED	
	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:
			if not message.guild.get_role(818242893805912067) in message.author.roles:
				embed= Embed(title="Message Deleted", description=f"By  {message.author.mention} __AKA__ **{message.author.display_name}** ", color=0xff0000, timestamp=datetime.utcnow())
				embed.set_thumbnail(url=message.author.avatar_url)
				fields = [("Content", message.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)
				
				await self.audit_log_channel.send(embed=embed)
			
			else:
				return
def setup(bot):
	bot.add_cog(Log(bot))
