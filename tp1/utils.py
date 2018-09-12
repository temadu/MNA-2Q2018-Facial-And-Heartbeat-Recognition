import numpy as np


def customSVD(matrix):

    matrix = np.matrix(matrix)
    print(matrix.shape)
    transposed = np.transpose(matrix)
    auxMatrix = np.matmul(matrix, transposed)
    # auxMatrix = np.matmul(transposed, matrix)
    # print(auxMatrix.shape)
    eigenvalues, eigenvectors = customEigenCalc(auxMatrix)
    # print(eigenvalues)
    # print(eigenvectors)
    v = eigenvectors
    u = np.empty(matrix.shape)
    for i in range(0, u.shape[1]):
        u[:, i] = np.reshape(np.matmul(np.transpose(matrix), v[:, i]) / np.sqrt(eigenvalues[i]), 3) # cambiar a lo q corresponda
    v = np.matmul(np.transpose(matrix), u)
    # print(v)
    # print(u)
    return v


def customEigenCalc(matrix):
    Q, R = qr_decomposition(matrix)
    eigvectors = Q

    A = np.matmul(R, Q)
    error = 0.00001
    while not isConvergingTriangular(R, error):
        Q, R = qr_decomposition(A)
        A = np.matmul(R, Q)
        eigvectors = np.matmul(eigvectors, Q)
    return readEigenvalues(R), np.matrix(eigvectors)


def readEigenvalues(A):
    eigenvalues = []
    error = 0.00001
    for i in range(0, A.shape[0]):
        eigenvalue = A.item((i, i))
        if abs(eigenvalue) <= error:
            eigenvalue = 0
        eigenvalues.append(eigenvalue)
    return eigenvalues


# checks for lower triangles of val < admissibleError in matrix
def isConvergingTriangular(matrix, admissibleError):
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
    R = np.zeros(A.shape)
    for i in range(0, A.shape[0]):
        for j in range(i, A.shape[1]):
            R[i, j] = np.dot(Q[:, i], A[:][j])
    return Q, R


def norm_2(vec):
    vec = np.array(vec)
    return np.sqrt(sum([i ** 2 for i in vec]))


def main():
    matrix = [1, 1], [1, 0], [0, 1]

    print("Matrix oridinal: ")
    # print(matrix)
    # print(np.transpose(matrix))
    #   exit(0)
    #   aux = customSVD([matrix])
    print(np.array(matrix))
    print('--')
    aux = customSVD(np.array(matrix))

    #   aux = isConvergingTriangular([ [1, 1, 1],
    #                                  [0, 0, 1],
    #                                  [0, 0, 1]], 0.00001 )
    print("Eigenvalues: " + str(aux[0]))
    print("Eigenvectors: \n" + str(aux[1]))

    caca = np.linalg.svd(matrix)
    print(caca)
    exit(0)


if __name__ == "__main__":
    main()
