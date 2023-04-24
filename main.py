import json
import os
import shutil
import re
from pprint import pprint

"""ULDANA SHYNDALI
ushyndali@mail.tu
nfactorial 2023
"""

commands=[""]
types=["INT", "STR", "BOOL", "FLOAT"]
constraints=["PRIMARYKEY", "NOTNULL", "NONE"]


def get_json(filename):
    for folder in os.listdir('.'):
        if os.path.exists("{}/{}.json".format(folder,filename)):
             with open("{}/{}.json".format(folder, filename), "r") as file:
                 cur_table=json.load(file)
                 return cur_table
    #getting json object everytime by table name

def check_type(value, type):
    if type=="INT" and re.match(r"[0-9]+",value):
        return int(value)
    elif type=="STR" and re.match(r"[a-zA-Z]+",value):
        return str(value)
    elif type=="BOOL" and re.match(r"False|True",value):
        return bool(value)
    elif type=="FLOAT" and re.match(r"[0-9]+.[0-9]+",value):
        return float(value)
    else:
        return "error"
    #checking if we can insert values into table with correctness of corresponding data types

def check_conditions(table, ind, conditions):
    conditions2=[]
    for i,element in enumerate(conditions):
        conditions2.append(element.split("="))
        if re.match(r"'.*'", conditions2[i][1]):
            conditions2[i][1]=conditions2[i][1][1:-1]

    for key in list(table.keys()):
        for cond in conditions2:
            if key==cond[0]:
                if table[key][ind]==cond[1]:
                    continue
                else:
                    return False
                
    return True
    #checking conditions for select/delete/update method, returns true if we should print/alter the row

def create_db(db_name):
    if os.path.isdir(db_name):
        pass
    else:
        os.mkdir(db_name)

def create_table():
    new_t={}
    new_column=[]
    get_col=""
    while get_col!=")":
        get_col=input()
        if get_col==")":
            continue
        if re.match(r"[a-z]+ (INT|BOOL|STR|FLOAT) (PRIMARYKEY|NOTNULL),", get_col):
            new_column=get_col.split(" ") 
            new_t[new_column[0]]=[new_column[1], new_column[2][:-1]]
        elif re.match(r"[a-z]+ (INT|BOOL|STR|FLOAT),", get_col):
            new_column=get_col.split(" ") 
            new_t[new_column[0]]=[new_column[1][:-1], "NONE"]
        else:
            raise Exception("invalid comand")
            
        try:
            with open("{}/{}.json".format(commands[4], commands[2]), "w") as file:
                json.dump(new_t, file, indent=2)
        except:
            print("error has ocurred")

def drop_db(db_name):
    if os.path.isdir(db_name):
        shutil.rmtree(db_name)

def drop_table(tb_name):
    for folder in os.listdir('.'):
        if os.path.exists("{}/{}.json".format(folder,tb_name)):
            os.remove("{}/{}.json".format(folder,tb_name))

def select():
    commands=cmnd.split(" ")
    conditions=[]
    order=0
    ordercol=""
    columns=[]
    table=get_json(commands[3])
    
    if re.findall(r"[a-z]+='[A-Za-z]+'|[a-z]+=[0-9]+",cmnd):
        conditions=re.findall(r"[a-z]+='[A-Za-z]+'|[a-z]+=[0-9]+",cmnd)
    if re.findall(r"ORDER BY [a-z]+ ASC|ORDER BY [a-z]+ DESC", cmnd):
        if commands[-1]=="ASC":
            order=1
        else:
            order=-1
    if commands[1]=="*":
        columns=list(table.keys())
    else:
        columns=commands[1].split(",")
    
    ordercol=commands[-2]

    n=len(table[list(table.keys())[0]])

    if order!=0:
        for i in range(2,n-1):
            for j in range(i+1,n):
                if(order==1 and table[ordercol][i]>table[ordercol][j]) or (order==-1 and table[ordercol][i]<table[ordercol][j]):
                    for key in list(table.keys()):
                        table[key][i],table[key][j]=table[key][j],table[key][i]

    for key in columns:
        print("|"+key+"|", end="")
    print("")
    for i in range(2,n):
        if not check_conditions(table, i, conditions):
            continue
        for key in list(table.keys()):
            if key in columns:
                print(table[key][i], end="|")
        print("")

