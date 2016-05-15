# Fizzbuzz in the untyped lambda calculus

Copyright Eric Appelt, 2016, All Rights Reserved

Eventual link to travis tests

## The challenge

The traditional fizzbuzz programming challenge is to write a
program to print the numbers 1 through 100 on separate lines,
print 'fizz' after all numbers divisible by 3, 'buzz' after all
numbers divisilbe by both, and 'fizzbuzz' after all numbers
divisible by both, i.e:

```
1
2
3 fizz
4
5 buzz
6 fizz
7
8
9 fizz
10 buzz
11
12 fizz
13
14
15 fizzbuzz
16
...
```

Since writing to any output is not part of the untyped lambda calculus,
the challenge instead becomes:

> Produce a lambda abstraction that is a list of Church encoded numerals
> [ for example the Church numeral '3' would be λf.λx.f(f(f(x))) ]
> that represent unicode codepoints, which if encoded and written to
> an output device would be a correct solution output of the traditional
> fizzbuzz interview test. Additionally produce abstractions for
> that produce the head and tail of the list above when applied to the list.

## The rules

Lambda terms are to be written and interpreted using a highly restricted
subset of python syntax. The following syntax allowed:

1. A name `x` representing any variable that is a valid lambda term, provided
that the name is not any python built-in function or keyword.
1. If `t` is a lambda term, and `x` is a variable, then the expression
`lambda x: (t)` is allowed syntax for a lambda abstraction.
  * The enclosing parenthesis are optional, `lambda x: t` is also permitted.
1. If `t` and `s` are lambda terms, then `((t)(s))` is valid syntax for
an application.
  * The enclosing parenthesis are optional, `(t)(s)` and `t(s)` are also valid.

In addition, the following extensions are allowed for notational
convenience and clarity:

1. For any allowed name `var` and lambda abstraction `lambda x: (t)`, the
simple assignment statement `var = lambda x: (t)` is permitted, and `var`
may subsequently be used in place of `lambda x:(t)`.
1. Valid lambda terms may be written to a python module containing nothing
but valid lambda terms, simple assignment statements as given above,
empty lines, comment lines beginning with `#`, and an optional
blockquoted module docstring.
1. Import statements of the form `from m import x` or
`from m import (x, y,..., z)` are permitted provided that `m` is a module
conforming to the above rules and `x`, `y`, `z`, etc... are references
to lambda abstractions as defined above.

## Why Am I Doing This?

Not having a computer science degree, I am performing this exercise
to improve my understanding of the untyped lambda calculus and to
gain experience using functional techniques built upon first principles.

More importantly, I think this is fun.
