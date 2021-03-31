from discord.ext.commands import Cog
from discord import Embed
from datetime import datetime
import discord
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role

class Suggestions(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		if not message.author.bot and message.channel.id == (803319938575630376):
			if not message.content.startswith("?nosuggest"):
				await message.delete()
				suggestEmbed=Embed(description=f"{message.content}", color=0x000000, timestamp=datetime.utcnow())
				suggestEmbed.set_author(name=f"{message.author.display_name}'s Suggestion", icon_url=f"{message.author.avatar_url}")
				suggestEmbed.set_footer(text="Use `?nosuggest` if you dont want your message to appear as an embed")
				await self.audit_log_channel.send(embed=suggestEmbed)
				
				reaction_message = await message.channel.send(embed=suggestEmbed)
				await reaction_message.add_reaction("<:RES_ThumbsUp:824692074615930942>")
				await reaction_message.add_reaction("<:RES_ThumbsDown:824692213476360292>")
				await reaction_message.add_reaction("<:pepe_cringe:824692893981736991>")
		
			else:
				await message.delete()
				message.content = message.content[10:]
				await message.channel.send(f"{message.content} • Said By {message.author.mention}")

		else:
			return


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.audit_log_channel= self.bot.get_channel(803038174057070602) # CHANNEL HERE
			self.bot.cogs_ready.ready_up("suggestions")

def setup(bot):
	bot.add_cog(Suggestions(bot))