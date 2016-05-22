"""
_solution_

"""

# numberic zero and basic addition
ZERO = lambda f: lambda x: (x)
SUCC = lambda n: lambda f: lambda x: (f)((n)(f)(x))
ADD = lambda a: lambda b: lambda f: lambda x: (a)(f)((b)(f)(x))

# convenience numerals
ONE = (SUCC)(ZERO)
TWO = (SUCC)(ONE)
THREE = (SUCC)(TWO)
FOUR = (SUCC)(THREE)
FIVE = (SUCC)(FOUR)

TEN = (ADD)(FIVE)(FIVE)
TWENTY = (ADD)(TEN)(TEN)
THIRTY = (ADD)(TWENTY)(TEN)
FOURTY = (ADD)(THIRTY)(TEN)
FIFTY = (ADD)(FOURTY)(TEN)

HUNDRED = (ADD)(FIFTY)(FIFTY)

# booleans and pairs
TRUE = lambda a: lambda b: (a)
FALSE = lambda a: lambda b: (b)

PAIR = lambda x: lambda y: lambda z: (z)(x)(y)
FIRST = lambda p: (p)(TRUE)
SECOND = lambda p: (p)(FALSE)

# is zero predicate
IS_ZERO = lambda n: (n)(lambda x: (FALSE))(TRUE)

# list encoding using two pairs to allow empty lists
# [ <empty list boolean>, [ head, tail ] ]
EMPTY = (PAIR)(TRUE)(TRUE)
IS_EMPTY = (FIRST)
CONS = lambda h: lambda t: (PAIR)(FALSE)((PAIR)(h)(t))
HEAD = lambda z: (FIRST)((SECOND)(z))
TAIL = lambda z: (SECOND)((SECOND)(z))

# Y-combinator
Y = lambda f: (lambda x: (f)((x)(x))) (lambda x: (f)((x)(x)))
