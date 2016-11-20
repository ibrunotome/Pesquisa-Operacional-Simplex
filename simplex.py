# coding=utf-8
import numpy
import sys


######################################################################################################
#
# Método simplex, adaptado do algoritmo R fornecido
#
# Disciplina: Pesquisa Operacional
# Alunos: Bruno Tomé - 0011254
#         Ronan Nunes - 0011219
# Professor: Diego Mello Silva
#
# Repositório no GitHub: https://github.com/ibrunotome/Pesquisa-Operacional-Simplex
#
######################################################################################################


def simplex(matrix_a, vector_b, costs_c, base_index, non_base_index, m, n, title):
    """
    Resolve linear problems by using the simplex method porposed byDantzig in 1947.

    Code adapted of Diego Mello R script

    :param matrix_a: is a matrix of coefficients
    :param vector_b: is the resource vector
    :param costs_c: is the costs vector
    :param base_index: is the index of matrix_a that form the bases of the initial feasible basic solution
    :param non_base_index: is the index of non-basic variables
    :param m: are the rows of matrix_a
    :param n: are the cols of matrix_a
    :param title: is the title of the problem
    """
    iteration = 0
    x = None

    print 'A',
    print numpy.asmatrix(matrix_a)

    print 'b',
    print vector_b

    print 'c',
    print costs_c

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

        # Print basic and non-basic index of current iteration (debug)
        print '\n################\n# Iteration #', iteration, '\n################'

        print '\nBasic index:',
        for i in base_index:
            print ' ', i,

        print '\nNon-basic index:',
        for i in non_base_index:
            print ' ', i,

        # Create a blank matrix B with m x m dimensions
        matrix_b = numpy.zeros((m, m))

        print '\n'
        # Copy the columns that form the initial base
        for j in xrange(m):
            matrix_b[:, j] = column(matrix_a, base_index[j])

        # Print the base B just for debug
        print 'Base: ', matrix_b

        # Calculate the inverse of B
        inversed_b = numpy.linalg.inv(matrix_b)
        # Calculate the initial Feasible basic solution by inverse of B * b

        x = numpy.dot(inversed_b, vector_b)

        print '\nInversed base: ', inversed_b

        print '\nFeasible basic solution interation: ', iteration,
        print x

        objective = 0

        for i in xrange(m):
            objective += costs_c[base_index[i]] * x[i]

        print '\nObjective: ', objective

        ##############################################################
        #
        # Step 2: Calculating the reduced costs of non-base index
        #
        ##############################################################

        # For each non-base index, calculate the reduced cost
        base_cost = numpy.zeros(m)

        for i in xrange(m):
            base_cost[i] = costs_c[base_index[i]]
            print 'c_B[', base_index[i], '] = ', base_cost[i]

        choosen_j = -1
        choosen_cost = sys.maxsize

        for j in non_base_index:
            print column(matrix_a, j)

            # Calculate the j feasible direction by the product -B^{-1}A_j, just for debug
            direction = numpy.dot(-inversed_b, column(matrix_a, j))

            # Calculate the reduced cost
            cost = numpy.dot(base_cost.transpose(), inversed_b)
            cost = costs_c[j] - numpy.dot(cost, column(matrix_a, j))

            if cost < 0 and cost < choosen_cost:
                choosen_j = j
                choosen_cost = cost

            # Print the j feasible direction, just for debug
            print '\nFeasible direction:', j, 'Reduced cost =', cost

            for i in xrange(m):
                print 'd_B[', base_index[i], '] = ', direction[i]

        # If no index was found with reduced cost, we have a optimun
        if choosen_j == -1:
            # Show the optimun solution, just for debug
            objective_value = 0
            for i in xrange(m):
                objective_value += (base_cost[i] * x[i])

            print '\nObjective = ', objective_value, ' (Found on iteration nº ', iteration, ')'
            solution = numpy.zeros(n)

            for i in xrange(m):
                solution[base_index[i]] = x[i]

            for i in xrange(n):
                print 'x[', i, ']', solution[i]

            return x

        print '\nPut variable on base: x[', choosen_j, ']'

        ##############################################################
        #
        # Step 3: Computer vector u
        #
        ##############################################################

        # We don't have a optimun solution yet. Some basic variable must get out of
        # the base and give his place for one non-basic variable. Compute u to verify
        # if the solution is unlimited
        u = numpy.dot(inversed_b, column(matrix_a, choosen_j))

        # Check if no one of the components of u is positive
        positive_exists = False

        for i in xrange(m):
            if u[i] > 0:
                positive_exists = True

        # Test. If doesn't have no one positive value on vector u, it's because
        # the optimun value is -infinite
        if not positive_exists:
            print '\nOptimun cost = -infinite'
            return numpy.repeat(sys.maxsize, n)

        ##############################################################
        #
        # Step 4: Determinate the value of theta
        #
        ##############################################################

        # Kick a high value for theta, and it decreases according to the reason x_i / u_i
        theta = sys.maxsize
        index_l = -1

        for i in xrange(m):
            if u[i] > 0:
                # Calculate the rason
                reason = x[i] / u[i]

                # Update the reason, because we find a lower value of theta
                if reason < theta:
                    theta = reason
                    index_l = base_index[i]

        print '\nRemove variable of base: x[', index_l, '], theta = ', theta

        ##############################################################
        #
        # Step 5: Update the basic and non-basic variable
        #
        ##############################################################

        # Calculate the value of non-basic and update the base
        for i in xrange(m):
            # If we find the l indicates who of the basic variable that will leave
            # the base, replace it with the non-basic variable corresponding to
            # the j feasible direction of cost reduction
            if base_index[i] == index_l:
                x[i] = theta
                base_index[i] = choosen_j

        # For the other non-basic variables, it only updates the index of those
        # who left the base (entered the set of non-basic ones)
        for i in xrange(n - m):
            if non_base_index[i] == choosen_j:
                non_base_index[i] = index_l

        iteration += 1

    return x


