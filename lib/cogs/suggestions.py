from discord.ext.commands import Cog
from discord import Embed
from datetime import datetime
import discord
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
from discord.errors import NotFound
from discord.ext.commands import command
from prsaw import RandomStuff
from discord.ext.commands import Cog
import asyncpraw
from datetime import datetime
import random
from discord import Embed
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role

class Suggestions(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		#COMMUITY SUGGESTIONS CHANNEL:
		guild = self.bot.get_guild(736258866504925306)
		if not message.author == guild.me and message.channel.id == (827960572330377233) and not message.content.startswith("+"):
			try:
				suggestEmbed=Embed(description=f"{message.content}", color=0xBC0808, timestamp=datetime.utcnow())
				suggestEmbed.set_author(name=f"{message.author.display_name}'s Suggestion", icon_url=f"{message.author.avatar_url}")
				
				reaction_message = await self.community_suggestions_channel.send(embed=suggestEmbed)
				await message.delete()
				await reaction_message.add_reaction("<:RES_ThumbsUp:823851707292844102>")
				await reaction_message.add_reaction("<:RES_ThumbsDown:823851740242640907>")
				await reaction_message.add_reaction("<:pepe_cringe:789523123389202452>")
				
			except NotFound:
				pass
	
		if not self.bot.user == message.author and message.channel == self.ai_chat_channel:			api_key = "WjGcchHanX"
			try:
				response = get_ai_response(message.content)
				
				await message.reply(response)
			except NotFound:
				pass
		
		else:	
			return
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.audit_log_channel= self.bot.get_channel(761567095133306880) # CHANNEL HERE
			self.community_suggestions_channel = self.bot.get_guild(736258866504925306).get_channel(827960572330377233)
			self.ai_chat_channel = self.bot.get_channel(759470480981229598)
			self.bot.cogs_ready.ready_up("suggestions")

def setup(bot):
	bot.add_cog(Suggestions(bot))