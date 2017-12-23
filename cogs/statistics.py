import discord
from discord.ext import commands
import asyncio
import cogs.basic.db as db
import cogs.basic.statuses as status

def check_admin(ctx):
    guild = ctx.guild
    #admin_roles in ctx.message.author.roles
    return True

class Statistics:
    def __init__(self, bot):
        self.bot = bot
        print("RCS: STATISTICS MODULE")

def setup(bot):
    bot.add_cog(Statistics(bot))

    @commands.command(name='recount')
    @commands.check(check_admin)
    @commands.guild_only()
    async def cmd_partyadd(self, ctx, party_role: discord.Role=None, party_leader_role: discord.Role=None, channel: discord.TextChannel=None):
        """Add a party into the Database."""
        guild = ctx.guild
        ch = ctx.channel
        try:
            
            if party_role is None or party_leader_role is None or channel is None:
                await ch.send(embed=status.wrong_input("Did you provide role, leader role and channel?"))
                return

            print(party_leader_role.name)
            print(party_role.name)
            print(channel.name)

            db.new_party(guild, party_role.id, party_leader_role.id, str(party_role.name).split(" (", 1)[0], party_role.color, channel.id)
            print("lol")
            await ch.send(embed=status.cmd_partyadd(party_role.mention, party_leader_role.mention, party_role.color, channel.mention))
            
            
            print("Added a new party.")
            
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)
