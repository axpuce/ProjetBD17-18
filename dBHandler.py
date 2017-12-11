import sqlite3
class dBHandler :

	def __init__(self,database):
		self.conn=sqlite3.connect(database)
		self.cursor=self.conn.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS funcDep(nameTable TEXT NOT NULL,lhs TEXT NOT NULL,rhs TEXT NOT NULL, PRIMARY KEY(nameTable,lhs,rhs))')
		self.conn.commit()
	

	def insert(self,insert):#insert est un triplet (nameTable,lhs,rhs)
		self.cursor.execute("INSERT INTO funcDep(nameTable,lhs,rhs) VALUES(?,?,?)",insert)
		self.conn.commit()
	

	def delete(self,remove):	
		self.cursor.execute("DELETE FROM funcDep WHERE nameTable=? AND lhs=? AND rhs=?",remove)
		self.conn.commit()