def insert(table_n, columns, values):
    table=get_json(table_n)
    for column in columns:
        if column in table:
            continue
        else:
            raise Exception("no such column!")
            
    for key in list(table.keys()):
        type=table[key][0]
        constraint=table[key][1]
        if key in columns:
            value=values[columns.index(key)]
            if check_type(value,type)=="error":
                raise Exception("invalid data type!")
            else:
                if constraint=="PRIMARYKEY":
                    for i,n in enumerate(table[key]):
                        if i==0 or i==1:
                            continue
                        if n==value:
                            raise Exception("cannot set not unique value")
        else:
            if constraint=="NOTNULL":
                raise Exception("cell cannot be empty")
            
    for key in list(table.keys()):
        if key in columns:
            value=values[columns.index(key)]
            table[key].append(value)
        else:
            table[key].append("NULL")

    for folder in os.listdir('.'):
        if os.path.exists("{}/{}.json".format(folder,table_n)):
            with open("{}/{}.json".format(folder, table_n), "w") as file:
                json.dump(table, file, indent=2)

def delete():
    commands=cmnd.split(" ")
    table=get_json(commands[2])
    conditions=commands[4].split(",")
    n=len(table[list(table.keys())[0]])
    for i in range (2,n):
        if check_conditions(table, i, conditions):
            for key in list(table.keys()):
                table[key].pop(i)

    for folder in os.listdir('.'):
        if os.path.exists("{}/{}.json".format(folder,commands[2])):
            with open("{}/{}.json".format(folder, commands[2]), "w") as file:
                json.dump(table, file, indent=2)

def update():
    commands=cmnd.split(" ")
    table=get_json(commands[1])
    conditions=commands[3].split(",")
    set=input()
    updlist=set.split(" ")[1].split(",")
    updlist2=[]
    for i,n in enumerate(updlist):
        updlist2.append(updlist[i].split("="))
        if re.match(r"'.*'", updlist2[i][1]):
            updlist2[i][1]=updlist2[i][1][1:-1]
    n=len(table[list(table.keys())[0]])
    for i in range (2,n):
        if check_conditions(table, i, conditions):
            for key in list(table.keys()):
                for upd in updlist2:
                    if upd[0]==key:
                        table[key][i]=upd[1]

    for folder in os.listdir('.'):
        if os.path.exists("{}/{}.json".format(folder,commands[1])):
            with open("{}/{}.json".format(folder, commands[1]), "w") as file:
                json.dump(table, file, indent=2)

    
        
    

cmnd=""

while cmnd!="stop":
    cmnd=input()
    if re.match(r"CREATE TABLE [A-Za-z0-9]+ IN [A-Za-z0-9]+ [^0-9A-Za-z]",cmnd):
        commands=cmnd.split(" ")
        create_table()
    elif re.match(r"CREATE DATABASE [A-Za-z0-9]+",cmnd):
        commands=cmnd.split(" ")
        create_db(commands[2])    
    elif re.match(r"DROP DATABASE [A-Za-z0-9]+",cmnd):
        commands=cmnd.split(" ")
        drop_db(commands[2])
    elif re.match(r"DROP TABLE [A-Za-z0-9]+",cmnd):
        commands=cmnd.split(" ")
        drop_table(commands[2])
    elif re.match(r"SELECT .* FROM [A-Za-z0-9]+",cmnd):
        select()
    elif re.match(r"INSERT INTO [A-Za-z0-9]+ \([0-9a-zA-Z,]+\) VALUES \([0-9a-zA-Z,]+\)", cmnd):
        commands=cmnd.split(" ")
        columns=commands[3][1:-1].split(",")
        values=commands[5][1:-1].split(",")
        insert(commands[2], columns, values)
    elif re.match(r"UPDATE [A-Za-z0-9]+ WHERE [a-z]+='[A-Za-z]+'|UPDATE [A-Za-z0-9]+ WHERE [a-z]+=[0-9]+",cmnd):
        update()
    elif re.match(r"DELETE FROM [A-Za-z0-9]+ WHERE [a-z]+='[A-Za-z]+'|DELETE FROM [A-Za-z0-9]+ WHERE [a-z]+=[0-9]+",cmnd):
        delete()
    elif commands[0]!="stop":
        print("incorrect command")
        break