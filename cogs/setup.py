import discord
from discord.ext import commands
import asyncio

import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check


class Setup:
    def __init__(self, bot):
        self.bot = bot
        print("RCS: SETUP MODULE")
        try:
            for guild in bot.guilds:
                db.new_db(guild)
                db.cache_getadd(guild,"admin_roles")
                for role in guild.roles:
                    print(role.name+":"+str(role.id))
            return
        except Exception as e:
            print(e)
            
    @commands.command(name='setupadmin')
    @commands.check(check.check_admin)
    @commands.guild_only()
    async def cmd_setupadmin(self, ctx, act_type: str=None ,role: discord.Role=None):
        """Add/remove/list roles who can access admin commands."""
        ch = ctx.channel
        try:
            print(act_type)
            if act_type is None or act_type not in ["add","remove","list"]:
                print("None")
                await ch.send(embed=status.wrong_input("You can either input 'add', 'remove' or 'list'. e.g !setupadmin add @admin"))
                return

            if role == None:
                await ch.send(embed=status.wrong_input("You need to input a role too!"))
                return
                
            if act_type == "list":
                
                return
                
            if act_type == "add":
                return
            
            if act_type == "remove":
                return
        
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)

    @commands.command(name='setupchannel')
    @commands.check(check.check_admin)
    @commands.guild_only()
    async def cmd_setupchannel(self, ctx, channel: discord.TextChannel=None):
        """Change the bot channel."""
        ch = ctx.channel
        try:
            if channel == None:
                channel == ch
                
            db.cache_getadd(ctx.guild,"bot_channel",str(channel.id))
            db.cache_update(ctx.guild,"bot_channel",str(channel.id))
        
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)


    

def setup(bot):
    bot.add_cog(Setup(bot))
