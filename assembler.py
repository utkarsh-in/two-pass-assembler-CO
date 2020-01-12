""" assembly language program to machine code

USER DOCUMENTATION
Code to convert an assembly language program to machine code
Made by Utkarsh Sharma(2018114) and Ira Aggarwal(2018039)

* The code covers every opcode discussed in the tutorial or in the class.
* You can declare variables using
	DS: declare storage -> specifies how much memory space a varaible has
	DC: declare constant -> specifies the value of the varaible. If no storage is specified, it assumes the storage space to be 4
* Literals used in the assembly code must be precided by the character '$'; e.g. - $5
* Document need not have a START and a END statement. By default no reallocation is done if there is no START. START statement should be followed by the relocation number; e.g. "START 400"
* You can write comments in the assembly language. The statement has to start with '# '
* All variables that store data must be preceded by the character '`'
* Labels are stored at the end of the document. It is upto the compiler to handle this accordingly
"""

import warnings


labels = {}
variables = {}
literal_pool = []
reg_variable_pool = []
labels_location = {}
length_table = {   #TODO: Include any more if length!=3
	"CLA": 2,  
	"STP": 2
}
all_labels_used = []
all_variables_used = []
get_opcode = {
	"CLA" : "0000",
	"LAC" : "0001",
	"SAC" : "0010",
	"ADD" : "0011",
	"SUB" : "0100",
	"BRZ" : "0101",
	"BRN" : "0110",
	"BRP" : "0111",
	"INP" : "1000",
	"DSP" : "1001",
	"MUL" : "1010",
	"DIV" : "1011",
	"STP" : "1100"
}
expected_operands = {
	"0000" : 0,
	"0001" : 1,
	"0010" : 1,
	"0011" : 1,
	"0100" : 1,
	"0101" : 1,
	"0110" : 1,
	"0111" : 1,
	"1000" : 1,
	"1001" : 1,
	"1010" : 1,
	"1011" : 1,
	"1100" : 0
}
label_statements = ["BRZ", "BRN", "BRP"]
variable_statements = ["ADD", "SUB", "DSP", "MUL", "DIV", "INP"]




"""
DEBUGGER DOCUMENTATION
Types of comments in this document
	TODO:  means bug
	TODO-ER: means error handeling required
	ASSUME: means assumption taken, put in read me
	DOUBT: clear doubt, usually followed by solving bug
	IMPROV: scope for improvments
	NOTE: to be remembered
"""

def line_not_comment(line): #IMPROV: very rudementary test! may improve afterwards - may include multiline comments 
	if (line[0]=='#'):
		return False
	return True

def check_for_symbol(line): #NOTE: just checks for labels
	if(line[0][-1]==':'):
		return line[0][:-1]
	else:
		return None

def enter_new_symbol(symbol, line):
	line.pop(0)
	if symbol in labels.keys():
		raise Exception("Label declared twice") 
	labels[symbol] = line
	



def write_temp_file(line, length, lc): 
	writeLine = str(line) + "~" + str(length) + "~" + str(lc)
	#print(writeLine)					#PRINTS ON-SCREEN
	aCode.write(writeLine)				#writes into file
	aCode.write("\n")
	aCode.flush()

def line_declares_variable(line):
	if(line[0]=='DC' or line[0]=='DS'): #ASSUME: basically assuming you either declare constant or declare storage for constant
		return True
	return False

def enter_variable(line): 
	variable = line[1]
	if variable in variables:
		if(line[0]=='DC' and variables[variable][1]!=None):
			raise Exception("Variable declared twice")
		elif (line[0]=='DC' and variables[variable][1]==None):
			variables[variable][1] = line[2]
		elif line[0]=='DS':
			variables[variable][0] = line[2]
	if (line[0]=='DS'):
		variables[variable]=[line[2], None]
	if(line[0]=='DC'):
		variables[variable]=[4,line[2]]  #ASSUME: assuming default storage of 4

def check_for_literal(line): #ASSUME: assume literals are declared as $5
	for i in line:
		if (i[:1]=='$'):
			return int(i[1:])
	return None

def check_for_reg_variable(line): #ASSUME: assume literals are declared as $5
	if (line[0] in variable_statements and line[1][:1]!='$'):
		return line[1]
	return None
def doc_all_labelsANDvariables(line):
	if(line[0] in label_statements and not str(line[1]).isdigit()):
		all_labels_used.append(line[1])
	elif (line[0] in variable_statements and not str(line[1]).isdigit() and line[1][:1]=='`'):
		all_variables_used.append(line[1])
		
def enter_new_literal(literal):
	literal_pool.append(literal)

def getLength(line):
	if (line[0]=='DS'):
		return line[2]
	if (line[0]=='DC'):
		return 4
	if (line[0][-1]==':'):
		return getLength(line.pop[0])
	if  line[0] in length_table:
		return length_table[line[0]]
	return 3

