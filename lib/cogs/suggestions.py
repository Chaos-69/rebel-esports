from discord.ext.commands import Cog
from discord import Embed
from datetime import datetime
import discord
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
from discord.errors import NotFound
from discord.ext.commands import command
from discord.ext.commands import Cog
import asyncpraw
from datetime import datetime
import random
from discord import Embed
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
import randomstuff
from prsaw import RandomStuff
from discord.ext import tasks


class Suggestions(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.rs = RandomStuff(async_mode= True, api_key= "WjGcchHanX" )
		self.reddit = asyncpraw.Reddit(
							client_id = "OS1rZE67Bn0mMw",
							client_secret = "hdLS0IWqdkzJWmRQr7XbBhgUNaDoyw",
							username = "chad-bot-69",
							password = "chad-bot-69",
							user_agent = "Chad | Bot")
	#REDDIT COMMAND
	@command(name="reddit",aliases=["meme"], brief="Surf Reddit", help="Waste your time looking at shit reddit posts")
	@cooldown(3, 120, BucketType.user)
	async def meme(self, ctx, *, subred = "memes"):
			try:
				subreddit = await self.reddit.subreddit(subred)
				all_subs = []
				hot = subreddit.hot(limit = 100)
				
				async for submission in hot:
					all_subs.append(submission)
				random_sub = random.choice(all_subs)
				name = random_sub.title
				url = random_sub.url 

				embed = Embed(title=name, url= url, color=0xBC0808)
				embed.set_image(url= url)
				embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url= ctx.author.avatar_url)
				await ctx.reply(embed = embed)
			
			except:
				this = await ctx.reply("Your momma made that sub? <:cringe:789523123389202452> <a:pepe_fu:804010091619680267>")
				await this.add_reaction("<a:keke:805437951105695746>")
	
	@tasks.loop(seconds=600)
	#REDDIT MEMES LOOP
	async def memes_loop(self):
		reddit_feed_channel = self.bot.get_guild(736258866504925306).get_channel(858993983530860554)
		
		try:
			subreddit = await self.reddit.subreddit('memes')
			all_subs = []
			hot = subreddit.hot(limit = 100000)
			
			async for submission in hot:
				all_subs.append(submission)
			random_sub = random.choice(all_subs)
			name = random_sub.title
			url = random_sub.url 

			embed = Embed(title = name, url = url, color = 0xBC0808)
			embed.set_image(url = url)
			await reddit_feed_channel.send(embed = embed)
		
		except:
			print("Something went wrong with reddit memes loop!")
			pass

	@tasks.loop(seconds=600)
	#REDDIT CODM LOOP
	async def codm_loop(self):
		reddit_feed_channel = self.bot.get_guild(736258866504925306).get_channel(859002683674198016)
		
		try:
			subreddit = await self.reddit.subreddit('CallOfDutyMobile')
			all_subs = []
			hot = subreddit.hot(limit = 100000)
			
			async for submission in hot:
				all_subs.append(submission)
			random_sub = random.choice(all_subs)
			name = random_sub.title
			url = random_sub.url 

			embed = Embed(title = name, url = url, color = 0xBC0808)
			embed.set_image(url = url)
			await reddit_feed_channel.send(embed = embed)
		
		except:
			print("Something went wrong with reddit codm loop!")
			pass

	#REDDIT PCMR LOOP
	@tasks.loop(seconds=600)
	async def pcmr_loop(self):
		reddit_feed_channel = self.bot.get_guild(736258866504925306).get_channel(859002723033546802)
		
		try:
			subreddit = await self.reddit.subreddit('pcmasterrace')
			all_subs = []
			hot = subreddit.hot(limit = 100000)
			
			async for submission in hot:
				all_subs.append(submission)
			random_sub = random.choice(all_subs)
			name = random_sub.title
			url = random_sub.url 

			embed = Embed(title = name, url = url, color = 0xBC0808)
			embed.set_image(url = url)
			await reddit_feed_channel.send(embed = embed)
		
		except:
			print("Something went wrong with reddit pcmr loop!")
			pass			

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
				
				try:
					await reaction_message.add_reaction("<:RES_ThumbsUp:823851707292844102>")
					await reaction_message.add_reaction("<:RES_ThumbsDown:823851740242640907>")
					await reaction_message.add_reaction("<:cringe:789523123389202452>")

				
				except:
					await reaction_message.add_reaction("👍")
					await reaction_message.add_reaction("👎")
					await reaction_message.add_reaction("😓")
			
			except NotFound:
				await message.author.send("Your suggestion could not be logged because it was either deleted or removed!")



		#AI CHAT
		if not self.bot.user == message.author:
			if message.channel == self.ai_chat_channel_1 or message.channel == self.ai_chat_channel_2 or message.channel == self.ai_chat_channel_3:
				if "@everyone" not in message.content and "@here" not in message.content:
					try:
						async with randomstuff.AsyncClient(api_key="tQeJ9s1ZRUQt") as client:
							response = await client.get_ai_response(message.content)
							await message.reply(response.message)
					
					except:
						await message.channel.send("Try again later")
						await self.config_channel.send(f"{message.author.mention} tried to use ai-chat \n Ai-chat being gay again, smfh")
				else:
					await message.reply("You really thought that would work? <:cringe_2:789523123389202452>")
					embed = Embed(description=f"{message.author.name}#{message.author.discriminator} tried to ping `@everyone` or `@here` in <#826537727104253993>", color=0xBC0808, timestamp=datetime.utcnow())
					await self.audit_log_channel.send(embed=embed)
		
		else:	
			return 
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.memes_loop.start()
			self.codm_loop.start()
			self.pcmr_loop.start()
			self.audit_log_channel= self.bot.get_channel(761567095133306880) # CHANNEL HERE
			self.community_suggestions_channel = self.bot.get_guild(736258866504925306).get_channel(827960572330377233)
			self.ai_chat_channel_1 = self.bot.get_guild(736258866504925306).get_channel(759470480981229598)
			self.ai_chat_channel_2 = self.bot.get_guild(795726142161944637).get_channel(861194200413110303)
			self.ai_chat_channel_3 = self.bot.get_guild(803028981698789407).get_channel(861223245335363594)
			self.config_channel = self.bot.get_guild(736258866504925306).get_channel(830188895374278686)
			self.bot.cogs_ready.ready_up("suggestions")

def setup(bot):
	bot.add_cog(Suggestions(bot))