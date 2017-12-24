import discord
from discord.ext import commands
import asyncio
import datetime
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check

def citizen(member):
    return True
    
def checkall(guild, ts):
    print("STARTING CHECKALL")
    print("FOR "+guild.name)
    party_ids = db.select(guild, "party", "role_id", None, None, True)
    if type(party_ids) is str:
        party_ids = [party_ids]
    print(party_ids)
    for member in guild.members:
        print("MEMBER NAME: "+str(member).translate(non_bmp_map))
        print("GUILD NAME: "+str(guild.name))
        db.insert(guild, True, "member", str(member.id),str(ts))
        partyrole = db.party_ids(guild,[role.id for role in member.roles],party_ids)
        print(partyrole)
        db.member_update_party(guild, member, partyrole)
        if member is citizen(member):
            return
            

    
class Member:
    def __init__(self, bot):
        self.bot = bot
        ts = datetime.datetime.utcnow()
        try:
            for guild in bot.guilds:
                print(guild.name)
                check_on_startup = db.cache_getadd(guild, "check_startup", True)
                print("CoS: "+str(check_on_startup))
                
                if str(check_on_startup) == 'False':
                    print("RETURNING")
                    return

                print("CHECKALLING "+guild.name)
                checkall(guild, ts)
                
                    
        except Exception as e:
            print(e)
            
        print("RCS: MEMBERS MODULE")

    #CASUAL CMDS
    @commands.command(name='memberinfo')
    @commands.guild_only()
    async def cmd_memberinfo(self, ctx, member: discord.Member=None):
        """Re-check all members in the server and update them in the database. Will be also done on each startup of the bot unless specified otherwise."""
        try:
            guild = ctx.guild
            ch = ctx.channel
            if member == None:
                return
                
   
        except Exception as e:
            try:
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)
    


    #ADMIN CMDS
    @commands.command(name='membercheck')
    @commands.check(check.check_admin)
    @commands.guild_only()
    async def cmd_membercheck(self, ctx):
        """Re-check all members in the server and update them in the database. Will be also done on each startup of the bot unless specified otherwise."""
        try:
            guild = ctx.guild
            ch = ctx.channel
            ts = ctx.message.created_at
            checkall(guild, ts)
            count = ctx.guild.member_count

            #yield from ch.send(embed=status.cmd_membercheck(count))
   
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)

                
def setup(bot):
    bot.add_cog(Member(bot))
