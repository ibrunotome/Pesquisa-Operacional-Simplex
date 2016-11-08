# coding=utf-8
import numpy
import sys


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

        # Calculate the inverse of B
        inversedB = numpy.linalg.inv(B)
        # Calculate the initial Feasible basic solution by inverse of B * b

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

        choosenJ = -1
        choosenCost = -sys.maxsize

        for j in nonBaseIndex:
            print column(A, j)

            # Calculate the j feasible direction by the product -B^{-1}A_j, just for debug
            direction = numpy.dot(-inversedB, column(A, j))

            # Calculate the reduced cost
            cost = numpy.dot(baseCost.transpose(), inversedB)
            cost = c[j] - numpy.dot(cost, column(A, j))

            if cost < 0 and cost < choosenCost:
                choosenJ = j
                choosenCost = cost

            # Print the j feasible direction, just for debug
            print '\nFeasible direction:', j, 'Reduced cost =', cost

            for i in range(0, m):
                print 'd_B[', baseIndex[i], '] = ', direction[i]

            # If no index was found with reduced cost, we have a optimun
            if choosenJ == -1:
                # Show the optimun solution, just for debug
                objectiveValue = 0
                for i in range(0, m):
                    objectiveValue += (baseCost[i] * x[i])

                print '\nObjective = ', objectiveValue, ' (found on iteration nº ', iteration, ')'
                solution = numpy.zeros(n)

                for i in range(0, m):
                    solution[baseIndex[i]] = x[i]

                for i in range(0, n):
                    print 'x[', i, ']', solution[i]

            print 'Put variable on base: x[', choosenJ, ']'
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
