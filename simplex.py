# coding=utf-8
import math
import numpy


def simplex(A, b, c, baseIndex, nonBaseIndex, m, n, title):
    """
    Resolve problems of linear problem by using the simplex method porposed byDantzig in 1947.

    Code adapted of Diego Mello

    :param A:
    :param b:
    :param c:
    :param baseIndex:
    :param nonBaseIndex:
    :param m:
    :param n:
    :param title:
    """
    iteration = 0

    print A
    print b
    print c

    # Print the title of problem

    print '\n\n-------------------------------------------------------------'
    print title
    print '-------------------------------------------------------------'

    """
    Main while of application, do the five steps prorposed of Bertsimas and Tsiksiklis to do a complete iteration
    of simplex method
    """
    while True:
        #
        # Step 1: calculate initial SBF
        #

        # Print basic and non basic index of current iteration (debug)
        print('\nIteration # %s' % iteration)

        print '\n\tBasic index:',
        for i in baseIndex:
            print(' %s' % i),

        print '\n\tNon basic index:',
        for i in nonBaseIndex:
            print(' %s' % i),

        # Create a matrix m x m
        B = numpy.zeros((m, m)).tolist()
        break


if __name__ == '__main__':
    A = numpy.zeros((3, 5)).tolist()
    b = [4, 6, 8]
    c = [-3, -5, 0, 0, 0]
    simplex(A, b, c, [3, 2, 5], [1, 4], 3, 5, 'Teste')