def write_list_to_file(l, aCode):
	for i in l:
		writeLine = ''
		for j in i:
			writeLine += str(j)
			writeLine += '\t'
		aCode.write(writeLine)				#writes into file
		aCode.write("\n")
		aCode.flush()
	aCode.flush()

def binary(num, digits):

	num = int(num)
	ans = ''
	while(num>0):
		ans = str(num%2) + ans
		num = num//2	
	while(len(ans)<digits):
		ans = '0' + ans
	return ans

def raise_label_not_found_error():
	for i in all_labels_used:
		if not i in labels.keys():
			raise Exception("Label used but not declared")

def raise_variable_not_found_error():
	for i in all_variables_used:
		if not i in variables.keys():
			raise Exception("Variable used but not declared")
def raise_reg_variable_not_found_error():
	pass
def check_noOf_operands(temp):
	num = expected_operands[temp[1]]+2
	if(len(temp))<num:
		raise Exception("Not enough operands given")
	if(len(temp))>num:
		raise Exception("Too many operands given")
############################## PASS ONE #######################################################################

print("input file name")
filename = input()
# sample input - C:\Users\Utkarsh\Desktop\assembler\sample_input.txt
# filename = "sample_input.txt"
asmFile = open(filename, "r")			#assembly code file
aCode = open("aCODE.txt","w")		#to store the assembly file with addresses

endPresent = False
start = asmFile.readline()
while(start[0]=='.'):
	start = asmFile.readline()
start = start[:-1]
firstLine = start.split()
startConstant = 0
if firstLine[0]=="START":
	startConstant = int(firstLine[1])  #ASSUME: format - start 4000
else:
	warnings.warn("No START statement found! Assuming start from address 0")
	asmFile.seek(0)

lc = startConstant #location counter
for iline in asmFile:
	line = iline[:-1].split()
	if(line_not_comment(line)):
		if(line[0]=='END'):
			endPresent = True
			break

		symbol = check_for_symbol(line)
		if(symbol!=None):
			enter_new_symbol(symbol, line)
			continue

		if(line_declares_variable(line)):
			enter_variable(line)
			continue

		literal = check_for_literal(line) 
		if(literal!=None):
			enter_new_literal(literal) 
		
		
		reg_variable = check_for_reg_variable(line)
		if(reg_variable!=None):
			reg_variable_pool.append(reg_variable) 

		doc_all_labelsANDvariables(line)

		length = getLength(line)
		write_temp_file(line, length, lc) 
		lc = lc + length
literal_pool.sort()
literal_pool = list(set(literal_pool)) 
reg_variable_pool = list(set(reg_variable_pool))
removeTemp = []
for i in reg_variable_pool:
	if(i in variables.keys()):
		removeTemp.append(i)
for i in removeTemp:
	reg_variable_pool.remove(i)
writeLine = "['STP']~2~"+str(lc)
lc += 2
aCode.write(writeLine)				# Add a 'STP' command so that the label statements are not executed
aCode.write("\n")
aCode.flush()

labels_name = labels.keys()
for i in labels_name:
	line = labels[i]
	length = getLength(line)
	write_temp_file(line, length, lc) 
	labels_location[i] = lc
	lc = lc + length


raise_label_not_found_error()
raise_variable_not_found_error()
raise_reg_variable_not_found_error()
literal_pool += reg_variable_pool
print(reg_variable_pool)
if(endPresent==False):
	warnings.warn("No END statement. Program end assumed at the end of the file")
#TODO: find how to store literal pool values in registers
asmFile.close()
aCode.close()

#################### PASS ONE ENDS ###############################################################

####################### PASS TWO #################################################################


aCodeI = open("aCODE.txt","r")	#assembly code file with addresses
m_code = [] 
obj = open("output.o","w")				#to store only the object code

aCodeI.seek(0)
for iline in aCodeI: 
	line = iline[:-1]
	line = line.split('~')
	curr = line[0][1:-1].split(', ')
	for c in range(len(curr)):
		curr[c] = curr[c][1:-1]
	try:
		opcode = get_opcode[curr[0]] 
	except:
		raise Exception("Illegal opcode")
	temp = []
	temp.append(int(line[2]))
	temp.append(opcode)
	for i in curr:
		if(i!=curr[0]):
			if i in labels: 
				temp.append(labels_location[i])
			elif i in reg_variable_pool:
				temp.append(literal_pool.index(i))
			elif i in variables:
				temp.append(variables[i][1]) #IMPROV: if variable is used then lc should increment with storage of the variable
			elif (i[:1]=='$'):
				temp.append(literal_pool.index(int(i[1:]))) #ASSUME: assume first literal stored in R0 whose address is 0 and so on
			else:
				temp.append(i)
	check_noOf_operands(temp) 
	m_code.append(temp)

print("m_code")
for m in m_code:
	print(m)
for i in range(len(m_code)):
	m_code[i][0] = binary(m_code[i][0], 8)
	for j in range(2, len(m_code[i])):
		m_code[i][j] = binary(m_code[i][j], 8)
write_list_to_file(m_code, obj)


#################### PASS TWO ENDS ###############################################################