def column(matrix, index):
    """
    Return the requested column of a matrix

    :param matrix:
    :param index:
    :return list:
    """
    return [row[index] for row in matrix]


##################################################
#
# Requirement 02 - Data Structure + Operations
#
##################################################
def create_matrix(rows, columns):
    """
    Create and return a matrix with m rows and n columns
    fill with zeros, it' the same to do:
    matrix = [[0,0,0], [0,0,0], [0,0,0]]

    :param rows:
    :param columns:
    :return:
    """

    matrix = []  # Empty list
    for i in xrange(rows):
        linha = []  # Empty list
        for j in xrange(columns):
            linha.append(0)

        # Put the line in the matrix
        matrix.append(linha)

    return matrix


###############################################
# Requirement 02 - c)
#
# Dot product of the matrix, considering the
# compatibility between rows and cols
###############################################
def multiply_matrix(matrix_a, matrix_b):
    # Confirm dimensions
    matrix_a_rows = len(matrix_a)
    matrix_a_cols = len(matrix_a[0])
    matrix_b_rows = len(matrix_b)
    matrix_b_cols = len(matrix_b[0])

    ####################################################
    # Test if is possible to multiply the both matrix,
    # otherwise, trows a exception
    #
    # THIS IS A PART OF THE REQUIRIMENT 02 - c)
    ####################################################
    assert (matrix_a_cols == matrix_b_rows)  # Test if is possible to multiply the both matrix

    rows = matrix_a_rows
    cols = matrix_b_cols

    # Create the result matrix c = a*b
    result = create_matrix(rows, cols)

    # Now find each value in turn in the result matrix
    for row in xrange(rows):
        for col in xrange(cols):
            dot_product = 0
            for i in xrange(matrix_a_cols):
                dot_product += matrix_a[row][i] * matrix_b[i][col]
            result[row][col] = dot_product

    return result


###############################################
# Requirement 02 - d)
#
# Calculus of the transpose of matrix
###############################################
def transpose(matrix):
    """
    Transpose the matrix passed (rows become columns and columns become rows)

    :param matrix:
    :return:
    """

    return [[row[i] for row in matrix] for i in xrange(len(matrix[0]))]


if __name__ == '__main__':
    ####################################
    #
    # Requirement 01 - Data Entry
    #
    ####################################

    # A = [[20, 30, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]]
    # b = [1200, 40, 30]
    # c = [-1000, -1800, 0, 0, 0]
    # simplex(A, b, c, [2, 3, 4], [0, 1], 3, 5, 'Pag 6')

    a = [[1, 2, 3],
         [4, 5, 6]]
    b = [[0, 3],
         [1, 4],
         [2, 5]]

    print multiply_matrix(a, b)
