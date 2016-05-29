"""
_cli_

Command line interface to lambda calculus fizzbuzz.
"""
import sys
import argparse

import fizzbuzz.solution as lc
from fizzbuzz.printer import church_print


def church(number):
    church_number = lc.ZERO
    for _ in range(number):
        church_number = lc.SUCC(church_number)
    return church_number


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('number', nargs='?', default='100')
    args = parser.parse_args()

    try:
        number = int(args.number)
    except ValueError:
        print('Error: {0} is not an integer'.format(args.number))
        sys.exit(1)

    if number == 100:
        church_print(
            lc.FIZZBUZZ,
            head=lc.HEAD,
            tail=lc.TAIL,
            isnil=lc.IS_EMPTY
        )
    elif number > 0:
        church_print(
            lc.FIZZBUZZ_UPTO(church(number)),
            head=lc.HEAD,
            tail=lc.TAIL,
            isnil=lc.IS_EMPTY
        )
    else:
        print('Error: {0} is not a positive integer'.format(number))
        sys.exit(1)


if __name__ == '__main__':
    main()
