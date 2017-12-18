import sqlite3, cmd, sys
from itertools import chain, combinations

class dBHandler(cmd.Cmd) :
    intro = "Welcome to the database handler. type help or ? to list commands\nYou should connect to a database using \"connect\" to start"
    prompt = '(dbhandler)'
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.cursor = None
        self.conn = None
        self.connected = False
        self.databaseName = ""
        self.index=[]

    def do_connect(self,arg):
        'Attempt to connect to the specified database\narg= DatabaseName. Create the databse if it don\'t already exist'
        self.conn=sqlite3.connect(arg)
        self.cursor=self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS funcDep(nameTable TEXT NOT NULL,lhs TEXT NOT NULL,rhs TEXT NOT NULL, PRIMARY KEY(nameTable,lhs,rhs))')
        self.conn.commit()
        self.connected = True
        self.databaseName = arg
        self.do_display("")
        print("Succesfully connected to database: " , arg , "!")

    def do_disconnect(self,arg):
        'Disconnect from the actually connected database\nNo argument'
        self.conn.close()
        self.conn = None
        self.cursor = None
        self.connected = False
        self.databaseName = ""

    def do_status(self,arg):
        'Display the status of the database\nNo argument'
        if not self.isConnected():
            return
        print("Connected to database : ", self.databaseName)


    def do_insert(self,arg):
        'Insert a new functional dependency\n arg = tablename, lhs, rhs'
        if not self.isConnected():
            return
        res = parse(arg)
        if not self.isIn(res[0],res[2]):
            print(res[2]," is not in table")
            return
        attlhs=res[1].split()
        for a in attLhs:
            if not self.isIn(res[0],a):
                print(a," is not in table")
                return

        if " " in res[2] :
            print ("error Fd not singulary")
        else:
            self.cursor.execute("INSERT INTO funcDep(nameTable,lhs,rhs) VALUES(?,?,?)",(res[0],res[1],res[2]))
            self.conn.commit()

    def do_execute(self,arg):
        'Execute the sql request given in argument\nargument being a sql request'
        if not self.isConnected():
            return
        try:
            self.cursor.execute(arg)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print("invalid request",e)
        except sqlite3.IntegrityError as e:
            print(e)


    def do_delete(self,arg):
        'Delete a functional dependency\nnumber of the line to delete'
        if not self.isConnected():
            return
        try:
            i=int(arg)
            self.cursor.execute("DELETE FROM funcDep WHERE nameTable=? AND lhs=? AND rhs=?",self.index[i])
            self.conn.commit()
        except:
            print("error")
    def do_update(self,arg):
        'arg= int(index),(l or r), replace.  replace being the now string to update'
        if not self.isConnected():
            return
        res=parse(arg)
        collumn=res[1]
        (x,y,z)=self.index[int(res[0])]
        if collumn=="l":
            attlhs=res[2].split()
            for a in attlhs:
                if not self.isIn(x,a):
                    print(a," is not in table")
                    return
            self.cursor.execute("UPDATE funcDep SET lhs=? WHERE nameTable=? AND lhs=? AND rhs=?",(res[2],x,y,z))
            self.conn.commit()
        elif collumn=="r":
            if not self.isIn(x,res[2]):
                print(res[2]," is not in table")
                return
            if " " in res[2] :
                print ("error Fd not singulary")
            else :
                self.cursor.execute("UPDATE funcDep SET rhs=? WHERE nameTable=? AND lhs=? AND rhs=?",(res[2],x,y,z))
                self.conn.commit()
        else:
            print("Error")





    def do_display(self,arg):
        'Display the funcDep table of the database actually connected\ntakes no argument'
        if not self.isConnected():
            return
        i=0
        self.index=[]
        for row in self.cursor.execute("SELECT * from funcDep ORDER BY nameTable"):
            print(row, "(",i,")")
            self.index.append(row)
            i+=1







    def getLHS(self,table):
        'Print LHS from the table given'
        if not self.isConnected():
            return
        self.cursor.execute("SELECT lhs FROM funcDep WHERE nameTable =?", table)
        res = self.cursor.fetchall()
        l=[]
        for row in res:
            l.append(str(row)[1:-2])
        return l

    def getRHS(self,table):
        'Print RHS from the table given'
        if not self.isConnected():
            return
        self.cursor.execute("SELECT rhs FROM funcDep WHERE nameTable =?",table)
        res = self.cursor.fetchall()
        r=[]
        for row in res:
            r.append(str(row)[1:-2])
        return r


    def isConnected(self):
        if not self.connected:
            print("You are currently not connected to a database")
            return False
        return True

    def getName(self,table):
        table = str(table)
        res=self.cursor.execute("select * from "+table)
        return list(map(lambda x:x[0] ,self.cursor.description))


    def isIn(self,table,att):
        name=self.getName(table)
        for n in name:
            if n==att:
                return True
        return False


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(str, arg.split(",")))

if __name__ == '__main__':
    dBHandler().cmdloop()

"""
    Le commentaire qui suit est un prémisse de code pour vérifier si une table est en 3NF.
    En partant du principe que getKeys(self,table) existe et retourne un tableau contenant les clés.

"""
"""

def is3nf(self,table):
    if self.allP(table)==True or self.allK(table)==True:
        return True
    return False

def allP(self,table):
    Pr=self.getP(table)
    names=self.getName(table)
    for n in names:
        ok=false
        for p in Pr:
            if p==n:
                ok=True
                breakh
        if ok==False:
            return False
    return True

def allK(self,table):
    l=self.getLHS(table)
    keys=self.getKeys(table)
    for att in l:
        ok=false
        for k in keys:Il
            if att==k:
                ok=True
                break
        if ok==False:
            return False
    return True

def getP(self,table)
    keys=self.getKeys(table)
    pr=[]
    for k in keys:
        tab=parse[k]
        for att in tab:
            pr.append(att)
    return pr

"""
