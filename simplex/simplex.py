# coding=utf-8
import sys
import numpy
import matrix


######################################################################################################
#
# Método simplex, adaptado do algoritmo R fornecido
#
# Disciplina: Pesquisa Operacional
# Alunos: Bruno Tomé - 0011254
#         Ronan Nunes - 0011919
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

    tad_matrix = matrix.Matrix()
    iteration = 0

    print 'A', matrix_a

    print 'b', vector_b

    print 'c', costs_c

    # Print the title of problem

    print '-------------------------------------------------------------', title, \
        '-------------------------------------------------------------'

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
        matrix_b = tad_matrix.create_matrix(m, m)

        # Copy the columns that form the initial base
        for j in xrange(m):
            matrix_b[j] = tad_matrix.column(matrix_a, base_index[j])

        matrix_b = tad_matrix.transpose(matrix_b)

        # Print the base B just for debug
        print 'Base: ', matrix_b

        # Calculate the inverse of B
        inversed_b = numpy.linalg.inv(matrix_b)
        # Calculate the initial Feasible basic solution by inverse of B * b

        x = tad_matrix.matrix_x_matrix(inversed_b, vector_b)

        print '\nInversed base: ', inversed_b

        print '\nFeasible basic solution interation', iteration, ':', x

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
            print tad_matrix.column(matrix_a, j)
            ##############################################################
            #
            # Requirement 05 - Calculus of -B^{-1}A_j
            #
            ##############################################################

            # Calculate the j feasible direction by the product -B^{-1}A_j, just for debug
            direction = tad_matrix.matrix_x_matrix(-inversed_b, tad_matrix.column(matrix_a, j))

            ##############################################################
            #
            # Requirement 04 - Calculate the reduced cost
            #
            ##############################################################
            # Calculate the reduced cost
            cost = tad_matrix.matrix_x_matrix(tad_matrix.transpose(base_cost), inversed_b)
            cost = costs_c[j] - numpy.dot(cost, tad_matrix.column(matrix_a, j))

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
        u = tad_matrix.matrix_x_matrix(inversed_b, tad_matrix.column(matrix_a, choosen_j))

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
        ##############################################################
        #
        # Requirement 06 - Update the value of theta
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
        ##############################################################
        #
        # Requirement 07 - Change of base
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


if __name__ == '__main__':
    ####################################
    #
    # Requirement 01 - Data Entry
    #
    ####################################

    A = [[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0],
         [2860, 3520, 36490, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

    b = [132, 66, 159, 53, 3, 1, 1000000]

    c = [8680, 4140, 82800, 0, 0, 0, 0, 0, 0, 0, 2000000, 2000000, 2000000]

    simplex(A, b, c, [6, 7, 8, 9, 10, 11, 12], [0, 1, 2, 3, 4, 5], 7, 13, 'Luiz')
