"""
_solution_

"""

# numberic zero and basic addition
zero = lambda f: lambda x: (x)
succ = lambda n: lambda f: lambda x: (f)((n)(f)(x))
add = lambda a: lambda b: lambda f: lambda x: (a)(f)((b)(f)(x))

# convenience numerals
one = (succ)(zero)
two = (succ)(one)
three = (succ)(two)
four = (succ)(three)
five = (succ)(four)

ten = add(five)(five)
twenty = add(ten)(ten)
thirty = add(twenty)(ten)
fourty = add(thirty)(ten)
fifty = add(fourty)(ten)

hundred = add(fifty)(fifty)

# booleans and pairs
true = lambda a: lambda b: (a)
false = lambda a: lambda b: (b)

pair = lambda x: lambda y: lambda z: (z)(x)(y)
first = lambda p: (p)(true)
second = lambda p: (p)(false)

# Y-combinator
Y = lambda f: (lambda x: (f)((x)(x))) (lambda x: (f)((x)(x)))

# list encoding using two pairs to allow empty lists
# [ <empty list boolean>, [ head, tail ] ]
empty = (pair)(true)(true)
is_empty = (first)
cons = lambda h: lambda t: (pair)(false)((pair)(h)(t))
head = lambda z: (first)((second)(z))
tail = lambda z: (second)((second)(z))
