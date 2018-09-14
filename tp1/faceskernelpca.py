# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 16:32:14 2017

@author: pfierens
"""
from os import listdir
from os.path import join, isdir
from scipy import ndimage as im
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import utils as u
from picturetaker import getLastInDB



# image size
horsize = 92
versize = 112
areasize = horsize * versize


def kpca(imageToAnalize, trainingImagesNum, testingImagesNum, dbPath, testFlag):

    mypath = dbPath
    onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

    #number of figures
    personno = getLastInDB()
    trnperper = trainingImagesNum
    tstperper = testingImagesNum
    trnno = personno*trnperper
    tstno = personno*tstperper

    # TRAINING SET
    images = np.zeros([trnno, areasize])
    person = np.zeros([trnno, 1])
    imno = 0
    per = 0
    for dire in onlydirs:
        for k in range(1, trnperper + 1):
            a = im.imread(mypath + dire + '/{}'.format(k) + '.pgm')
            images[imno, :] = (np.reshape(a, [1, areasize]) - 127.5) / 127.5
            person[imno, 0] = per
            imno += 1
        per += 1

    # TEST SET
    imagetst = np.zeros([tstno, areasize])
    persontst = np.zeros([tstno, 1])
    imno = 0
    per = 0
    for dire in onlydirs:
        for k in range(trnperper, 10):
            a = im.imread(mypath + dire + '/{}'.format(k) + '.pgm')
            imagetst[imno, :] = (np.reshape(a, [1, areasize]) - 127.5) / 127.5
            persontst[imno, 0] = per
            imno += 1
        per += 1

    # KERNEL: polinomial de grado degree
    degree = 2
    K = (np.dot(images, images.T) / trnno + 1) ** degree
    # K = (K + K.T)/2.0

    # esta transformación es equivalente a centrar las imágenes originales...
    unoM = np.ones([trnno, trnno]) / trnno
    K = K - np.dot(unoM, K) - np.dot(K, unoM) + np.dot(unoM, np.dot(K, unoM))

    # Autovalores y autovectores
    w, alpha = u.customEigenCalc(K)
    # w, alpha = np.linalg.eigh(K)
    lambdas = w / trnno

    # Los autovalores vienen en orden ascendente. No hago nada

    for col in range(alpha.shape[1]):
        alpha[:, col] = alpha[:, col] / np.sqrt(lambdas[col])

    # pre-proyección
    improypre = np.dot(K.T, alpha)
    unoML = np.ones([tstno, trnno]) / trnno
    Ktest = (np.dot(imagetst, images.T) / trnno + 1) ** degree
    Ktest = Ktest - np.dot(unoML, K) - np.dot(Ktest, unoM) + np.dot(unoML, np.dot(K, unoM))
    imtstproypre = np.dot(Ktest, alpha)

    # from sklearn.decomposition import KernelPCA
    # kpca = KernelPCA(n_components = None, kernel='poly', degree=2, gamma = 1, coef0 = 0)
    # kpca = KernelPCA(n_components = None, kernel='poly', degree=2)
    # kpca.fit(images)

    # improypre = kpca.transform(images)
    # imtstproypre = kpca.transform(imagetst)

    nmax = alpha.shape[1]
    accs = np.zeros([nmax, 1])
    clf = None
    if(testFlag):
        for neigen in range(1, nmax+1):
            # Me quedo sólo con las primeras autocaras
            # proyecto
            improy = improypre[:, 0:neigen]
            imtstproy = imtstproypre[:, 0:neigen]

            # SVM
            # entreno
            clf = svm.LinearSVC()
            clf.fit(improy, person.ravel())
            accs[neigen-1] = clf.score(imtstproy, persontst.ravel())
            print('Precisión con {0} autocaras: {1} %\n'.format(neigen, accs[neigen-1] * 100))

        fig, axes = plt.subplots(1, 1)
        axes.plot(range(nmax), (1 - accs) * 100)
        axes.set_xlabel('No. autocaras')
        axes.set_ylabel('%error')
        axes.grid(which='Both')
        fig.suptitle('Error')
        plt.show()

    imageToVector = np.reshape(imageToAnalize, 92 * 112)
    imageArray = np.array(imageToVector)

    Ktest = (np.dot([imageArray], images.T) / trnno + 1) ** degree
    Ktest = Ktest - np.dot(unoML, K) - np.dot(Ktest, unoM) + np.dot(unoML, np.dot(K, unoM))
    imtstproypre = np.dot(Ktest, alpha)

    improy = improypre[:, 0:nmax]
    #SVM
    #entreno
    clf = svm.LinearSVC()
    clf.fit(improy, person.ravel())

    return int(clf.predict(imtstproypre)[0]) + 1
