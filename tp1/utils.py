import numpy as np


def customSVD(matrixes):
    v = []
    for matrix in matrixes:
        transposed = np.transpose(matrix)
        auxMatrix = np.matmul(transposed, matrix)
        eigenvalues, eigenvectors = customEigenCalc(auxMatrix)
        v.append(eigenvectors)
    return eigenvectors


def customEigenCalc(matrix):
    Q, R = QRFactorization(matrix)
    eigvectors = Q
    A = np.matmul(R, Q)
    while not isConvergingTriangular(A):
        Q, R = QRFactorization(A)
        A = np.matmul(R, Q)
        eigvectors = eigvectors * Q
    return readEigenvalues(A), np.matrix(eigvectors)


def readEigenvalues(A):
    eigenvalues = []
    error = 0.00000000000000000001
    for i in range(0, A.shape[0]):
        eigenvalue = A.item((i, i))
        if abs(eigenvalue) <= error:
            eigenvalue = 0
        eigenvalues.append(eigenvalue)
    return eigenvalues


def isConvergingTriangular(matrix, admissibleError):
    if matrix[matrix.shape[1] - 1, matrix.shape[0] - 2] <= admissibleError:
        return True
    return False


def QRFactorization(A):
    Q = A[:, 0]
    for i in range(1, A.shape[0]):
        b = A[:, i] - projection(A[:, i], Q[:, i - 1])
        np.append(Q, b, axis=1)
    R = np.matmul(np.transpose(Q), A)
    return Q, R


# vec1 projected on vec2
def projection(vec1, vec2):
    return (np.dot(vec1, vec2) / np.dot(vec2, vec2)) * vec2
