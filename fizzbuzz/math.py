"""
_math_

Numerals and mathematical operations
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
