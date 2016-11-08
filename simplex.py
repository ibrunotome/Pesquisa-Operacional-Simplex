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

    print 'A',
    print numpy.asmatrix(A)

    print 'b',
    print b

    print 'c',
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

        # Create a blank matrix B with m x m dimensions
        B = numpy.zeros((m, m))

        print
        print

        # Copy the columns that form the initial base
        for j in range(0, m):
            B[:, j] = column(A, baseIndex[j])

        # Print the base B just for debug
        print B

        break


def column(matrix, index):
    """
    Return the requested column of a matrix
    :param matrix:
    :param index:
    :return:
    """
    return [row[index] for row in matrix]


if __name__ == '__main__':
    # Create a matrix for the problem
    A = [[1, 0, 1, 0, 0], [0, 1, 0, 1, 0], [3, 2, 0, 0, 1]]
    b = [4, 6, 18]
    c = [-3, -5, 0, 0, 0]
    simplex(A, b, c, [2, 1, 4], [0, 3], 3, 5, 'Goldbarg (pag 104)')
