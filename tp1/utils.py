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
    Q, R = QRFactorization(matrix)
    eigvectors = Q

    A = np.matmul(R, Q)
    error = 0.00000000001
    while not isConvergingTriangular(A, error):
        Q, R = QRFactorization(A)
        A = np.matmul(R, Q)
        print('RQ: ' + str(A))
        eigvectors = eigvectors * Q
    return readEigenvalues(A), np.matrix(eigvectors)


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
    print('es triangular: ' + str(matrix))
    for x in range(0, matrix.shape[0]):
        for y in range(0, matrix.shape[1]):
            if x != y and abs(matrix[x, y]) > admissibleError:
                return False
    return True


def QRFactorization(A):
    print('Entro a factqr')
    print('A: ' + str(A))
    Q = [(A[:, 0]/np.linalg.norm(A[:, 0]))]
    print('Q: ' + str(Q))
    print('Arranco qr')
    for i in range(1, A.shape[0]):
        print('Entro con index ' + str(i) + ' de '+ str(A.shape[0]))
        print('B anterior: ' + str(Q[:][i-1]))
        print('Vec que agarro: '+ str(A[:, i]))
        print('Res proyeccion: '+ str(projection(A[:, i], Q[:][i-1])))
        b = [A[:, i] - projection(A[:, i], Q[:][i-1])]
        Q = np.append(Q, b/np.linalg.norm(b), 0) #esto aca era un 1
        print('Nuevo Q: ' + str(Q))
    print('Q transpuesta: '+ str(np.transpose(Q)))
    R = np.matmul(np.transpose(Q), A)
    print('R: '+ str(R))
    return Q, R


# vec1 projected on vec2
def projection(vec1, vec2):
    return np.dot((np.dot(vec1, vec2) / np.dot(vec2, vec2)), vec2)


def main():
  matrix = [1,1,0],[1, 0, 1],[0,1, 1]

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
  print("Eigenvectors: " + str(aux[1]))
  exit(0)


if __name__ == "__main__":
    main()