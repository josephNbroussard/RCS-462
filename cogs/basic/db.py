import sqlite3
import sys
import datetime
import discord
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
mult_req = False
count = 0
db_pub = []

#conn=sqlite3.connect(":memory:")
#c=conn.cursor()

# TABLES
def new_db(guild):
    global conn, c
    
    conn=sqlite3.connect(".\\database\\"+str(guild.id)+".db")
    c=conn.cursor()
    
    sample = '.\\database\\database_guide'

    try:
        with open(sample) as fp:
            line = fp.readline()
            while line:
                c.execute(str(line.strip()))
                #print("Line: {}".format(line.strip()))
                line = fp.readline()
    except sqlite3.OperationalError:
        print("Table already exists.")
        

# BASIC ACTIONS

def insert(guild, check, table, value,value2=None,value3=None,value4=None,value5=None,value6=None,value7=None,value8=None,value9=None):

    try:

        try:
            conn=sqlite3.connect(".\\database\\"+str(guild.id)+".db")
            c=conn.cursor()
        except Exception as e:
            print(e)

        #print("INSERTING...")

        if check is True:
            try:
                name = c.execute("SELECT * FROM "+str(table))
                names = [description[0] for description in c.description]
                a = (value,)
                #print(names)

                items = [item[0] for item in c.execute("SELECT * FROM "+str(table)+" WHERE "+str(names[0])+" = ?", a)]

                #print(items)

                try:
                    #print("Trying")
                    if str(items[0]) == str(value):
                        #print("DB.INSERT.CHECK: CHECK IS POSITIVE. RETURNING.")
                        return
                except:
                    #print("DB.INSERT: CHECK IS NEGATIVE. GOING ON..")
                    pass
                    
            except:
                raise
                print("Error:", sys.exc_info()[1])

        print("CHECKDONE")

                
        
        t = (value, value2, value3, value4, value5, value6, value7, value8, value9)
        while True:
            q = 'INSERT INTO '+str(table)+' VALUES (' + ','.join(('?',) * (len(t))) + ')'
            try:
                c.execute(q, t)
                break
            except:
                t = t[:-1]
                if len(t) == 1:
                    raise Exception("Wrong input")

            

        conn.commit()
        #print("DB.INSERT: Done inserting new values to the DB!")
    except Exception as e:
        raise e
                                        
def update(guild, table, column_by, value_by, column_to, value_to):

    try:
    
        conn=sqlite3.connect(".\\database\\"+str(guild.id)+".db")
        c=conn.cursor()

        #if str(column_by) == "default":
        #    name = c.execute("SELECT * FROM "+str(table))
        #    names = [description[0] for description in c.description]
        #    column_by = names[0]

        params = (value_to, value_by)

        c.execute("UPDATE "+str(table)+" SET {} = ? WHERE {} = ?".format(column_to,column_by), params)
        

        conn.commit()
        #print("DB.UPDATE: Done updating values!")

    except Exception as e:
        raise e
    

def delete(guild, table, column_by, value_by):

    try:

        conn=sqlite3.connect(".\\database\\"+str(guild.id)+".db")
        c=conn.cursor()

        c.execute("DELETE FROM {} WHERE {}=?".format(table, column_by), (value_by,))

        conn.commit()
        #print("DB.DELETE: Done deleting values!")
    except Exception as e:
        raise e

def select(guild, table, column_by, value_by, column_to, multi=False):

    try:
    
        conn=sqlite3.connect(".\\database\\"+str(guild.id)+".db")
        c=conn.cursor()

        if not multi:
            sql = "SELECT {} FROM {} WHERE {}=?".format(column_to, table, column_by)
            #print(sql)
            selection = [item[0] for item in c.execute(sql, (value_by,))]
        if multi:
            get = c.execute("SELECT {} FROM {}".format(column_by,table))
            selection = [item[0] for item in get]        

        #print("DB.SELECT: Done selecting!")
        try:
            #print(len(info))
            if int(len(selection)) == 1:
                return selection[0]
            if int(len(selection)) > 1:
                return selection
        except:
            return None

    except Exception as e:
        raise e

# CACHE
  
def cache_update(guild, item, value):
    try:
        update(guild, "cache", "item", item, "value")
    except Exception as e:
        raise e
    
def cache_getadd(guild, item, def_value=None):
    try:
        insert(guild, True, "cache", item, str(def_value))
        value = select(guild, "cache", "item", str(item), "value")

        return value
    except Exception as e:
        raise e
    
# MEMBER
    # GENERAL

def get_from_member(guild, by_column, by_item, column):
    try:
        get = select(guild, "member", str(by_column), str(by_item), str(column))
                     
        if get is None:
            #print("Nothing to get.")
            return False
        else:
            return get
    except Exception as e:
        print(e)

def if_member_in_db(guild,member):
    try:
        get = select(guild, "member", "id", str(member.id), "id")

        if get is None:
            #print("User not in DB")
            return False
        else:
            #print("User in DB")
            return True
        
    except Exception as e:
        raise e

def member_add_db(guild,member):
    try:
        insert(guild, True, "member", str(member.id))
    except Exception as e:
        raise e
    
def member_update_party(guild, member, party_role_id):
    try:
        if party_role_id == int:
            party_role_id = str(party_role_id)
        print("UPDATING "+str(party_role_id))
        update(guild, "member", "id", str(member.id), "party_role_id", party_role_id)
    except Exception as e:
        raise e
    
    # INACTIVITY CONTROL

def member_update_date(ctx):
    try:
        member = ctx.author
        update(ctx.guild, "member", "id",str(member.id),"last_msg",str(ctx.created_at))
    except Exception as e:
        raise e
# PARTY

def get_party_role(guild, party_name):
    try:
        role_id = select(guild, "party", "name", str(party_name), "role_id")
        role = discord.utils.get(guild.role, id=int(role_id))
        return role
    except Exception as e:
        raise e

def party_remove(guild, party_name):
    try:
        delete(guild, "party", "name", str(party_name))
    except Exception as e:
        raise e

def party_ids(guild,idlist,party_ids):
    try:
        print("COMPARING")
        print("IDLIST: "+str(idlist))
        print("PARTY_IDS: "+str(party_ids))
        party_id = None
        for id1 in idlist:
         for id2 in party_ids:
             if int(id1) == int(id2):
                 party_id = id1
        #print(party_id)
        return party_id
    except Exception as e:
        raise e
          
def party_list(guild):
    try:
        conn=sqlite3.connect(".\\database\\"+str(guild.id)+".db")
        c=conn.cursor()

        get = select(guild, "party", "name", None, None, True)
        
        print("get:"+str(get))
        return get
    except Exception as e:
        print(e)

def new_party(guild, role_id, leader_role_id, name, color, channel_id):
    print("Adding a new party..")
    try:
        insert(guild, True, "party", str(role_id), str(leader_role_id), str(name), str(color), str(channel_id))
        print("New party has been added to the DB!")
    except Exception as e:
        print(e)
    

def get_from_party(guild, by_column, by_item, column):
    try:
        get = select(guild, "party", str(by_column), str(by_item), str(column))
                     
        if get is None:
            #print("Nothing to get.")
            return False
        else:
            return get
    except Exception as e:
        print(e)
        
