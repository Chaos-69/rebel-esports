from discord.ext import commands
import asyncio
from discord.ext.commands import Cog
from discord import Embed
from better_profanity import profanity 
from discord.ext.commands import command
from discord.ext.commands import has_permissions, bot_has_permissions, CheckFailure, MissingRequiredArgument
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

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="poll", brief="Poll Command", help="Make polls cuz you are a snowflake and your opinion doesn't mean shit so you have to ask everyone", hidden=True)
    @has_any_role(847565615329574913, 848311479941726288)
    async def poll(self, ctx, *, question):            
        if question is None:
            embed=Embed(title="Poll",description=":x: One or more arguments are missing, use the below provided syntax", color=0xffec00)
            
            fields = [("Syntax", "```+poll | question```", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.message.delete(delay=15)
            return await ctx.reply(embed=embed,delete_after=10)
        

        else:
            messages = [ctx.message]
            answers = []

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100
            
            channel_embed = Embed(title="🎉 Select A Channel",description=f"Which **channel** should it be hosted in? Mention a channel like {ctx.channel.mention}", color=0xBC0808)
            channel_embed.set_footer(text="You can cancel this process by replying with '+cancel'")
            
            questions = [channel_embed]
            ans = []
            for b in questions:
                await ctx.send(embed=b)

                try:
                    msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    embed = Embed(title="✅ Process Canceled", description="You didn\'t answer in the given time!\nPlease answer in under **15 seconds** next time!",color=0xBC0808)
                    await ctx.send(embed = embed,delete_after=10)
                    return
                else:
                    if msg.content == "+cancel":
                        embed = Embed(title="Process Canceled",description="Process has been canceled sucessfully", color=0xBC0808)
                        await ctx.send(embed = embed,delete_after=10)
                        return
                    ans.append(msg.content)
            try:
                c_id = int(ans[0][2:-1])
            
            except:
                embed = Embed(title="✅ Process Canceled", description=f"You didn't mention a channel properly\nMention the channel like this {ctx.channel.mention} next time.",color=0xBC0808)
                await ctx.send(embed=embed,delete_after=10)
                return

            channel = self.bot.get_channel(c_id)
            
            info_embed = Embed(title="Enter your options", color=0xBC0808)
            fields = [("Instuctions","To add options, simply type them out after this message\nYou can add up to **20** options\nThis message will timeout after **60 seconds**", False),
                ("Publish Poll", f"To publish your poll, simply type `{ctx.prefix}publish`",False),
                ("Cancel Poll", f"To cancel your poll, simply type `{ctx.prefix}cancel`", False),
                ("Timeout", "Add options message will timeout after **60 seconds**", False)]
            for name, value, inline in fields:
                info_embed.add_field(name=name, value=value, inline=inline)
                info_embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=info_embed, delete_after=60)

            for i in range(20):
                embed=Embed(title="Enter Your Options", description="Type below your option for the poll\nThis message will appear everytime you sucessfully add a new option", color=0xBC0808)
                messages.append(await ctx.send(embed = embed,))

                try:
                    entry = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    break

                messages.append(entry)
                
                if entry.clean_content.startswith(f'{ctx.prefix}cancel'):
                    embed = Embed(title="Process Canceled",description="Process has been canceled sucessfully", color=0xBC0808)
                    return await ctx.send(embed = embed)
                
                if entry.clean_content.startswith(f'{ctx.prefix}publish'):
                    break
                
                answers.append((to_emoji(i), entry.clean_content))

            try:
                await ctx.channel.delete_messages(messages)
            except:
                pass # oh well

            answer = '\n'.join(f'{i[0]} 》 {i[1]}' for i in answers)
            embed = Embed(title="Poll",color=0xBC0808, timestamp=datetime.utcnow())
            fields = [("Question", f"{question}", False),
                    ("Options", f"{answer}",False),
                    ("Instructions", "React to cast your vote!", False)]
            for name, value, inline in fields:
                embed.set_footer(text=f"Poll by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.add_field(name=name, value=value, inline=inline)
            actual_poll = await channel.send(embed = embed)
            for emoji, _ in (answers):
                await actual_poll.add_reaction(emoji)
            await ctx.send(f"**Poll has been sucessfully created in {channel.mention}**")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.audit_log_channel= self.bot.get_channel(761567095133306880) # CHANNEL HERE
            self.bot.cogs_ready.ready_up("poll")

def setup(bot):
    bot.add_cog(Poll(bot))