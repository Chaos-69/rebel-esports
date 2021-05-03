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
from discord.errors import NotFound

class Reactions(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.giveaways = []
	
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
	@has_any_role(806886607541633045, "RES | Executives")
	async def giveaway(self, ctx):
		start_embed = Embed(title="🎉 Giveay Initiated", description="Let's start with this giveaway! Answer these questions within **15 seconds**!",color=0xBC0808)
		await ctx.send(embed=start_embed)
		
		channel_embed = Embed(title="🎉 Select A Channel",description=f"Which **channel** should it be hosted in? Mention a channel like {ctx.channel.mention}", color=0xBC0808)
		channel_embed.set_footer(text="You can cancel this process by replying with '+cancel'")
		
		duration_embed = Embed(title="🎉 Select The Duration",description="What should be the **duration** of the giveaway? \nReply **(s|m|h|d)** at the end of an integer \n For example `2h`, `60s` , `4d` , `30m` ", color=0xBC0808)
		duration_embed.set_footer(text="You can cancel this process by replying with '+cancel'")

		prize_embed = Embed(title="🎉 Select A Prize", description="What is the prize of the giveaway?", color=0xBC0808)
		prize_embed.set_footer(text="You can cancel this process by replying with '+cancel'")

		questions = [channel_embed , duration_embed , prize_embed]

		answers = []

		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel

		for i in questions:
			await ctx.send(embed=i)

			try:
				msg = await self.bot.wait_for('message', timeout=15.0, check=check)
			except asyncio.TimeoutError:
				embed = Embed(title="✅ Process Canceled", description="You didn\'t answer in the given time!\nPlease answer in under **15 seconds** next time!",color=0xBC0808)
				await ctx.send(embed = embed,delete_after=10)
				return
			else:
				if msg.content == "+cancel":
					embed = Embed(title="✅ Process Canceled",description="Process has been canceled sucessfully", color=0xBC0808)
					await ctx.send(embed = embed,delete_after=10)
					return
				answers.append(msg.content)

		try:
			c_id = int(answers[0][2:-1])
		except:
			embed = Embed(title="✅ Process Canceled", description=f"You didn't mention a channel properly\nMention the channel like this {ctx.channel.mention} next time.",color=0xBC0808)
			await ctx.send(embed=embed,delete_after=10)
			return

		channel = self.bot.get_channel(c_id)

		time = self.convert(answers[1])
		if time == -1:
			embed = Embed(title="✅ Process Canceled",description=f"You didn't answer with a proper unit! Use either **(s|m|h|d)**\n For example `2h` , `4d` , `30m`", color=0xBC0808)
			await ctx.send(embed=embed,delete_after=10)
			return
		elif time == -2:
			embed = Embed(title="✅ Process Canceled", description=f"The time must be an integer. Please enter an integer next time.",color=0xBC0808)
			await ctx.send(embed =embed,delete_after=10)
			return
		global prize
		prize = answers[2]
		confirmation_embed = Embed(description=f"The giveaway will be in {channel.mention} for **{prize}** and will last for **{answers[1]}**", color=0x43b581)
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
		embed = Embed(title="🎉 Giveaway Results", description=f"🏆 Results are in! {winner.mention} just won **{prize}** from the giveaway! GG", color=0xBC0808)
		await channel.send(f"||{winner.mention}||", embed=embed)


	#GIVEAWAY REROLL COMMAND
	@command(name="greroll",help="Reroll recently conducted giveaways", brief="Reroll Giveaways", hidden=True)
	@has_any_role(806886607541633045, "RES | Executives")
	async def reroll(self, ctx, channel : discord.TextChannel, id_ : int):		
		try:
			new_msg = await channel.fetch_message(id_)
		
		except:
			
			embed = Embed(description="**The provided ID was incorrect, make sure you have entered the correct giveaway message ID\n Do not enter the ID of a reroll message either**", color=0xBC0808)
			await ctx.send(embed =embed)
		
		users = await new_msg.reactions[0].users().flatten()
		users.pop(users.index(self.bot.user))

		winner = random.choice(users)

		embed = Embed(title="🎉 Giveaway Results", description=f"🎉 Results are in! {winner.mention} just won **{prize}** from the giveaway! GG", color=0xBC0808)
		await channel.send(f"||{winner.mention}||",embed = embed)

	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.guild = self.bot.get_guild(736258866504925306)
			self.bot.cogs_ready.ready_up("reactions")


def setup(bot):
	bot.add_cog(Reactions(bot))
