def is3nf(self,table):
	if self.allP(table)==True or self.allK(table)==True:
		return True
	return False

def allP(self,table):
	Pr=self.getP(table)
	names=self.getName(table)
	for n in names:
		in=false
		for p in Pr:
			if p==n:
				in=True
				break
		if in==False:
			return False
	return True

def allK(self,table):
	l=self.getLHS(table)
	keys=self.getKeys(table)
	for att in l:
		in=false
		for k in keys:
			if att==k:
				in=True
				break
		if in==False:
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


