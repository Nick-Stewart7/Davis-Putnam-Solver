import os
import sys

def DavisPutnam(atoms, clauses):
	values = {}
	for atom in atoms:
		values[atom] = 0
	return DPHelper(atoms, clauses, values)
	
def SingleLiteral(S):
	for clause in S:
		if len(clause) == 1:
			return clause[0]
	return None
			
def SameSignedLiteral(atoms, S):
	for atom in atoms:
		atomPresent = False
		onlyTrue = True
		onlyFalse = True
		for clause in S:
				for literal in clause:
					if abs(literal) == atom:
						atomPresent = True
						if literal > 0:
							onlyFalse = False
						if literal < 0:
							onlyTrue = False
				
		if onlyTrue and atomPresent:
			return (atom,1)
		if onlyFalse and atomPresent:
			return (atom,-1)
	return None	
					
def propagator(S, values):
	satisfied_clauses = []
	for value_pair in values.items():
		for clause in S:
			satisfied = False
			for i in range(0, len(clause)):
				if abs(clause[i]) == value_pair[0]:
					if value_pair[1] > 0:
						if clause[i] > 0:
							satisfied = True
					elif value_pair[1] < 0:
						if clause[i] < 0:
							satisfied = True
						
			if satisfied:
				satisfied_clauses.append(clause)
	for clause in satisfied_clauses:
		S.remove(clause)
	return S 	

def DPHelper(atoms, S, values):
	stuck = False
	while True:
		if(S == []):
			#we have statified every clause and have popped it off the stack
			#assign all remaning unbound atoms to T or F arbitrarily
			for atom in atoms:
				if values[atom] == 0:
					values[atom] = 1
			return values
		SSL = SameSignedLiteral(atoms, S)
		if(SSL):
			#some literal L appears in S with only one sign
			#assign this atom the value of its sign (T/F)
			if values[SSL[0]] == 0:
				values[SSL[0]] = SSL[1]
		L = SingleLiteral(S)
		if(L):
			#a clause in S is a single literal
			#assign T/F appropriately since it must be satisfied
			if L > 0:
				l = abs(L)
				values[l] = 1
			if L < 0:
				l = abs(L)
				values[l] = -1
		
		#propagate assignment in S
		#means if there exists a literal L in S with 1 sign or single literal L in S 		assign all other clauses containing L in S the value assigned.
		# conditional break if S hasnt changed
		SNEW = S.copy()
		S = propagator(S, values)
		if SNEW == S:
			break
	#outside the loop
	for atom in values.items():
		if atom[1] == 0:
			break
	if atom[1] == 1 or atom[1] == -1:
		values[atom[0]] == 0
		return None
	SC = S.copy()
	VC = values.copy()
	VC[atom[0]] = 1 #true
	#PROPAGATE IN SC
	SC = propagator(SC, VC)
	VNEW = DPHelper(atoms, SC, VC)
	if (VNEW != None):
		return VNEW
	values[atom[0]] = -1 #false
	#PROPAGATE IN S
	#print(S)
	S = propagator(S, values)
	#print(S)
	return DPHelper(atoms, S, values)
		
	

def main():
	clause_list = []
	footer = []
	atoms = []
	afterZero = False
	input_file_name = sys.argv[1]
	input_file = open(input_file_name, 'r')
	for line in input_file.readlines():
		line = line.replace('\n','')
		if line == "0":
			afterZero = True
		if afterZero:
			footer.append(line)
			continue
		clause = []
		line_elements = line.split()
		for element in line_elements:
			element = int(element)
			clause.append(element)
			atom = abs(element)
			if atom not in atoms:
				atoms.append(atom)
		clause_list.append(clause)
				
	print("ATOMS: ", atoms)
	print("CLAUSES: ", clause_list)
	
	result = DavisPutnam(atoms, clause_list)
	if result == None:
		print("No Solution Found")
	else:
		print("Solution Found!")
		for kv in result.items():
			if kv[1] > 0:
				print(kv[0], "true")
			elif kv[1] < 0:
				print(kv[0], "false")
			else:
				print(kv[0], "UNBOUND")	
	for item in footer:
		print(item)
	return 0
	

if __name__ == "__main__":
    main()
