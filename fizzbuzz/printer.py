"""
_printer_

Non-lambda calculus python functions to print a Church
encoded list of Church numerals.
"""

def unchurch(church_numeral):
    """
    Take a Church numeral and return an equivalent python integer
    """
    return church_numeral(lambda x: x + 1)(0)


def unchurch_list(church_list, head=None, tail=None, isnil=None):
    """
    Given a Church list, head, tail, and isnil functions
    return a python list of the elements.
    """
    py_list = []
    while not isnil(church_list)(True)(False):
        py_list.append(head(church_list))
        church_list = tail(church_list)
    return py_list
