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
    def scalar_x_matrix(matrix, scalar):
        """
        Do a scalar product with a matrix

        :param matrix:
        :param scalar:
        :return:
        """
        return [Matrix.scalar_x_vector(matrix[i], scalar) for i in xrange(len(Matrix.column(matrix, 0)))]

    ###############################################
    # Requirement 02 - b)
    #
    # Calculus of scalar product by given a row
    # or col of a matrix, or given a single vector
    ###############################################
    @staticmethod
    def scalar_x_vector(vector, scalar):
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
    def multiply_matrix(matrix_a, matrix_b):
        # Confirm dimensions
        """
        Multiply two matrix, checking first if is possible do that

        :param matrix_a:
        :param matrix_b:
        :return:
        """
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
        result = Matrix.create_matrix(rows, cols)

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
    @staticmethod
    def transpose(matrix):
        """
        Transpose the matrix passed (rows become columns and columns become rows)

        :param matrix:
        :return:
        """

        return [[row[i] for row in matrix] for i in xrange(len(matrix[0]))]

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