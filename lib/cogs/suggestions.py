from discord.ext.commands import Cog
from discord import Embed
from datetime import datetime
import discord
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
from discord.errors import NotFound

class Suggestions(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		#COMMUITY SUGGESTIONS CHANNEL:
		guild = self.bot.get_guild(736258866504925306)
		if not message.author == guild.me and message.channel.id == (827960572330377233):
			if not message.content.startswith("?nosuggest"):
				try:
					suggestEmbed=Embed(description=f"{message.content}", color=0xBC0808, timestamp=datetime.utcnow())
					suggestEmbed.set_author(name=f"{message.author.display_name}'s Suggestion", icon_url=f"{message.author.avatar_url}")
					suggestEmbed.set_footer(text="?nosuggest = Simple message")
					await self.audit_log_channel.send(embed=suggestEmbed)
					
					reaction_message = await self.community_suggestions_channel.send(embed=suggestEmbed)
					await message.delete()
					await reaction_message.add_reaction("<:RES_ThumbsUp:824692074615930942>")
					await reaction_message.add_reaction("<:RES_ThumbsDown:824692213476360292>")
					await reaction_message.add_reaction("<:pepe_cringe:824692893981736991>")
				
				except NotFound:
					pass
			else:
				
				message.content = message.content[10:]
				await message.channel.send(f"{message.content} • Said By {message.author.mention}")
				await message.delete()

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.audit_log_channel= self.bot.get_channel(761567095133306880) # CHANNEL HERE
			self.community_suggestions_channel = self.bot.get_guild(736258866504925306).get_channel(827960572330377233)
			self.bot.cogs_ready.ready_up("suggestions")

def setup(bot):
	bot.add_cog(Suggestions(bot))