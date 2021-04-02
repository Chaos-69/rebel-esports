from discord.ext.commands import command
from prsaw import RandomStuff
from discord.ext.commands import Cog
import asyncpraw
from datetime import datetime
import random
from discord import Embed
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role

class Aichat(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.rs = RandomStuff(async_mode = True)
		self.reddit = asyncpraw.Reddit(
							client_id = "OS1rZE67Bn0mMw",
							client_secret = "hdLS0IWqdkzJWmRQr7XbBhgUNaDoyw",
							username = "chad-bot-69",
							password = "chad-bot-69",
							user_agent = "Chad | Bot")
	#REDDIT COMMAND
	@command(name="reddit", brief="Reddit Command", help="Displays top posts from Reddit")
	@cooldown(3, 120, BucketType.user)
	async def meme(self, ctx, subred = "memes"):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:			
			subreddit = await self.reddit.subreddit(subred)
			all_subs = []
			top = subreddit.top(limit = 50)
			
			async for submission in top:
				all_subs.append(submission)
			random_sub = random.choice(all_subs)
			name = random_sub.title
			url = random_sub.url

			embed = Embed(title=name, color=0x000000, timestamp=datetime.utcnow())
			embed.set_image(url= url)
			embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed = embed)

	@Cog.listener()
	async def on_message(self,message):
		if not self.bot.user == message.author and message.channel == self.ai_chat_channel:
			response = await self.rs.get_ai_response(message.content)
			
			await message.reply(response)
		
		else:	
			return 

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		    826442024927363072, 818444886243803216)
			self.ai_chat_channel = self.bot.get_channel(826537727104253993)
			self.bot.cogs_ready.ready_up("aichat")



def setup(bot):
	bot.add_cog(Aichat(bot))