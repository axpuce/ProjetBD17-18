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
		self.conn=sqlite3.connect(arg[1])
		self.cursor=self.conn.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS funcDep(nameTable TEXT NOT NULL,lhs TEXT NOT NULL,rhs TEXT NOT NULL, PRIMARY KEY(nameTable,lhs,rhs))')
		self.conn.commit() 

	def do_insert(self,arg):#insert est un triplet (nameTable,lhs,rhs)
		self.cursor.execute("INSERT INTO funcDep(nameTable,lhs,rhs) VALUES(?,?,?)",arg[1:4])
		self.conn.commit()
	

	def do_delete(self,arg):	
		self.cursor.execute("DELETE FROM funcDep WHERE nameTable=? AND lhs=? AND rhs=?",arg[1:3])
		self.conn.commit()
	def do_display(self,arg):
		'Display the funcDep table of the database actually connected'
		for row in cursor.execute("SELECT * from funcDep ORDER BY nameTable"):
			print(row)
def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
	dBHandler().cmdloop()
