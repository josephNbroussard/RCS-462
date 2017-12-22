import discord
from discord.ext import commands
import asyncio
import cogs.basic.db as db
import sys

def check_for_inactives():
        print("a")

class Inactivity:
    """Inactivity Control"""

    def __init__(self, bot):
        self.bot = bot
        print("RCS: INACTIVITY MODULE")
        
            

    @commands.command(name='forcecheck')
    @commands.guild_only()
    @asyncio.coroutine
    def cmd_forcecheck(self, ctx):
        """Force a check for inactive users."""
        return

    @commands.command(name='inactiverole')
    @commands.guild_only()
    @asyncio.coroutine
    def cmd_inactiverole(self, ctx, discord):
        """Force a check for inactive users."""
        return

    @asyncio.coroutine
    def on_message(self, ctx):
        if not db.if_member_in_db(ctx.guild,ctx.author):
            db.member_add_db(ctx.guild,ctx.author)
            #yield from ctx.guild.default_channel.send('Welcome!')
        db.member_update_date(ctx)
        #print(ctx.created_at)
        #print(ctx.author)


    
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Inactivity(bot))
