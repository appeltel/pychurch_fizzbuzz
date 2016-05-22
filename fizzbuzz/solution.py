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

# predecessor function and subtraction
PRED = (
    lambda n: lambda f: lambda x:
    (n)                                 # apply n-times
    (lambda g: lambda h: (h)((g)(f)))   # incrementor of contained function
    (lambda u: x)                       # to special const initial container
    (lambda u: u)                       # and extract church numeral
)
MINUS = lambda m: lambda n: (n)(PRED)(m) # m - n, i.e. MINUS(10)(5) = 5

# booleans
TRUE = lambda a: lambda b: (a)
FALSE = lambda a: lambda b: (b)

# is zero and less than or equal to predicate
IS_ZERO = lambda n: (n)(lambda x: (FALSE))(TRUE)
LEQ = lambda m: lambda n: (IS_ZERO)((MINUS)(m)(n)) # m <= n

# pairs
PAIR = lambda x: lambda y: lambda z: (z)(x)(y)
FIRST = lambda p: (p)(TRUE)
SECOND = lambda p: (p)(FALSE)

# list encoding using two pairs to allow empty lists
# [ <empty list boolean>, [ head, tail ] ]
EMPTY = (PAIR)(TRUE)(TRUE)
IS_EMPTY = (FIRST)
CONS = lambda h: lambda t: (PAIR)(FALSE)((PAIR)(h)(t))
HEAD = lambda z: (FIRST)((SECOND)(z))
TAIL = lambda z: (SECOND)((SECOND)(z))

# Y-combinator
Y = lambda f: (lambda x: (f)((x)(x))) (lambda x: (f)((x)(x)))
