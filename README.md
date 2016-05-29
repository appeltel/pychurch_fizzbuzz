# Fizzbuzz in the untyped lambda calculus

Copyright Eric Appelt, 2016, All Rights Reserved

[![Travs-CI status](https://travis-ci.org/appeltel/pychurch_fizzbuzz.png)](https://travis-ci.org/appeltel/pychurch_fizzbuzz)

## Introduction

I have no interesting (or made-up) story to go along with this
mini-project. I've just always enjoyed having fun finding silly
ways to do fizzbuzz with one hand tied behind my back, like not
allowing if statements, looping constructs, etc...

Not having a CS degree, I always found lambda calculus to be a
mysterious but interesting subject. I recently leared about
Church Encodings, and was also inspired by various blog posting
implementing Church Numerals and other constructs in python.

I thought that actually trying to program something simple in
the untyped lambda calculus from scratch would be a good way to
really understand the mathematical system, and doing fizzbuzz in
absurd ways is always fun.

As there is no concept of IO in the untyped lambda calculus,
the meaning of fizzbuzz has to be slightly altered, and this
is given in the challenge below.

I chose python as this is just what I currently work in all
day so it is convenient, but also because the syntax for lambdas
is very similar to how lambda expressions are generally
written anyway. Plus the recursion limit of 1000 makes the
challenge more interesting.

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
> ( for example the Church numeral '3' would be λf.λx.f(f(f(x))) )
> that represent unicode codepoints, which if encoded and written to
> an output device would be a correct solution output of the traditional
> fizzbuzz interview test. Additionally produce abstractions 
> that produce the head and tail of the list above when applied to the list,
> as well as a predicate abstraction to determine if the list is empty.

The lambda calculus solution would thus take the form:

```
[ 49 ("1"), 10 ("\n"), 50 ("2"), 10 ("\n"), 51 ("3"), 32 (" "), 102 ("f"), ...]
```

This list along with the head and tail abstractions can then be passed to
a python function that will interpret each Church encoded numeral and write
the resulting characters to the screen.

## The rules

Lambda terms are to be written and interpreted using a highly restricted
subset of python syntax. The following syntax allowed:

1. A name `x` representing any variable that is a valid lambda term, provided
that the name is not any python built-in function or keyword.
  * Optional enclosing parenthesis are allowed, i.e. `(x)`, which will
    allow expressions to continue across multiple lines.
1. If `t` is a lambda term, and `x` is a variable, then the expression
`lambda x: (t)` is allowed syntax for a lambda abstraction.
  * The enclosing parenthesis are optional, `lambda x: t` is also permitted.
1. If `t` and `s` are lambda terms, then `((t)(s))` is valid syntax for
an application.
  * The enclosing parenthesis are optional, `(t)(s)` and `t(s)` are also valid.

In addition, the following extensions are allowed for notational
convenience and clarity:

1. For any allowed name `VAR` and lambda expression `x`, the
simple assignment statement `VAR = x` is permitted, and `VAR`
may subsequently be used in place of `x`. Once `VAR` is declared
it may not be reassigned.
1. Valid lambda terms may be written to a python module containing nothing
but valid lambda terms, simple assignment statements as given above,
empty lines, comment lines beginning with `#`, and an optional
blockquoted module docstring.

## My Solution

The [solution](fizzbuzz/solution.py) is just under 300 lines with comments,
and builds up a small language using only lambda expressions with
just enough functionality to produce a fizzbuzz "string".

In order to actually print this Church List of Church Numerals representing
the Unicode codepoints of fizzbuzz output, a
[printer utility](fizzbuzz/printer.py) is provided, which has a
`church_print(...)` function that takes as arguments a Church List as well
as lambda abstractions to obtain the head and tail of the list and a
predicate to determine if the list is empty. This was independently tested
against various list implementations.

Finally, a python setup script and
[command line utility](fizzbuzz/cli.py) were added to allow a simple
command `fizzbuzz` to perform fizzbuzz up to 100, or
`fizzbuzz` to perform fizzbuzz to the specified integer.

Surprisingly, this does not hit the relatively low python recursion limit
of 1000 calls, although it does take nearly 5 minutes to execute fizzbuzz
up to 100 on a modern laptop processor!

So here is the solution executed on a 2.5 GHz Intel Core i7, python 3.5.1,
OSX 10.11:

```
$ time fizzbuss
1 
2 
3 FIZZ
4 
5 BUZZ
6 FIZZ
7 
8 
9 FIZZ
10 BUZZ
11 
12 FIZZ
13 
14 
15 FIZZBUZZ
16 
...
98 
99 FIZZ
100 BUZZ

real    4m20.603s
user    4m20.374s
sys 0m0.187s
```

...and that is after rethinking the FIZZBUZZ function due to poor performance!

## Retrospective

The most difficult thing initially was really gaining an intutive
understanding of Currying. Once I became comfortable with that,
building church pairs, performing addition, and even constructing
lists became reasonable to understand. Even though I did refer to
references like the Wikipedia page for Church Encoding, I strove
to ensure that I understood how each lambda absrtraction actually
worked as I added it to my solution.

The next big challenge was subtraction, or the predecessor function.
I worked through the solution in the Wikipedia Church Encoding page,
which is a clever method without any attribution. The other method
that I really like is the "Wisdom Tooth" trick which Church's student
Keene apparently figured out in a dream state while getting his
wisdom teeth removed. According to story, Church thought that the
predecessor function was impossible before hearing the story. I stuck
this in as an alternate predecessor.

The hardest part was recursion, and this was made very difficult
due to python's eager evaluation. When I started this I had played
with the Y-combinator in erlang to allow for recursive lambdas in the
interactive shell, so I thought it would be easy enough in python.
A lot of reading and frustration later I learned that with eager
evaluation, the Y-combinator will create an infinite recursion and
blow the stack. The so-called Z-combinator protects against this,
but you also have to add an extra "thunk" function
in the recursive clause of
your predicate of a step function that you apply the Z-combinator to,
so that your recursive step is tucked into the body of a lambda
that is not evaluated if the predicate is not true/false.

I also found that the Z-combinator along with this "thunk" would
not work on a Curried step function of multiple variables, so I
had to pack everything in pairs to be passed along through the
recursive function calls. This is still an open question for me
why I can't use a Curried function with the Z-combinator with
eager evaluation.

Once I had built recursive functions for modular arithmetic and
division, I had a good pattern for recursion, started to develop
a preferred indentation style, and everything went pretty much
downhill from there. Connverting Church Numerals to lists of
unicode codepoints representing the integer was the last function
that really felt difficult to implement.

I've dabbled in Scheme and Racket before, so
I did notice that my language was starting to look like an
odd LISP dialect, and there was an a-ha moment in understanding
the why LISP looks the way it does.

This project was to me a more interesting way to learn the uptyped
lambda calculus by actually programming something that performs
a (slightly) non-trival computation. It also gave me additional
respect for Church and his students for following through with
these developments in the absence of an interpreter to test out
their propositions.
