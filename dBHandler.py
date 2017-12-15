import sqlite3, cmd, sys 

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
		'Attempt to connect to the specified database'
		self.conn=sqlite3.connect(arg)
		self.cursor=self.conn.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS funcDep(nameTable TEXT NOT NULL,lhs TEXT NOT NULL,rhs TEXT NOT NULL, PRIMARY KEY(nameTable,lhs,rhs))')
		self.conn.commit()
		self.connected = True
		self.databaseName = arg
		self.do_display("")
		print("Succesfully connected to database: " , arg , "!")

	def do_disconnect(self,arg):
		'Disconnect from the actually connected database'
		self.conn.close()
		self.conn = None
		self.cursor = None
		self.connected = False
		self.databaseName = ""
		
	def do_status(self,arg):
		if not self.isConnected():
			return
		print("Connected to database : ", self.databaseName)


	def do_insert(self,arg):
		'Insert a new functional dependency'
		if not self.isConnected():
			return
		res = parse(arg)
		if " " in res[2] :
			print ("error Fd not singulary")
		else:
			self.cursor.execute("INSERT INTO funcDep(nameTable,lhs,rhs) VALUES(?,?,?)",(res[0],res[1],res[2]))
			self.conn.commit()

	def do_execute(self,arg):
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
		'Delete a functional dependency'
		if not self.isConnected():
			return
		try:
			i=int(arg)
			self.cursor.execute("DELETE FROM funcDep WHERE nameTable=? AND lhs=? AND rhs=?",self.index[i])
			self.conn.commit()
		except:
			print("soucis")
	def do_update(self,arg):
		'arg= int(index),(l or r),replace'
		if not self.isConnected():
			return
		res=parse(arg)
		collumn=res[1]
		(x,y,z)=self.index[int(res[0])]
		if collumn=="l":
			self.cursor.execute("UPDATE funcDep SET lhs=? WHERE nameTable=? AND lhs=? AND rhs=?",(res[2],x,y,z))
			self.conn.commit()	
		elif collumn=="r":
			if " " in res[2] :
				print ("error Fd not singulary")
			else :
				self.cursor.execute("UPDATE funcDep SET rhs=? WHERE nameTable=? AND lhs=? AND rhs=?",(res[2],x,y,z))
				self.conn.commit()
		else:
			print("Error")	
		
		
		


	def do_display(self,arg):
		'Display the funcDep table of the database actually connected'
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
		self.cursor.execute("SELECT lhs FROM funcDep WHERE nameTable =?",table)
		res = self.cursor.fetchall()
		l=[]
		i=0
		for row in res:
			l[i]=str(row)[1:-2]
		return l

	def getRHS(self,table):
		'Print RHS from the table given'
		if not self.isConnected():
			return
		self.cursor.execute("SELECT rhs FROM funcDep WHERE nameTable =?",table)
		res = self.cursor.fetchall()
		r=[]
		i=0
		for row in res:
			r[i]=str(row)[1:-2]
		return r


	def isConnected(self):
		if not self.connected:
			print("You are currently not connected to a database")
			return False
		return True

	def getName(self,table):
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
