# coding=utf-8
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
        ##############################################################
        #
        # Step 1: Calculate initial Feasible basic solution
        #
        ##############################################################

        # Print basic and non basic index of current iteration (debug)
        print '\nIteration # ', iteration

        print '\nBasic index:',
        for i in baseIndex:
            print ' ', i,

        print '\nNon basic index:',
        for i in nonBaseIndex:
            print ' ', i,

        # Create a blank matrix B with m x m dimensions
        B = numpy.zeros((m, m))

        print '\n'
        # Copy the columns that form the initial base
        for j in range(0, m):
            B[:, j] = column(A, baseIndex[j])

        # Print the base B just for debug
        print 'Base: ', B

        # Calculate the initial Feasible basic solution by inverse of B * b
        inversedB = numpy.linalg.inv(B)
        x = numpy.dot(inversedB, b)

        print '\nInversed base: ', inversedB

        print '\nFeasible basic solution interation: ', iteration,
        print x

        objective = 0

        for i in range(0, m):
            objective += c[baseIndex[i]] * x[i]

        print '\nObjective: ', objective

        ##############################################################
        #
        # Step 2: Calculating the reduced costs of non base index
        #
        ##############################################################

        # For each non base index, calculate the reduced cost
        baseCost = numpy.zeros(m)

        for i in range(0, m):
            baseCost[i] = c[baseIndex[i]]
            print '\nc_B[', baseIndex[i], '] = ', baseCost[i]

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
