import numpy as np


def customSVD(matrixes):
    v = []
    for matrix in matrixes:
        print(matrix)
        transposed = np.transpose(matrix)
        auxMatrix = np.matmul(transposed, matrix)
        eigenvalues, eigenvectors = customEigenCalc(auxMatrix)
        v.append(eigenvectors)
    return eigenvectors


def customEigenCalc(matrix):
    Q, R = qr_decomposition(matrix)
    eigvectors = Q

    A = np.matmul(R, Q)
    error = 0.00000000001
    while not isConvergingTriangular(R, error):
        Q, R = qr_decomposition(A)
        A = np.matmul(R, Q)
        # print('RQ: ' + str(A))
        eigvectors = np.matmul(eigvectors, Q)
    return readEigenvalues(R), np.matrix(eigvectors)


def readEigenvalues(A):
    eigenvalues = []
    error = 0.00000000001
    for i in range(0, A.shape[0]):
        eigenvalue = A.item((i, i))
        if abs(eigenvalue) <= error:
            eigenvalue = 0
        eigenvalues.append(eigenvalue)
    return eigenvalues


# checks for lower triangles of val < admissibleError in matrix
def isConvergingTriangular(matrix, admissibleError):
    # print('es triangular: ' + str(matrix))
    for x in range(0, matrix.shape[0]):
        for y in range(0, matrix.shape[1]):
            if x != y and abs(matrix[x, y]) > admissibleError:
                return False
    return True


def qr_decomposition(matrix):
    A = np.array(matrix)
    Q = np.matrix([[]])
    for i in range(0, A.shape[0]):
        u = A[:][i]
        for j in range(0, i):
            u = np.subtract(u, np.dot(A[:][i], Q[:][j]) * Q[j])
        a = u / norm_2(u)
        if i == 0:
            Q = np.array([a])
        else:
            Q = np.vstack((Q, a))
    Q = np.transpose(Q)
    R = np.zeros((3,3))
    for i in range(0, A.shape[0]):
        for j in range(i, A.shape[0]):
            R[i, j] = np.dot(Q[:, i], A[:][j])
    return Q, R


def norm_2(vec):
    vec = np.array(vec)
    return np.sqrt(sum([i ** 2 for i in vec]))


def QRFactorization(A):
    print('Entro a factqr')
    print('A: ' + str(A))
    Q = [(A[:, 0] / np.linalg.norm(A[:, 0]))]
    print('Q: ' + str(Q))
    print('Arranco qr')
    for i in range(1, A.shape[0]):
        print('Entro con index ' + str(i) + ' de ' + str(A.shape[0]))
        print('B anterior: ' + str(Q[:][i - 1]))
        print('Vec que agarro: ' + str(A[:, i]))
        print('Res proyeccion: ' + str(projection(A[:, i], Q[:][i - 1])))
        b = A[:, i]
        print(b)
        for j in range(0, i):
            print(projection(A[:, i], Q[:][i - 1]))
            b -= projection(A[:, i], Q[:][i - 1])
        Q = np.append(Q, b / np.linalg.norm(b), 0)  # esto aca era un 1
        print('Nuevo Q: \n' + str(Q))
    print('Q transpuesta: \n' + str(np.transpose(Q)))
    R = np.matmul(np.transpose(Q), A)
    print('R: \n' + str(R))
    return Q, R


# vec1 projected on vec2
def projection(vec1, vec2):
    return (np.dot(vec1, vec2) / np.dot(vec2, vec2)) * vec2


def main():
    matrix = [1, 1, 0], [1, 0, 1], [0, 1, 1]

    print("Matrix oridinal: ")
    # print(matrix)
    # print(np.transpose(matrix))
    #   exit(0)
    #   aux = customSVD([matrix])
    print(np.array(matrix))
    print('--')
    aux = customEigenCalc(np.array(matrix))
    #   aux = isConvergingTriangular([ [1, 1, 1],
    #                                  [0, 0, 1],
    #                                  [0, 0, 1]], 0.00001 )
    print("Eigenvalues: " + str(aux[0]))
    print("Eigenvectors: \n" + str(aux[1]))
    exit(0)


if __name__ == "__main__":
    main()
