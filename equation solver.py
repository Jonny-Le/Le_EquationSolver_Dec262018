import math #math.factorial()

"""
	Gets user-inputted expression
"""
def get_expression():		
	expression = input("Enter your mathematical expression: ")
	return expression

"""
	Formats the expression; splits values and symbols
"""
def exp_split(expression):
	exp_format = ""	#Assign blank string as final formatted expression
	for i in range(0, len(expression)):
		if expression[i] in  ["+", "-", "*", "/", "%", "^", "!", "(", ")", "[", "]", "{", "}"]:
			exp_format = exp_format + " " + expression[i] + " "	#If current index is symbol, add one space to the index before and after symbol
		if expression[i] in  ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:	#If numbers, adds to string
			exp_format += expression[i]
		#If expression contains invalid characters, return false
		if expression[i] not in ["0","1","2","3","4","5","6","7","8","9","+","-","*","/","%","^","!","(",")", "[", "]", "{", "}", ".", " "]:
			return "false"

	return exp_format.split() #Returns split expression

"""
	Makes sure that brackets are in order and logical 
"""
def bracket_order(expression):
	exp_tmp = "" #Temporarily writes all characters of expression
	for i in range(0, len(expression)):
		exp_tmp += expression[i] 
		
	#Checks if there are enough brackets, sharp and square brackets can only appear once and have a corresponding end bracket
	if exp_tmp.count("{") > 1 or exp_tmp.count("{") != exp_tmp.count("}"):
		return "false"
	if exp_tmp.count("[") > 1 or exp_tmp.count("[") != exp_tmp.count("]"):
		return "false"
	if exp_tmp.count("(") != exp_tmp.count(")"):
		return "false"
  
	#Checks for square brackets and parentheses in sharp brackets
	exp_cmp = "" #Used for comparision
	for i in range(0, len(exp_tmp)):
		if exp_tmp[i] == "{":	
			#If sharp bracket encountered, set sub string to all values inside 
			while True:
				exp_cmp += exp_tmp[i]	#Adds current index value to substring
				if exp_tmp[i] == "}":
					break #Exits loop if index is ending sharp bracket
				#Returns false if no sharp bracket is found
				if i == len(exp_tmp) - 1: 
					return "false"
				i += 1
				
			#If sub string does not contain square brackets and parentheses inside, expression is invalid, returns "false"
			if exp_cmp.count("{") != 1 or exp_cmp.count("{") != exp_cmp.count("}"):
				return "false"
			if exp_cmp.count("[") != 1 or exp_cmp.count("[") != exp_cmp.count("]"):
				return "false"
			if exp_cmp.count("(") != exp_cmp.count(")"):
				return "false"
		
	#Checks for parentheses in square brackets
	exp_cmp = ""
	for i in range(0, len(exp_tmp)):
		#If square bracket encountered, set sub string to all values inside square brackets
		if exp_tmp[i] == "[":
			while True:
				exp_cmp += expression[i]	#Adds current index value to substring
				if exp_tmp[i] == "]":
					break
				#Returns false if no ending square bracket is found
				if i == len(exp_tmp) - 1:
					return "false"
				i += 1	#Increases index
				
			#Square brackets must contain at least one pair of parentheses
			if exp_cmp.count("[") != 1 or exp_cmp.count("[") != exp_cmp.count("]"):
				return "false"
			if exp_cmp.count("(") != exp_cmp.count(")") or exp_cmp.count("(") < 1:
				return "false"

	#Checks for order of parentheses
	exp_cmp = ""
	i  = 0
	for rep in range(0, expression.count(")")):
		exp_cmp = ""
		while True:	#Attaches exp_tmp from one beginning parenthesis to the next
			exp_cmp = exp_cmp + exp_tmp[i]
			if exp_tmp[i] == ")":
				i += 1
				break
			i += 1
		if exp_cmp.count("(") != 1:	
			return "false"
			
	for i in range(0, len(exp_tmp)):
		if exp_tmp[i] == ")":
			if i < len(exp_tmp) - 1:
				if exp_tmp[i + 1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
					return "false"
	return expression

"""
	Checks for appropriate symbol placement 
"""
def	symb_check(expression): 
	#First and last values cannot be an operator
	if expression[0] in ["+", "-", "*", "/", "%", "^", "!"]:
		return "false"
	if expression[len(expression) - 1] in ["+", "-", "*", "/", "%", "^"]:
		return "false"
	
	#All "decimals" can only contain one decimal symbol
	for i in range(0, len(expression)):
		val = expression[i]
		if val.count(".") > 1:
			return "false"
			
	#Sorts all possibilities for indexes surrounding operators
	for i in range(0, len(expression)):

		#Factorial operator must immediately be followed by another operator
		if expression[i] == "!":
			#Value following factorial must be an operator
			if i < len(expression) - 1:
				if expression[i + 1] not in ["+", "-", "*", "/", "%", "^", ")"]:
					return "false"
			#Value preceding factorial must be bigger t
			if float(expression[i - 1]) % 1 != 0:
				return "false"
		
		#Exponents must have values in front and behind it
		if expression[i] == "^":
			if expression[i + 1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "("]:
				return "false"
				
		#Period/decimal symbol must have values in front and behind it
		if expression[i] == ".":
			if expression[i + 1] or expression[i - 1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
				return "false"
		
		#Parentheses pairs must contain values in them, and there must be an operator between parentheses
		if expression[i] == ")": 
			if expression[i - 1] in ["+", "-", "*", "/", "%", "^", "("]:
				return "false"
			if i < len(expression) - 1 and expression[i + 1] in ["{", "[", "("]:
				return "false"
				
	return expression
	
"""
	Check for division by 0 
"""	
def checkzero(expression):
	for i in range(0, len(expression)):
		if expression[i] == "/" or expression[i] == "%":
			if expression[i + 1] == "0" or expression[i + 1] == 0:
				return "false"
				
	return expression

"""
	Calculates expression, using order of operations
"""
def calc_exp(expression):
	#Evaluates Exponents & Factorials
	i = 0
	while i < len(expression):
		if expression[i] == "!" or expression[i] == "^":
			if expression[i] == "!":
				expression[i] = math.factorial(float(expression[i - 1]))	#Calculates factorial 
				
			if expression[i] == "^":
				expression[i] = float(expression[i - 1]) ** float(expression[i + 1]) #Calculates exponent		
				expression.pop(i + 1) #Removes value after operator
			
			expression.pop(i - 1) #Removes value before operator	
		else:
			i += 1
	
	i = 0
	while i < len(expression):
		if expression[i] == "*" or expression[i] == "/" or expression[i] == "%":
			if expression[i] == "*":
				expression[i] = float(expression[i - 1]) * float(expression[i + 1]) #Calculates multiplication
				
			if expression[i] == "/":
				expression[i] = float(expression[i - 1]) / float(expression[i + 1]) #Calculates division

			if expression[i] == "%":
				expression[i] = float(expression[i - 1]) % float(expression[i + 1])	#Calculates floor division
				
			expression.pop(i + 1) #Removes value after operator
			expression.pop(i - 1) #Removes value before operator
		else:
			i += 1
	
	i = 0
	while i < len(expression):
		if expression[i] == "+" or expression[i] == "-":
			if expression[i] == "+":
				expression[i] = float(expression[i - 1]) + float(expression[i + 1]) #Adds
				
			if expression[i] == "-":
				expression[i] = float(expression[i - 1]) - float(expression[i + 1])	#Subtracts
			
			expression.pop(i + 1) #Removes value after operator
			expression.pop(i - 1) #Removes value before operator
		else:
			i += 1
			
	return expression
	
"""
	Groups all parentheses and solves
"""			
def get_paren(expression):
	i = 0
	for rep in range(0, expression.count("(")):
		exp_tmp = ""
		#Gets index of beginning parenthesis
		while expression[i] != "(":
			i += 1 
		expression.pop(i) #Removes expression at index i
		while expression[i] != ")":
			exp_tmp = exp_tmp + expression[i] + " "
			expression.pop(i)
		#Removes all values inside parentheses besides the ending parentheses
		val = calc_exp(exp_tmp.split()) #Assigns val as the list containing 1 value
		expression[i] = val[0] #Assigns index of ending parentheses to index 0 of val
		
	return expression		

"""
	Groups all square brackets and solves
"""	
def get_squ_brack(expression):
	exp_tmp = ""
	i = 0
	#Gets index of beginning parenthesis
	while expression[i] != "[":
		i += 1 
	expression.pop(i) #Removes expression at index i (beginning bracket)
	while expression[i] != "]":
		exp_tmp = exp_tmp + expression[i] + " "
		expression.pop(i)
	#Removes all values inside bracket besides the ending square bracket
	val = calc_exp(exp_tmp.split()) #Assigns val as the list containing 1 value
	expression[i] = val[0] #Assigns index to value in list val
		
	return expression
	
"""
	Groups all sharp brackets and solves
"""	
def get_shar_brack(expression):
	exp_tmp = ""
	i = 0
	#Gets index of beginning parenthesis
	while expression[i] != "{":
		i += 1 
	expression.pop(i) #Removes expression at index i (beginning bracket)
	while expression[i] != "}":
		exp_tmp = exp_tmp + expression[i] + " "
		expression.pop(i)
	#Removes all values inside bracket besides the ending sharp bracket
	val = calc_exp(exp_tmp.split()) #Assigns val as the list containing 1 value
	expression[i] = val[0] #Assigns index to value in list val
	
	return expression

"""
	Reverts all values back to string
"""
def getstring(expression):
	for i in range(0, len(expression)):
		expression[i] = str(expression[i]) #Turns all values to string
		
	return expression

"""
	Get all brackets and solves
"""
def getallbrackets(expression):
	if expression.count("(") > 0:
		expression = getstring(expression)
		expression = get_paren(expression) 
		if expression.count("[") > 0:
			expression = getstring(expression)
			expression = get_squ_brack(expression)
			if expression.count("{") > 0:
				expression = getstring(expression)
				expression = get_shar_brack(expression)
		
	return expression
	
retry = ""
while retry not in ["n", "no"]:
	exp = get_expression() #Gets user-input expression
	exp = exp_split(exp) #Splits expression
	
	#Gather original expression and formats
	exp_ori = ""
	for i in range(0, len(exp)):
		exp_ori += exp[i] + " "
				
	if exp.count("(") > 0:
		exp = bracket_order(exp) #Makes sure all brackets are in order
		exp = getallbrackets(exp)
		exp = getstring(exp)
	exp = symb_check(exp) #Checks for proper operator placement

	if exp == "false":
		print("This expression is invalid")
	else:  
		exp = checkzero(exp) #Checks for division by 0
		if exp == "false":
			print("This expression is invalid: Division by 0")
		else:
			exp = calc_exp(exp)
			sol = exp[0] #Removes brackets
			print(exp_ori, "=", sol) #Prints result
	
		retry = input("\nWould you like to enter another expression? Enter n or no to exit: ")
		retry.lower()
		print()
if retry in ["n", "no"]:
	print("Goodbye!")