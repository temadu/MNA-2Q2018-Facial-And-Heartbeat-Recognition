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
    error = 0.00000000000000000001
    while not isConvergingTriangular(A, error):
        Q, R = QRFactorization(A)
        A = np.cross(R, Q)
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


# checks for lower triangles of val < admissibleError in matrix
def isConvergingTriangular(matrix, admissibleError):
    for x in range(0, len(matrix)):
        for y in range(0, x):
            if matrix[x][y] > admissibleError:
                return False
    return True


def QRFactorization(A):
    Q = A[:][0]
    for i in range(1, A.shape[0]):
        b = A[:][i] - projection(A[:][i], Q[:][i - 1])
        np.append(Q, b, 0) #esto aca era un 1
    R = np.matmul(np.transpose(Q), A)
    return Q, R


# vec1 projected on vec2
def projection(vec1, vec2):
    return np.dot((np.dot(vec1, vec2) / np.dot(vec2, vec2)), vec2)


def main():
  # matrix = [1,2],[3,4]

  print("Matrix original: ")
  # print(matrix)
  # print(np.transpose(matrix))
#   exit(0)
#   aux = customSVD([matrix])
  aux = isConvergingTriangular([ [1, 1, 1],
                                 [0, 0, 1],
                                 [0, 0, 1]], 0.00001 )
  print("Answer: ")
  print(aux)
  exit(0)


if __name__ == "__main__":
    main()