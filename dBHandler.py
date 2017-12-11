import sqlite3, cmd, sys
class dBHandler(cmd.Cmd) :
	intro = 'Welcome to the database handler. type help or ? to list commands/n'
	prompt = '(dbhandler)'
	file = None
	database = ''
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.cursor = None
		self.conn = None

	def do_connect(self,arg):
		'Attempt to connect to the specified database'
		self.conn=sqlite3.connect(arg)
		self.cursor=self.conn.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS funcDep(nameTable TEXT NOT NULL,lhs TEXT NOT NULL,rhs TEXT NOT NULL, PRIMARY KEY(nameTable,lhs,rhs))')
		self.conn.commit() 


	def do_insert(self,arg):#insert est un triplet (nameTable,lhs,rhs)
		res = parse(arg)
		self.cursor.execute("INSERT INTO funcDep(nameTable,lhs,rhs) VALUES(?,?,?)",(res[0],res[1],res[2]))
		self.conn.commit()

	def do_delete(self,arg):	
		res = parse(arg)
		self.cursor.execute("DELETE FROM funcDep WHERE nameTable=? AND lhs=? AND rhs=?",(res[0],res[1],res[2]))
		self.conn.commit()


	def do_display(self,arg):
		'Display the funcDep table of the database actually connected'
		for row in self.cursor.execute("SELECT * from funcDep ORDER BY nameTable"):
			print(row)	

	def do_getLHS(self,arg):
		self.cursor.execute("SELECT lhs FROM funcDep WHERE nameTable =?",parse(arg))
		res = self.cursor.fetchall()
		print(res)

	def do_getRHS(self,arg):
		self.cursor.execute("SELECT rhs FROM funcDep WHERE nameTable =?",parse(arg))
		res = self.cursor.fetchall()
		print(res)



def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(str, arg.split(" ")))

if __name__ == '__main__':
	dBHandler().cmdloop()
