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
from utils import customSVD
from picturetaker import getLastInDB



#image size
horsize     = 92
versize     = 112
areasize    = horsize*versize

def pca(imageToAnalize, trainingImagesNum, testingImagesNum, dbPath, testFlag):

    mypath = dbPath
    onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

    #number of figures
    personno = getLastInDB()
    trnperper = trainingImagesNum
    tstperper = testingImagesNum
    trnno = personno*trnperper
    tstno = personno*tstperper

    #TRAINING SET
    images = np.zeros([trnno,areasize])
    person = np.zeros([trnno,1])
    imno = 0
    per  = 0    
    for dire in onlydirs:
        for k in range(1,trnperper+1):
            a = im.imread(mypath + dire + '/{}'.format(k) + '.pgm')/255.0
            images[imno,:] = np.reshape(a,[1,areasize])
            person[imno,0] = per
            imno += 1
        per += 1

    #TEST SET
    imagetst  = np.zeros([tstno,areasize])
    persontst = np.zeros([tstno,1])
    imno = 0
    per  = 0
    for dire in onlydirs:
        for k in range(trnperper,10):
            a = im.imread(mypath + dire + '/{}'.format(k) + '.pgm')/255.0
            imagetst[imno,:]  = np.reshape(a,[1,areasize])
            persontst[imno,0] = per
            imno += 1
        per += 1



    #CARA MEDIA
    meanimage = np.mean(images,0)
    if(testFlag):
        fig, axes = plt.subplots(1,1)
        axes.imshow(np.reshape(meanimage,[versize,horsize])*255,cmap='gray')
        fig.suptitle('Imagen media')

    #resto la media
    images  = [images[k,:]-meanimage for k in range(images.shape[0])]
    imagetst= [imagetst[k,:]-meanimage for k in range(imagetst.shape[0])]


    if(testFlag):
        import time
        start = time.time()

    #PCA
    # U, S, V = np.linalg.svd(images, full_matrices=False)
    V = customSVD(images) # Hacer inhouse
    V = V*-1

    if(testFlag):
        end = time.time()
        print(end - start)

    #Primera autocara...
    eigen1 = (np.reshape(V[0,:],[versize,horsize]))*255
    if(testFlag):
        fig, axes = plt.subplots(1,1)
        axes.imshow(eigen1,cmap='gray')
        fig.suptitle('Primera autocara')

    eigen2 = (np.reshape(V[1,:],[versize,horsize]))*255
    if(testFlag):
        fig, axes = plt.subplots(1,1)
        axes.imshow(eigen2,cmap='gray')
        fig.suptitle('Segunda autocara')

    eigen3 = (np.reshape(V[2,:],[versize,horsize]))*255
    if(testFlag):
        fig, axes = plt.subplots(1,1)
        axes.imshow(eigen2,cmap='gray')
        fig.suptitle('Tercera autocara')


    nmax = V.shape[0]
    accs = np.zeros([nmax,1])

    if(testFlag):
        for neigen in range(1,nmax+1):
            print(neigen)
            #Me quedo sólo con las primeras autocaras
            B = V[0:neigen,:]
            #proyecto
            improy      = np.dot(images,np.transpose(B))
            imtstproy   = np.dot(imagetst,np.transpose(B))

            #SVM
            #entreno
            clf = svm.LinearSVC()
            clf.fit(improy,person.ravel())
            accs[neigen-1] = clf.score(imtstproy,persontst.ravel())
            print('Precisión con {0} autocaras: {1} %\n'.format(neigen,accs[neigen-1]*100))
    
    if(testFlag):
        fig, axes = plt.subplots(1,1)
        axes.semilogx(range(nmax),(1-accs)*100)
        axes.set_xlabel('No. autocaras')
        axes.grid(which='Both')
        fig.suptitle('Error')
        plt.show()

    improy = np.dot(images, np.transpose(V))
    #SVM
    #entreno
    clf = svm.LinearSVC()
    clf.fit(improy, person.ravel())
    # accs[neigen-1] = clf.score(imtstproy, persontst.ravel())

    imageToVector = np.reshape(imageToAnalize, 92 * 112)
    imageArray = np.array(imageToVector)
    diff = imageArray - meanimage
    test = np.dot([diff], np.transpose(V))
    # print(test)

    return int(clf.predict(test)[0]) + 1
