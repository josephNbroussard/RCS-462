import discord
from discord.ext import commands
import asyncio

import sys, traceback

tf = open("token","r")
token = str(tf.readline())
tf.close()


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    
    prefixes = ['!']
    if not message.guild:
        # Only allow ? to be used in DMs
        return '!'

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.setup',
                      'cogs.inactive',
                      'cogs.statistics',
                      'cogs.party',
                      'cogs.member']
bot = commands.Bot(command_prefix=get_prefix, description='Commands for RCS-462')


@bot.event
async def on_ready():
    print('Logged in as: {} - {}\nVersion: {}\n'.format(bot.user.name,bot.user.id,discord.__version__))
    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(game=discord.Game(name='Supervising', type=0))
    # Here we load our extensions(cogs) listed above in [initial_extensions].
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}.'.format(extension), file=sys.stderr)
                traceback.print_exc()
    
    print('Successfully logged in and booted...!')

try:
    bot.run(token, bot=True, reconnect=True)
except Exception as e:
    print(e)
finally:
    pass
