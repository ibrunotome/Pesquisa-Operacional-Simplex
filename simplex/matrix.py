# coding=utf-8

import numpy


######################################################################################################
#
# TAD Matrix para o simplex
#
# Disciplina: Pesquisa Operacional
# Alunos: Bruno Tomé - 0011254
#         Ronan Nunes - 0011919
# Professor: Diego Mello Silva
#
# Repositório no GitHub: https://github.com/ibrunotome/Pesquisa-Operacional-Simplex
#
######################################################################################################


class Matrix(object):
    ##################################################
    #
    # Requirement 02 - Data Structure + Operations
    #
    ##################################################
    @staticmethod
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
    # Requirement 02 - a)
    #
    # Calculus of scalar product by given a matrix
    # and a scalar
    ###############################################
    @staticmethod
    def matrix_x_scalar(matrix, scalar):
        """
        Do a scalar product with a matrix

        :param matrix:
        :param scalar:
        :return:
        """
        return [Matrix.vector_x_scalar(matrix[i], scalar) for i in xrange(len(Matrix.column(matrix, 0)))]

    ###############################################
    # Requirement 02 - b)
    #
    # Calculus of scalar product by given a row
    # or col of a matrix, or given a single vector
    ###############################################
    @staticmethod
    def vector_x_scalar(vector, scalar):
        """
        Do a scalar product with a vector

        :param vector:
        :param scalar:
        :return:
        """
        return [vector[i] * scalar for i in xrange(len(vector))]

    ###############################################
    # Requirement 02 - c)
    #
    # Dot product of the matrix, considering the
    # compatibility between rows and cols
    ###############################################
    @staticmethod
    def matrix_x_matrix(matrix_a, matrix_b):
        """
        Multiply two matrix, checking first if is possible do that
        If try works, it's because two matrix are passed by parameters,
        If catch into Except, it' because a matrix and a vector are passed by parameters.
        If catch into IndexError, it's because a scalar and a vector are passed by parameters.

        :param matrix_a:
        :param matrix_b:
        :return:
        """

        try:
            result = []  # Final result
            for i in range(len(matrix_a)):

                row = []  # The new row in new matrix
                for j in range(len(matrix_b)):
                    product = 0  # The new element in the new row

                    for v in range(len(matrix_a[i])):
                        product += matrix_a[i][v] * matrix_b[v][j]

                    row.append(product)  # Append sum of product into the new row

                result.append(row)  # Append the new row into the final result

            return result
        except TypeError:
            try:
                rows = len(matrix_a)
                result = [0] * rows  # Result will be a vector with quantity cols equal to matrix quantity rows
                sum_result = 0

                for j in xrange(rows):
                    r = matrix_a[j]
                    for i in xrange(len(matrix_b)):
                        sum_result += r[i] * matrix_b[i]  # Sum of the product

                    result[j], sum_result = sum_result, 0
                return result
            except IndexError:
                return numpy.dot(matrix_a, matrix_b)

    ###############################################
    # Requirement 02 - d)
    #
    # Calculus of the transpose of matrix
    ###############################################
    @staticmethod
    def transpose(matrix):
        """
        Transpose the matrix passed (rows become columns and columns become rows)

        :param matrix:
        :return:
        """

        try:
            return [[row[i] for row in matrix] for i in xrange(len(matrix[0]))]
        except TypeError:  # It's already transposed
            return matrix

    ###############################################
    # Requirement 02 - e)
    #
    # Calculus of the inverse matrix by using LU
    # decomposition
    ###############################################
    @staticmethod
    def inverse(matrix):
        """
        Make the inverse of a matrix, by LU decomposition method

        :param matrix:
        :return:
        """

        def pivot_matrix(matrix_aux):
            """
            Returns the pivoting matrix for M, used in Doolittle's method.
            """

            m = len(matrix_aux)

            # Create an identity matrix, with floating point values
            id_mat = [[float(_i == _j) for _i in xrange(m)] for _j in xrange(m)]

            # Rearrange the identity matrix such that the largest element of
            # each column of M is placed on the diagonal of of M
            for _j in xrange(m):
                row = max(xrange(_j, m), key=lambda index: abs(matrix_aux[index][_j]))
                if _j != row:
                    # Swap the rows
                    id_mat[_j], id_mat[row] = id_mat[row], id_mat[_j]

            return id_mat

        def aux(_l, _u):
            inv = _u

            _n = len(_l)

            for _i in xrange(1, _n):
                for _j in xrange(_i):
                    inv[_i][_j] = _l[_i][_j]

            return inv

        # Performs an LU Decomposition of matrix (which must be square) into PA = LU. The function returns P, L and U.
        n = len(matrix)

        # Create zero matrices for L and U
        l = Matrix.create_matrix(n, n)
        u = Matrix.create_matrix(n, n)

        # Create the pivot matrix P and the multipled matrix PA
        p = pivot_matrix(matrix)
        pa = Matrix.matrix_x_matrix(p, matrix)

        # Perform the LU Decomposition
        for j in xrange(n):
            # All diagonal entries of L are set to unity
            l[j][j] = 1.0

            for i in xrange(j + 1):
                s1 = sum(u[k][j] * l[i][k] for k in xrange(i))
                u[i][j] = pa[i][j] - s1

            for i in xrange(j, n):
                s2 = sum(u[k][j] * l[i][k] for k in xrange(j))
                l[i][j] = (pa[i][j] - s2) / u[j][j]

        inversa = aux(l, u)

        return inversa

    ###############################################
    # Requirement 02 - f)
    #
    # Other necessary operations
    ###############################################
    @staticmethod
    def column(matrix, index):
        """
        Return the requested column of a matrix

        :param matrix:
        :param index:
        :return list:
        """

        return [row[index] for row in matrix]

    @staticmethod
    def make_identity(n):
        """
        Create an identity matrix

        :param n:
        :return:
        """

        result = Matrix.create_matrix(n, n)
        for i in xrange(n):
            result[i][i] = 1
        return result

    @staticmethod
    def quantity_cols(matrix):
        """
        Return the quantity of cols of given matrix

        :param matrix:
        :return:
        """

        return len(matrix[0])

    @staticmethod
    def quantity_rows(matrix):
        """
        Return the quantity of rows of given matrix

        :param matrix:
        :return:
        """

        return len(matrix)
