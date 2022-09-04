#My own stack-based esolang
#For implementing sorting algorithms

import operator, random
from abc import ABC, abstractmethod

class Callable(ABC):
	
	@abstractmethod	
	def eval():
		pass
		
class Value(Callable):
		
	def __init__(self, val):
		self.val = val
		
	def eval(self):
		return self.val
		
	def __repr__(self):
		return str(self.val)
		
class Comp(Callable):
	
	def __init__(self, val1, val2):
		self.val1 = val1
		self.val2 = val2
		
	def eval(self):
		val1 = self.val1.eval()
		val2 = self.val2.eval()
		if val1 > val2:
			return 1
		if val1 < val2:
			return -1
		return 0
		
	def __repr__(self):
		return f"Comp({self.val1}, {self.val2})"

class SetItem(Callable):
	
	def __init__(self, arr, ind, value):
		self.arr = arr
		self.ind = ind
		self.value = value
		
	def eval(self):
		ind = self.ind.eval()
		val = self.value.eval()
		self.arr[ind] = val
		
	def __repr__(self):
		return f"Set({self.ind}, {self.value})"

class GetItem(Callable):
	
	def __init__(self, arr, ind):
		self.arr = arr
		self.ind = ind
		
	def eval(self):
		ind = self.ind.eval()
		return self.arr[ind]
		
	def __repr__(self):
		return f"Get({self.ind})"
		
class CmpCheck(Callable):
	
	def __init__(self, val1, val2, cmp, name):
		self.val1 = val1
		self.val2 = val2
		self.cmp = cmp
		self.name = name
		
	def eval(self):
		return int(self.cmp(self.val1.eval(), self.val2.eval()))
		
	def __repr__(self):
		return f"{self.name}({self.val1}, {self.val2})"
		
class BinOp(Callable):
	
	def __init__(self, val1, val2, op, name):
		self.val1 = val1
		self.val2 = val2
		self.op = op
		self.name = name
		
	def eval(self):
		return self.op(self.val1.eval(), self.val2.eval())
		
	def __repr__(self):
		return f"{self.name}({self.val1}, {self.val2})"
		
class IfStatement(Callable):
	
	def __init__(self, cond, func):
		self.cond = cond
		self.func = func
		
	def eval(self):
		if self.cond.eval():
			self.func.eval()
		
	def __repr__(self):
		return f"If({self.cond}, {self.func})"

class IfElse(Callable):
	
	def __init__(self, cond, funcT, funcF):
		self.cond = cond
		self.funcT = funcT
		self.funcF = funcF
		
	def eval(self):
		if self.cond.eval():
			self.funcT.eval()
		else:
			self.funcF.eval()
		
	def __repr__(self):
		return f"IfElse({self.cond}, {self.func})"

class CreateFunc(Callable):
	
	def __init__(self, funcs, funcname, params, body):#
		self.funcs = funcs
		self.funcname = funcname
		self.params = params
		self.body = body
		
	def eval(self):
		name = self.funcname.eval()
		if self.funcname in self.funcs:
			raise ValueError(f"function '{name}' already exists")
		self.funcs[name] = self
		
	def __repr__(self):
		return f"Func({self.funcname}, {self.params}, {self.body})"

class CallFunc(Callable):
	
	def __init__(self, funcs, func, args, callstack):
		self.funcs = funcs
		self.func = func
		self.args = args
		self.callstack = callstack
		
	def eval(self):
		name = self.func.eval()
		if name not in self.funcs:
			raise ValueError(f"function '{name}' does not exist")
		func = self.funcs[name]
		params_given = len(self.args)
		params_expected = len(func.params)
		if params_given != params_expected:
			raise ValueError(f"function '{name}' expected {params_expected} but got {params_given} arguments")
		argnames = list(map(lambda s: str(s.val), func.params))
		args = list(map(lambda s: s.val, self.args))
		vars = dict(zip(argnames, args))
		self.callstack.append((func, vars))
		func.body.eval()
		self.callstack.pop()
		
	def __repr__(self):
		return f"Call('{self.func}', {self.args})"

