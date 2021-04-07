from discord.ext.commands import command
from prsaw import RandomStuff
from discord.ext.commands import Cog
from datetime import datetime
import random
from discord import Embed
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import has_any_role, has_role
import discord

class Inrole(Cog):
    def __init__(self, bot):
        self.bot = bot

    def predicate(self, message, l, r):
        def check(reaction, user):

            if reaction.message.id != message.id or user == self.bot.user:
                return False
            if l and reaction.emoji == "⏪":
                return True
            if r and reaction.emoji == "⏩":
                return True
            return False

        return check

    #INROLE COMMAND
    @command(name = "inrole",brief="Inrole Users", help="Shows all the members with a specific role", hidden=True)
    @has_any_role('Chad', 'Admin', 'Executive')
    async def inrole(self, ctx, *role):
        server = self.bot.get_guild(803028981698789407)
        role_name = (' '.join(role))
        role_id = server.roles[0]
        for role in server.roles:
            if role_name == role.name or role_name.lower() == role.name.lower():
                role_id = role
                break
        else:
            embed = Embed(description="**Either that role does not exist or you provided the role mention\n Use the role name instead of the role mention**\n This is to prevent unnecessary role mentions", color=0x000000)
            await ctx.send(embed = embed)
            return
        n = 0
        members = []
        for member in server.members:
            if role in member.roles:
                n += 1
                name = str(n) + ". " + member.name + " #" + member.discriminator + "\n"
                members.append(name)
        composite_members = [members[x:x + 20] for x in range(0, len(members), 20)]
        pages = []
        for elements in composite_members:
            string = ""
            for element in elements:
                string = string + element
            embedVar = discord.Embed(title=f"List of users with {role} - {n}", colour=0x000000)
            embedVar.add_field(name = "Members", value = string)
            embedVar.set_thumbnail(url=ctx.guild.icon_url)
            pages.append(embedVar)

        page = 0
        left = "⏪"
        right = "⏩"
        while True:
            msg = await ctx.send(embed = pages[(page)], delete_after=120)
            l = page != 0
            r = page != len(pages) - 1
            if l:
                await msg.add_reaction(left)

            if r:
                await msg.add_reaction(right)
            # bot.wait_for_reaction
            react = await self.bot.wait_for('reaction_add', check=self.predicate(msg, l, r))
            
            if str(react[0]) == left:
                page -= 1
            elif str(react[0]) == right:
                page += 1

            await msg.delete()
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("inrole")
            self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
            826442024927363072, 818444886243803216)

def setup(bot):
    bot.add_cog(Inrole(bot))