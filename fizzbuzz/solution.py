"""
_solution_

This module defines the lambda abstraction
FIZZBUZZ which is a list of church encoded numerals each
representing a unicode codepoint which if interpreted and
printed to a device would present the solution to the
classic FIZZBUZZ problem.

In addition, HEAD, TAIL, and IS_EMPTY abstractions are defined
that will allow extraction of the codepoints from FIZZBUZZ by
an appropriate printing procedure.
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
FORTY = (ADD)(THIRTY)(TEN)
FIFTY = (ADD)(FORTY)(TEN)

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

# Alternate precesssor - the "Wisdom Tooth" trick.
# I'm including this because I really like the reasoning
# even though it's unused code.
#
# Create a step function that takes a pair [a, b] --> [b, b + 1]
# Then apply it to [0,0] n-times, and pick off the first element,
# which is n-1 !!!
WT_STEP = lambda p: (PAIR) ((SECOND)(p)) ((SUCC)((SECOND)(p)))
WT_PRED = lambda n: (FIRST)((n)(WT_STEP)((PAIR)(ZERO)(ZERO)))

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
        (lambda z: (f)(
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

# Unicode characters (church numerals representing codepoints)
CH_NEWLINE = (TEN)
CH_SPACE = (ADD)(THIRTY)(TWO)
CH_ZERO = (ADD) (FORTY) ((ADD)(FIVE)(THREE))
CH_B = (ADD) ((ADD)(TEN)(FIFTY)) ((ADD)(ONE)(FIVE))
CH_F = (ADD)(CH_B)(FOUR)
CH_I = (ADD)(CH_F)(THREE)
CH_U = (ADD) (FORTY) ((ADD)(FORTY)(FIVE))
CH_Z = (ADD)(FORTY)(FIFTY)

# Convert church numberals to "string" or list of unicode codepoints
# representing each numeral. Note this doesn't work for zero:
# INT_TO_STR(132) --> ["1", "3", "2"]

# Step function accepts a pair [number, string] and
# returns [ number / 10, "number % 10" + string ]
P_INT_TO_STR_STEP = ( lambda f: lambda p:
    (IS_ZERO)
        ((FIRST)(p))
        ((SECOND)(p))
        (lambda z: (f)(
            (PAIR)
                ((DIV) ((FIRST)(p)) (TEN))
                ((CONS)
                    ((ADD) ((MOD)((FIRST)(p))(TEN)) (CH_ZERO))
                    ((SECOND)(p))
                )
        )(z))
)
P_INT_TO_STR = (Z)(P_INT_TO_STR_STEP)
INT_TO_STR = lambda n: (P_INT_TO_STR)((PAIR)(n)(EMPTY))

# Reverse a list
#
# Stepper function will accept a pair of lists [ forward, reverse ]
# and return a new pair [ (TAIL)(forward), (CONS) ((HEAD)(forward)) (reverse) ]
# or just reverse if forward is empty
P_REVERSE_STEP = (lambda f: lambda p:
    ((IS_EMPTY)
        ((FIRST)(p))
        ((SECOND)(p))
        (lambda z: (f)(
            ((PAIR)
                ((TAIL) ((FIRST)(p)))
                ((CONS)
                    ((HEAD) ((FIRST)(p)))
                    ((SECOND)(p))
                )
            )
        )(z))
    )
)
P_REVERSE = (Z)(P_REVERSE_STEP)
REVERSE = lambda l: (P_REVERSE)((PAIR)(l)(EMPTY))

# APPEND - Concatenate two lists
#
# Start with a P_REV_APPEND which appends the reverse of the first list
# to the second. The stepper function takes a pair [ list1, list2 ] and
# returns [ (TAIL)(list1), (CONS) ((HEAD)(list1)) (list2) ] if list1
# is nonempty, or list2 otherwise.
P_REV_APPEND_STEP = lambda f: lambda p: (
    ((IS_EMPTY)
        ((FIRST)(p))
        ((SECOND)(p))
        (lambda z: (f)(
            ((PAIR)
                ((TAIL)((FIRST)(p)))
                ((CONS)
                    ((HEAD)((FIRST)(p)))
                    ((SECOND)(p))
                )
            )
        )(z))
    )
)
P_REV_APPEND = (Z)(P_REV_APPEND_STEP)
APPEND = lambda a: lambda b: (P_REV_APPEND) ((PAIR) ((REVERSE)(a)) (b))

# At this point I've constructed a sufficient programming language
# using Church encodings to start working on the specifics of fizzbuzz
#
# -------------------------------------------------------------------
#
# Fizzbuzz time!

# string literals for 'fizz' and 'buzz'
FIZZ = (
    (CONS)
        (CH_F)
        ((CONS)
            (CH_I)
            ((CONS)
                (CH_Z)
                ((CONS)
                    (CH_Z)
                    (EMPTY)
                )
            )
        )
)
BUZZ = (
    (CONS)
        (CH_B)
        ((CONS)
            (CH_U)
            ((CONS)
                (CH_Z)
                ((CONS)
                    (CH_Z)
                    (EMPTY)
                )
            )
        )
)

# TRY_FIZZ(BUZZ) - takes a number and returns a list [F,I,Z,Z] ([B,U,Z,Z])
# if divisible by 3(5), or an empty list otherwise.
TRY_FIZZ = lambda n: ((IS_ZERO) ((MOD)(n)(THREE)) (FIZZ) (EMPTY))
TRY_BUZZ = lambda n: ((IS_ZERO) ((MOD)(n)(FIVE)) (BUZZ) (EMPTY))

# FIZZBUZZ_NUM - return a proper fizzbuzz string for a given number,
# i.e. FUZZBUZZ_NUM(TEN) --> [1, 0, ' ', B, U, Z, Z, '\n']
FIZZBUZZ_NUM = lambda n: (
    ((APPEND)
        ((INT_TO_STR)(n))
        ((APPEND)
            ((CONS)(CH_SPACE)(EMPTY))
            ((APPEND)
                ((TRY_FIZZ)(n))
                ((APPEND)
                    ((TRY_BUZZ)(n))
                    ((CONS)(CH_NEWLINE)(EMPTY))
                )
            )
        )
    )
)

# FIZZBUZZ_UPTO - return a fizzbuzz list for numbers 1 through n
#
# Step function takes a pair [num, list] and returns a pair
# [ PRED(num), APPEND(FIZZBUZZ_NUM(num))(list) ]  unless num is zero,
# in which case list is returned
P_FIZZBUZZ_UPTO_STEP = lambda f: lambda p: (
    ((IS_ZERO)
        ((FIRST)(p))
        ((SECOND)(p))
        (lambda z: (f)(
            ((PAIR)
                ((PRED) ((FIRST)(p)))
                ((APPEND)
                    ((FIZZBUZZ_NUM) ((FIRST)(p)))
                    ((SECOND)(p))
                )
            )
        )(z))
    )
)
P_FIZZBUZZ_UPTO = (Z)(P_FIZZBUZZ_UPTO_STEP)
FIZZBUZZ_UPTO = lambda n: (P_FIZZBUZZ_UPTO) ((PAIR)(n)(EMPTY))

# TADA!
FIZZBUZZ = (FIZZBUZZ_UPTO)(HUNDRED)
