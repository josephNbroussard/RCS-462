import discord
from discord.ext import commands
import asyncio

import cogs.basic.db as db
import cogs.basic.statuses as status
import cogs.basic.checks as check


def party_role_change(guild,before_id,after_id):
    before_party = db.party_ids(guild,before_id)
    after_party = db.party_ids(guild,after_id)
    if before_party == after_party:
        return False

    if before_party == None:
        return ["added",after_party]

    if after_party == None:
        return ["left",before_party]
    
    

class Party:
    def __init__(self, bot):
        self.bot = bot
        print("RCS: PARTY MODULE")

    #WELCOME MESSAGES TO PARTIES
    async def on_member_update(self, before, after):
        rolelist_before = [role.id for role in before.roles]
        rolelist_after = [role.id for role in after.roles]
        if rolelist_before == rolelist_after:
            return
        guild = before.guild
        db.member_add_db(guild,after)
        print(rolelist_before)
        print(rolelist_after)

        rolechange = party_role_change(guild, rolelist_before, rolelist_after)

        try:
            if not rolechange[0]:
                return
        except:
            return

        partych = discord.utils.get(guild.text_channels, id=int(db.get_from_party(guild, "role_id", str(rolechange[1]), "channel_id")))

        if rolechange[0] == "added":
            db.member_update_party(guild, after, rolechange[1])
            await partych.send(embed=status.add_party(after.mention))


        if rolechange[0] == "left":
            db.member_update_party(guild, before, None)
            await partych.send(embed=status.left_party(before.mention))


    #NORMAL CMDS
    @commands.command(name='partylist')
    @commands.guild_only()
    async def cmd_partylist(self, ctx):
        """List all the parties in the Database."""
        guild = ctx.guild
        ch = ctx.channel
        try:
            partynames = db.party_list(guild)
            
            if partynames == None:
                await ch.send(embed=status.error("There are no parties! Add an one by doing !partyadd"))
            else:
                await ch.send(embed=status.cmd_partylist(partynames))
            
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)

    @commands.command(name='partyinfo')
    @commands.guild_only()
    async def cmd_partyinfo(self, ctx, party_name: str=None):
        """Get specific information about a party from Database."""
        guild = ctx.guild
        ch = ctx.channel
        try:
            
            if party_name is None:
                await ch.send(embed=status.wrong_input("Provide a party name, you can get an one by doing !partylist."))
                return
            
            #party_name = db.get_from_party(guild, party_name)
            
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)
            
            


    #ADMIN CMDS

    @commands.command(name='partyadd')
    @commands.check(check.check_admin)
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

    @commands.command(name='partyremove')
    @commands.check(check.check_admin)
    @commands.guild_only()
    async def cmd_partyremove(self, ctx, party_name: str=None):
        """Remove a party from the Database."""
        guild = ctx.guild
        ch = ctx.channel
        try:
            
            if party_name is None:
                await ch.send(embed=status.wrong_input("Provide a role name, you can get an one by doing !partylist."))
                return

            print(party_name)

            db.party_remove(guild, party_name)

            await ch.send(embed=status.cmd_partyremove(party_name))
            
            
            print("Removed a party.")
            
        except Exception as e:
            try:   
                await ch.send(embed=status.error(e))
                print(e)
            except:
                print(e)

def setup(bot):
    bot.add_cog(Party(bot))
