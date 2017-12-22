import discord
import asyncio
import cogs.basic.db as db

def check_admin(ctx):
    guild = ctx.guild
    #admin_roles = db.cache_getadd(guild,"admin_roles")
    if ctx.message.author == guild.owner:
        return True
    #user_roles = ctx.member.roles
    #admin_roles_ids = db.cache_getadd(guild, "admin_roles_ids")
    #for role in user_roles:
    #if admin_roles is None:
        #return True
    return True
