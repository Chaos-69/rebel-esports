from discord.ext.commands import Cog
from discord import Embed
from discord.ext.commands import command
from discord.ext.commands import has_permissions, bot_has_permissions
from ..db import db
from discord.ext.commands import command, has_permissions
from datetime import datetime, timedelta
from random import choice
import discord
import asyncio
from discord import Embed
import random
from discord.ext.commands import has_any_role, has_role
from discord.ext import commands
from discord import utils
import discord
from discord.utils import get

class Reactions(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.giveaways = []

	async def getemote(self, arg):
		emoji = utils.get(self.bot.emojis, name = arg.strip(":"))

		if emoji is not None:
			if emoji.animated:
				add = "a"
			else:
				add = ""
			return f"<{add}:{emoji.name}:{emoji.id}>"
		else:
			return None

	async def getinstr(self, content):
		ret = []

		spc = content.split(" ")
		cnt = content.split(":")

		if len(cnt) > 1:
			for item in spc:
				if item.count(":") > 1:
					wr = ""
					if item.startswith("<") and item.endswith(">"):
						ret.append(item)
					else:
						cnt = 0
						for i in item:
							if cnt == 2:
								aaa = wr.replace(" ", "")
								ret.append(aaa)
								wr = ""
								cnt = 0

							if i != ":":
								wr += i
							else:
								if wr == "" or cnt == 1:
									wr += " : "
									cnt += 1
								else:
									aaa = wr.replace(" ", "")
									ret.append(aaa)
									wr = ":"
									cnt = 1

						aaa = wr.replace(" ", "")
						ret.append(aaa)
				else:
					ret.append(item)
		else:
			return content

		return ret


	@Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if not before.channel and after.channel:
			if after.channel.id == (803143634933383218):
				role = discord.utils.get(member.guild.roles, name="Groovy")
				await member.add_roles(role)
			else:
				pass
	    
		elif before.channel and not after.channel:
			if before.channel.id == (803143634933383218):
				role = discord.utils.get(member.guild.roles, name="Groovy")
				await member.remove_roles(role)
			else:
				pass
	
	#BOT MESSAGE REACTIONS			
	@Cog.listener()
	async def on_message(self, message):
		if "xp" in message.content:
			await message.add_reaction(":cheemsPolice:820748937409462279")
		if "Xp" in message.content:
			await message.add_reaction(":cheemsPolice:820748937409462279")
		if "eggspee" in message.content:
			await message.add_reaction(":cheemsPolice:820748937409462279")
		if "eggs" in message.content:
			await message.add_reaction(":cheemsPolice:820748937409462279")
		if "gay" in message.content:
			await message.add_reaction(":D_weird:820756635609464832")
		if "Gay" in message.content:
			await message.add_reaction(":D_weird:820756635609464832")
		if "gae" in message.content:
			await message.add_reaction(":D_weird:820756635609464832")
		if "Gae" in message.content:
			await message.add_reaction(":D_weird:820756635609464832")

		if message.author.bot:
			return

		if ":" in message.content:
			msg = await self.getinstr(message.content)
			ret = ""
			em = False
			smth = message.content.split(":")
			if len(smth) > 1:
				for word in msg:
					if word.startswith(":") and word.endswith(":") and len(word) > 1:
						emoji = await self.getemote(word)
						if emoji is not None:
							em = True
							ret += f" {emoji}"
						else:
							ret += f" {word}"
					else:
						ret += f" {word}"

			else:
				ret += msg
			

			if em:
				webhooks = await message.channel.webhooks()
				webhook = utils.get(webhooks, name = "Imposter NQN")
				if webhook is None:
					webhook = await message.channel.create_webhook(name = "Imposter NQN")

				await webhook.send(ret, username = message.author.name, avatar_url = message.author.avatar_url)
				await message.delete()

	
	def convert(self, time):
		pos = ["s","m","h","d"]

		time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

		unit = time[-1]

		if unit not in pos:
			return -1
		try:
			val = int(time[:-1])
		except:
			return -2

		return val * time_dict[unit]

	#GIVEAWAY COMMAND
	@command(name="gstart", brief="Conduct Giveaways", help="Makes giveaways and picks a random winner", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def giveaway(self, ctx):
		start_embed = Embed(title="🎉 Giveay Initiated", description="Let's start with this giveaway! Answer these questions within **15 seconds**!",color=0x000000)
		await ctx.send(embed=start_embed)
		
		channel_embed = Embed(title="🎉 Select A Channel",description=f"Which **channel** should it be hosted in? Mention a channel like {ctx.channel.mention}", color=0x000000)
		channel_embed.set_footer(text="You can cancel this process by replying with 'cancel'")
		
		duration_embed = Embed(title="🎉 Select The Duration",description="What should be the **duration** of the giveaway? \nReply **(s|m|h|d)** at the end of an integer \n For example `2h`, `60s` , `4d` , `30m` ", color=0x000000)
		duration_embed.set_footer(text="You can cancel this process by replying with 'cancel'")

		prize_embed = Embed(title="🎉 Select A Prize", description="What is the prize of the giveaway?", color=0x000000)
		prize_embed.set_footer(text="You can cancel this process by replying with 'cancel'")

		questions = [channel_embed , duration_embed , prize_embed]

		answers = []

		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel

		for i in questions:
			await ctx.send(embed=i)

			try:
				msg = await self.bot.wait_for('message', timeout=15.0, check=check)
			except asyncio.TimeoutError:
				embed = Embed(title="✅ Process Canceled", description="You didn\'t answer in the given time!\nPlease answer in under **15 seconds** next time!",color=0x000000)
				await ctx.send(embed = embed,delete_after=10)
				return
			else:
				if msg.content == "cancel":
					embed = Embed(title="✅ Process Canceled",description="Process has been canceled sucessfully", color=0x000000)
					await ctx.send(embed = embed,delete_after=10)
					return
				answers.append(msg.content)

		try:
			c_id = int(answers[0][2:-1])
		except:
			embed = Embed(title="✅ Process Canceled", description=f"You didn't mention a channel properly\nMention the channel like this {ctx.channel.mention} next time.",color=0x000000)
			await ctx.send(embed=embed,delete_after=10)
			return

		channel = self.bot.get_channel(c_id)

		time = self.convert(answers[1])
		if time == -1:
			embed = Embed(title="✅ Process Canceled",description=f"You didn't answer with a proper unit! Use either **(s|m|h|d)**\n For example `2h` , `4d` , `30m`", color=0x000000)
			await ctx.send(embed=embed,delete_after=10)
			return
		elif time == -2:
			embed = Embed(title="✅ Process Canceled", description=f"The time must be an integer. Please enter an integer next time.",color=0x000000)
			await ctx.send(embed =embed,delete_after=10)
			return
		global prize
		prize = answers[2]
		confirmation_embed = Embed(description=f"The giveaway will be in {channel.mention} for **{prize}** and will last for **{answers[1]}**", color=0x000000)
		await ctx.send(embed = confirmation_embed)

		embed = Embed(title = "🎉 Giveaway!", description = f"🎁 {prize}", color = ctx.author.color)

		embed.add_field(name = "Hosted by:", value = ctx.author.mention)

		embed.set_footer(text = f"Ends {answers[1]} from now!")

		my_msg = await channel.send(embed = embed)

		await my_msg.add_reaction("🎉")

		await asyncio.sleep(time)

		new_msg = await channel.fetch_message(my_msg.id)

		users = await new_msg.reactions[0].users().flatten()
		users.pop(users.index(self.bot.user))

		winner = random.choice(users)
		embed = Embed(title="🎉 Giveaway Results", description=f"🏆 Results are in! {winner.mention} just won **{prize}** from the giveaway! GG", color=0x000000)
		await channel.send(f"||{winner.mention}||", embed=embed)
	
	#GIVEAWAY REROLL COMMAND
	@command(name="greroll",help="Reroll recently conducted giveaways", brief="Reroll Giveaways", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def reroll(self, ctx, channel : discord.TextChannel, id_ : int):		
		try:
			new_msg = await channel.fetch_message(id_)
		except:
			embed = Embed(description="**The provided ID was incorrect, make sure you have entered the correct giveaway message ID\n Do not enter the ID of a reroll message either**", color=0x000000)
			await ctx.send(embed =embed)
		users = await new_msg.reactions[0].users().flatten()
		users.pop(users.index(self.bot.user))

		winner = random.choice(users)

		embed = Embed(title="🎉 Giveaway Results", description=f"🎉 Results are in! {winner.mention} just won **{prize}** from the giveaway! GG", color=0x000000)
		await channel.send(f"||{winner.mention}||",embed = embed)


	@Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if self.bot.ready and payload.message_id == self.reaction_message.id:
			if not self.community in payload.member.roles:
				await payload.member.remove_roles(self.verification_pending_role, reason= "Member Verified")
				await payload.member.add_roles(self.verify[payload.emoji.name], reason="Member Verified")
				await self.reddit_role_message.remove_reaction(payload.emoji, payload.member)
	
		
		elif payload.emoji.name == "⭐":
			message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
			star_emoji = discord.utils.get(message.reactions , emoji="⭐")
			if not message.author.bot and payload.member_id != message.author.id:
				if star_emoji.count >= 5:
					msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?",message.id) or (None, 0)
					embed = Embed(description=f":star: **{stars+1}** ",
								  colour=message.author.colour,
								  timestamp=datetime.utcnow())

					fields = [("Content", message.content or "See attachment", False),
							("Original Message", f"[Jump!](https://discord.com/channels/803028981698789407/{payload.channel_id}/{payload.message_id})", False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
						embed.set_author(name= f"{message.author.display_name}", icon_url= f"{message.author.avatar_url}")
					if len(message.attachments):
						embed.set_image(url=message.attachments[0].url)

					if not stars:
						star_message = await self.starboard_channel.send(embed=embed)
						db.execute("INSERT INTO starboard (RootMessageID, StarMessageID) VALUES (?, ?)",
								   message.id, star_message.id)

					else:
						star_message = await self.starboard_channel.fetch_message(msg_id)
						await star_message.edit(embed=embed)
						db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)

			else:
				await message.remove_reaction(payload.emoji, payload.member)		
	

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.verify = {"☑️": self.bot.get_guild(803028981698789407).get_role(803035221808513025)}
			self.reaction_message = await self.bot.get_channel(825162415116779541).fetch_message(826457816997822464)
			self.starboard_channel = self.bot.get_channel(825162033707483176)		
			self.verification_pending_role = self.bot.get_guild(803028981698789407).get_role(826575568794943550)
			self.community = self.bot.get_guild(803028981698789407).get_role(803035221808513025)
			self.bot.cogs_ready.ready_up("reactions")


def setup(bot):
	bot.add_cog(Reactions(bot))
