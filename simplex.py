# coding=utf-8
import math
import numpy


def simplex(A, b, c, baseIndex, m, n, title):
    """
    Resolve problems of linear problem by using the simplex method porposed byDantzig in 1947.

    Code adapted of Diego Mello

    :param A:
    :param b:
    :param c:
    :param baseIndex:
    :param m:
    :param n:
    :param title:
    """
    iter = 0

    print A
    print b
    print c

    # Print the title of problem

    print '-------------------------------------------------------------'
    print title
    print '-------------------------------------------------------------'

    """
    Main while of application, do the five steps prorposed of Bertsimas and Tsiksiklis to do a complete iteration
    of simplex method
    """
    while True:
        #
        # Step 1: calculatint
        #
        break