class WhileLoop(Callable):
	
	def __init__(self, cond, func):
		self.cond = cond
		self.func = func
		
	def eval(self):
		while self.cond.eval():
			self.func.eval()
		
	def __repr__(self):
		return f"While({self.cond}, {self.func})"

class AndThen(Callable):
	
	def __init__(self, f1, f2):
		self.f1 = f1
		self.f2 = f2
		
	def eval(self):
		self.f1.eval()
		self.f2.eval()
		
	def __repr__(self):
		return f"AndThen({self.f1}, {self.f2})"

class Swap(Callable):
	
	def __init__(self, arr, ind1, ind2):
		self.arr = arr
		self.ind1 = ind1
		self.ind2 = ind2
		
	def eval(self):
		a = self.ind1.eval()
		b = self.ind2.eval()
		arr = self.arr
		arr[a], arr[b] = arr[b], arr[a]
		
	def __repr__(self):
		return f"Swap({self.ind1}, {self.ind2})"
		
class Random(Callable):
	
	def __init__(self, a, b):
		self.a = a
		self.b = b
		
	def eval(self):
		a = self.a.eval()
		b = self.b.eval()
		return random.randint(a, b)
		
	def __repr__(self):
		return f"Random({self.a}, {self.b})"
		
class DeclareVar(Callable):
	
	def __init__(self, vars, name):
		self.vars = vars
		self.name = name
		
	def eval(self):
		name = self.name.eval()
		if name in self.vars:
			raise ValueError(f"variable '{name}' already exists")
		self.vars[name] = 0
		
	def __repr__(self):
		return f"DeclareVar('{self.name}')"
		
class SetVar(Callable):
	
	def __init__(self, vars, name, value):
		self.vars = vars
		self.name = name
		self.value = value
		
	def eval(self):
		name = self.name.eval()
		if name not in self.vars:
			raise ValueError(f"variable '{name}' does not exist")
		self.vars[name] = self.value.eval()
		
	def __repr__(self):
		return f"SetVar('{self.name}', {self.value})"

class GetVar(Callable):
	
	def __init__(self, vars, name, callstack):
		self.vars = vars
		self.name = name
		self.callstack = callstack
		
	def eval(self):
		vars_check = [self.vars]
		if len(self.callstack) > 0:
			vars_check.append(self.callstack[-1][1])
		for vars in reversed(vars_check):
			name = self.name.eval()
			if name in vars:
				return vars[name]
		raise ValueError(f"variable '{name}' does not exist") 
		
	def __repr__(self):
		return f"GetVar('{self.name}')"
		
class IncrVar(Callable):
	
	def __init__(self, vars, name):
		self.vars = vars
		self.name = name
		
	def eval(self):
		name = self.name.eval()
		if name not in self.vars:
			raise ValueError(f"variable '{name}' does not exist")
		self.vars[name] += 1
		
	def __repr__(self):
		return f"IncrVar('{self.name}')"
		
class DecrVar(Callable):
	
	def __init__(self, vars, name):
		self.vars = vars
		self.name = name
		
	def eval(self):
		name = self.name.eval()
		if name not in self.vars:
			raise ValueError(f"variable '{name}' does not exist")
		self.vars[name] -= 1
		
	def __repr__(self):
		return f"DecrVar('{self.name}')"
		
