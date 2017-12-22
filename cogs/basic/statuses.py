import discord
import datetime

timestamp = datetime.datetime.utcnow()

def online_debug():
    embed = discord.Embed(title="RCS-462 ONLINE", description="Booted up successfully.", color=discord.Color.green())
    return embed

def error(error):
    embed = discord.Embed(title="ERROR! An exception has occurred!", description=str(error), color=discord.Color.red())
    embed.set_footer(text="If the problem persists, contact @jensolaf#9386")
    return embed

def wrong_input(solution):
    embed = discord.Embed(title="Wrong Input", description=str(solution), color=discord.Color.red())
    embed.set_footer(text="If the problem persists, consult the manual by saying !help or contact @jensolaf#9386")
    return embed


# PARTY

party_mod = "@ "+str(timestamp)+" by Party Module."

def add_party(member):
    embed = discord.Embed(title="A member has joined the party!", description=member+" has joined the party.", color=discord.Color.green())
    embed.set_footer(text=party_mod)
    return embed

def left_party(member):
    embed = discord.Embed(title="A member has left the party!", description=member+" has left the party.", color=discord.Color.red())
    embed.set_footer(text=party_mod)
    return embed

def left_server(member):
    embed = discord.Embed(title="A member has left the server!", description=member+" has left the server.", color=discord.Color.red())
    embed.set_footer(text=party_mod)
    return embed

def cmd_partyadd(role_m, leader_role_m, color, channel):
    embed = discord.Embed(title="New party has been added to the Database!", description=role_m+" with the leader being "+leader_role_m+" with a channel of "+channel+" has been added to the database!", color=color)
    embed.set_footer(text=party_mod)
    return embed


def cmd_partyremove(party_name):
    embed = discord.Embed(title="Party has been removed from the Database!", description=party_name+" has been removed from the database and is no longer included in corresponding features.", color=discord.Color.blue())
    embed.set_footer(text=party_mod)
    return embed

def cmd_partyinfo(party_name):
    
    embed = discord.Embed(title="Info of "+party_name+":", description=party_name+"", color=discord.Color.blue())
    embed.set_footer(text=party_mod)
    return embed

def cmd_partylist(partylist):
    partystring = ""
    if type(partylist) == str:
        partylist = [partylist]
    for party in partylist:
        partystring+=party+"\n"
        
    embed = discord.Embed(title="List of parties("+str(len(partylist))+"):", description=partystring, color=discord.Color.blue())
    embed.set_footer(text=party_mod)
    return embed

# CMD MEMBER

def cmd_membercheck(count):
    embed = discord.Embed(title="Database has been refreshed!", description="Memberdata for all "+str(count)+" members has been updated.", color=discord.Color.blue())
    return embed

