"""
_solution_

"""

# numberic zero and basic addition
ZERO = lambda f: lambda x: (x)
SUCC = lambda n: lambda f: lambda x: (f)((n)(f)(x))
ADD = lambda a: lambda b: lambda f: lambda x: (a)(f)((b)(f)(x))
MULT = lambda a: lambda b: lambda f: (a)((b)(f))

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

# Z-combinator
Z = (
    lambda f:
        (lambda x: (f)(lambda v: ((x)(x))(v)))
        (lambda x: (f)(lambda v: ((x)(x))(v)))
)

# Modular arithmetic and division
#
# For some reason I can't get the Z combinator to work properly
# with a Curried function of multiple variables, so I will
# use pairs as arguments for the combinated function, and then
# wrap it in a Curried function

#  Mod - Start with a stepper function accepts a pair p of numerals
PMOD_STEP = (
    lambda f: lambda p:
    (LEQ)
        ((FIRST)(p))
        ((PRED)((SECOND)(p)))
        ((FIRST)(p))
        (lambda z: (f)(
            (PAIR) ((MINUS)((FIRST)(p))((SECOND)(p))) ((SECOND)(p))
        )(z))
)
PMOD = (Z)(PMOD_STEP)
MOD = lambda m: lambda n: (PMOD)((PAIR)(m)(n)) # (MOD)(m)(n) --> m % n

# Div - use a pair of pairs
# (note the dividend is the initial remainder)
# [ quotient (q), [divisor (d), remainder (r)] ]
PDIV_STEP = (
    lambda f: lambda p:
    (LEQ)
        ((SECOND)((SECOND)(p)))             # if r <= d - 1
        ((PRED)((FIRST)((SECOND)(p))))
        ((FIRST)(p))                        # then q
        (lambda z: f(
            (PAIR)                          # else recurse with a new pair
                ((SUCC)((FIRST)(p)))        # [ q+1, [d, r-d] ]
                ((PAIR)
                    ((FIRST)((SECOND)(p)))
                    ((MINUS)
                        ((SECOND)((SECOND)(p)))
                        ((FIRST)((SECOND)(p)))
                    )
                )
        )(z))
)
PDIV = (Z)(PDIV_STEP)
DIV = lambda m: lambda n: (PDIV)((PAIR)(ZERO)((PAIR)(n)(m))) # m/n