def run(code, arr, debug=False):
	tokens = code.split()
	stack = []
	callstack = []
	vars = {}
	funcs = {}
	i = 0
	while i < len(tokens):
		token = tokens[i]
		if token.isnumeric():
			stack.append(Value(int(token)))
		elif token.startswith("\"") and token.endswith("\""):
			stack.append(Value(token[1:-1]))
		elif token == "len":
			stack.append(Value(len(arr)))
		elif token == "swap":
			p2, p1 = stack.pop(), stack.pop()
			stack.append(Swap(arr, p1, p2))
		elif token == "set":
			val, ind = stack.pop(), stack.pop()
			stack.append(SetItem(arr, ind, val))
		elif token == "get":
			ind = stack.pop()
			stack.append(GetItem(arr, ind))
		elif token == "comp":
			v2, v1 = stack.pop(), stack.pop()
			stack.append(Comp(v1, v2))
		elif token == "rand":
			b, a = stack.pop(), stack.pop()
			stack.append(Random(a, b))
		elif token == "if":
			func, cond = stack.pop(), stack.pop()
			stack.append(IfStatement(cond, func))
		elif token == "ifelse":
			funcF, funcT, cond = stack.pop(), stack.pop()
			stack.append(IfElse(cond, funcT, funcF))
		elif token == "while":
			func, cond = stack.pop(), stack.pop()
			stack.append(WhileLoop(cond, func))
		elif token == "andthen": #Andthen: performs one action before another
			f2, f1 = stack.pop(), stack.pop()
			stack.append(AndThen(f1, f2))
		elif token == "func": 
			body = stack.pop()
			args = []
			while isinstance(stack[-1], Value) and isinstance(stack[-1].val, str):
				args.append(stack.pop())
			name = args.pop()
			args.reverse()
			stack.append(CreateFunc(funcs, name, args, body))
		elif token == "call":
			args = []
			while isinstance(stack[-1], Value) and isinstance(stack[-1].val, int):
				args.append(stack.pop())
			args.reverse()
			print("Args", args)
			name = stack.pop()
			stack.append(CallFunc(funcs, name, args, callstack))
		elif token == "+":
			b, a = stack.pop(), stack.pop()
			stack.append(BinOp(a, b, operator.add, "Add"))
		elif token == "-":
			b, a = stack.pop(), stack.pop()
			stack.append(BinOp(a, b, operator.sub, "Sub"))
		elif token == "*":
			b, a = stack.pop(), stack.pop()
			stack.append(BinOp(a, b, operator.mul, "Mul"))
		elif token == "/":
			b, a = stack.pop(), stack.pop()
			stack.append(BinOp(a, b, operator.floordiv, "Div"))
		elif token == "==":
			b, a = stack.pop(), stack.pop()
			stack.append(CmpCheck(a, b, operator.eq, "Eq"))
		elif token == "<":
			b, a = stack.pop(), stack.pop()
			stack.append(CmpCheck(a, b, operator.lt, "Lt"))
		elif token == ">":
			b, a = stack.pop(), stack.pop()
			stack.append(CmpCheck(a, b, operator.gt, "Gt"))
		elif token == "!=":
			b, a = stack.pop(), stack.pop()
			stack.append(CmpCheck(a, b, operator.ne, "Ne"))
		elif token == "<=":
			b, a = stack.pop(), stack.pop()
			stack.append(CmpCheck(a, b, operator.le, "Le"))
		elif token == ">=":
			b, a = stack.pop(), stack.pop()
			stack.append(CmpCheck(a, b, operator.ge, "Ge"))
		elif token == "declare":
			name = stack.pop()
			stack.append(DeclareVar(vars, name))
		elif token == "setvar":
			value, name = stack.pop(), stack.pop()
			stack.append(SetVar(vars, name, value))
		elif token == "getvar":
			name = stack.pop()
			stack.append(GetVar(vars, name, callstack))
		elif token == "incrvar":
			name = stack.pop()
			stack.append(IncrVar(vars, name))
		elif token == "decrvar":
			name = stack.pop()
			stack.append(DecrVar(vars, name))
		i += 1
	
	if debug:
		for s in stack:
			print(s)
	
	for item in stack:
		item.eval()
		
import random
a = list(range(15))
random.shuffle(a)
print(a)


#Bubble sort

bubble_sort = """
"i" declare
"i" len 1 - setvar
"j" declare

"i" getvar 0 >=

"j" 0 setvar 
"j" getvar "i" getvar <
"j" getvar get "j" getvar 1 + get comp 1 == "j" getvar "j" getvar 1 + swap if
"j" incrvar
andthen
while

"i" decrvar
andthen
andthen

while
"""

run(bubble_sort, a, debug=True)
print(a)
