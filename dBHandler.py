import sqlite3, cmd, sys
class dBHandler(cmd.Cmd) :
	intro = "Welcome to the database handler. type help or ? to list commands\nYou should connect to a database using \"connect\" to start"
	prompt = '(dbhandler)'
	database = ''
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.cursor = None
		self.conn = None
		self.connected = False

	def do_connect(self,arg):
		'Attempt to connect to the specified database'
		self.conn=sqlite3.connect(arg)
		self.cursor=self.conn.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS funcDep(nameTable TEXT NOT NULL,lhs TEXT NOT NULL,rhs TEXT NOT NULL, PRIMARY KEY(nameTable,lhs,rhs))')
		self.conn.commit()
		self.connected = True
		print("Succesfully connected to database: " + arg + "!")


	def do_insert(self,arg):
		'Insert a new functional dependency'
		if not self.isConnected():
			return
		res = parse(arg)
		self.cursor.execute("INSERT INTO funcDep(nameTable,lhs,rhs) VALUES(?,?,?)",(res[0],res[1],res[2]))
		self.conn.commit()

	def do_delete(self,arg):
		'Delete a functional dependency'
		if not self.isConnected():
			return
		res = parse(arg)
		self.cursor.execute("DELETE FROM funcDep WHERE nameTable=? AND lhs=? AND rhs=?",(res[0],res[1],res[2]))
		self.conn.commit()


	def do_display(self,arg):
		'Display the funcDep table of the database actually connected'
		if not self.isConnected():
			return
		for row in self.cursor.execute("SELECT * from funcDep ORDER BY nameTable"):
			print(row)

	def do_getLHS(self,arg):
		'Print LHS from the table given'
		if not self.isConnected():
			return
		self.cursor.execute("SELECT lhs FROM funcDep WHERE nameTable =?",parse(arg))
		res = self.cursor.fetchall()
		print(res)

	def do_getRHS(self,arg):
		'Print RHS from the table given'
		if not self.isConnected():
			return
		self.cursor.execute("SELECT rhs FROM funcDep WHERE nameTable =?",parse(arg))
		res = self.cursor.fetchall()
		print(res)







	def isConnected(self):
		if not self.connected:
			print("You are currently not connected to a database")
			return False
		return True

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(str, arg.split(" ")))

if __name__ == '__main__':
	dBHandler().cmdloop()
