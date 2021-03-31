from discord.ext.commands import Cog
from discord import Embed
from better_profanity import profanity 
profanity.load_censor_words_from_file("./data/profanity.txt")
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

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

class Reactions(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.polls = []
		self.giveaways = []

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

	# POLL COMMAND
	@command(name="poll", aliases=["mkpoll"], brief="Make Polls", help="Runs a poll for a given time and displays the results after the deadline", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def create_poll(self, ctx, hours: int, question: str, *options):
		if len(options) > 10:
			embed = Embed(description="You can only supply a maximum of 10 options.",color=0xffec00)
			await ctx.send(embed=embed)

		else:
			embed = Embed(title="Poll",
						  description=f"__{question}__",
						  colour=0x000000,
						  timestamp=datetime.utcnow())

			fields = [("Instructions", f"React to cast a vote! Results will be out in **{hours}** hour(s)", False),
					  ("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			message = await ctx.send(embed=embed)

			for emoji in numbers[:len(options)]:
				await message.add_reaction(emoji)

			self.polls.append((message.channel.id, message.id))

			self.bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now()+timedelta(seconds=hours),
									   args=[message.channel.id, message.id])

	async def complete_poll(self, channel_id, message_id):
			message = await self.bot.get_channel(channel_id).fetch_message(message_id)

			most_voted = max(message.reactions, key=lambda r: r.count)
			embed = Embed(title="Results", description=f"The results are in! Option {most_voted.emoji} was the most popular with **{most_voted.count-1:,}** votes!", color=0x000000)
			await message.channel.send(embed=embed)
			self.polls.remove((message.channel.id, message.id))
	
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

		embed = Embed(title = "🎉 Giveaway!", description = f"{prize}", color = ctx.author.color)

		embed.add_field(name = "Hosted by:", value = ctx.author.mention)

		embed.set_footer(text = f"Ends {answers[1]} from now!")

		my_msg = await channel.send(embed = embed)

		await my_msg.add_reaction("🎉")

		await asyncio.sleep(time)

		new_msg = await channel.fetch_message(my_msg.id)

		users = await new_msg.reactions[0].users().flatten()
		users.pop(users.index(self.bot.user))

		winner = random.choice(users)
		embed = Embed(title="🎉 Giveaway Results", description=f"Results are in! {winner.mention} just won **{prize}** from the giveaway! GG", color=0x000000)
		await channel.send(embed=embed)
	
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

		embed = Embed(title="🎉 Giveaway Results", description=f"Results are in! {winner.mention} just won **{prize}** from the giveaway! GG", color=0x000000)
		await channel.send(embed = embed)


	@Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if self.bot.ready and payload.message_id == self.reaction_message.id:
			await self.reaction_message.add_reaction("☑️")
			await payload.member.add_roles(self.verify[payload.emoji.name], reason="Member Verified")
			await payload.memeber.remove_roles(self.verification_pending_role)
			await self.reaction_message.remove_reaction(payload.emoji, payload.member)

		elif payload.message_id in (poll[1] for poll in self.polls):
			message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

			for reaction in message.reactions:
				if (not payload.member.bot
					and payload.member in await reaction.users().flatten()
					and reaction.emoji != payload.emoji.name):
					await message.remove_reaction(reaction.emoji, payload.member)
		
		elif payload.emoji.name == "⭐":
			message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
			if not message.author.bot and payload.member.id != message.author.id:
				if len(self.reaction_message.reactions) > 4:
					message_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?",
											  message.id) or (None, 0)

					embed = Embed(colour=message.author.colour,
								  timestamp=datetime.utcnow())

					fields = [("Stars", stars+1, False),
							  ("Content", message.content or "Check Attachment", False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
						embed.set_author(name=f"Message By {message.author.display_name}", icon_url= f"{message.author.avatar_url}")

					if len(message.attachments):
						embed.set_image(url=message.attachments[0].url)

					if not stars:
						star_message = await self.starboard_channel.send(embed=embed)
						db.execute("INSERT INTO starboard (RootMessageID, StarMessageID) VALUES (?, ?)",
								   message.id, star_message.id)

					else:
						star_message = await self.starboard_channel.fetch_message(message_id)
						await star_message.edit(embed=embed)
						db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)
				else:
					return
			else:
				await message.remove_reaction(payload.emoji, payload.member)		
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.verify = {"☑️": self.bot.get_guild(803028981698789407).get_role(803035221808513025)}
			self.reaction_message = await self.bot.get_channel(825162415116779541).fetch_message(826457816997822464)
			self.starboard_channel = self.bot.get_channel(825162033707483176)		
			self.verification_pending_role = self.bot.get_guild(803028981698789407).get_role(826575568794943550)
			self.bot.cogs_ready.ready_up("reactions")


def setup(bot):
	bot.add_cog(Reactions(bot))
