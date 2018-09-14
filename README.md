# TPE MNA

## TP1: Facial Recognition

Python libraries required: 
- numpy
- Pillow
- sklearn
- scipy
- opencv-python
install them using $ pip install [library-name]

```
$ python .\main.py -h
usage: main.py [-h] [-l] [-a] [--name NAME] [-r ID] [-q]
               [--imagesNum IMGPERSUBJECT]
               [--trainImagesNum TRAININGIMGPERSUBJECT]
               [--testImagesNum TESTINGIMGPERSUBJECT] [--method {pca,kpca}]
               [--dbpath DBPATH] [--imagepath IMAGEPATH] [--test]

This program checks if a person in the database by using facial recognition.
You can add or remove a person from the DB and then use the webcam to recognize them.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            Shows a list of the people in the DB


  -a, --add             Add a person to DB. If no --imagepath is provided, it will try to use the camera.
      --name NAME           Name of the person to add.


  -r ID, --remove ID    Remove a person from DB by using his id. (Check id by using -l or --list)


  -q, --query           Check if a person is in the DB by using a photograph
      --imagesNum IMGPERSUBJECT
                            Number images per subject
      --trainImagesNum TRAININGIMGPERSUBJECT
                            Number of training images per subject
      --testImagesNum TESTINGIMGPERSUBJECT
                            Number of testing images per subject
      --method {pca,kpca}   Method used to perform the face recognition
      --dbpath DBPATH       Path to the database to use when querying.
      --imagepath IMAGEPATH
                            Path of file to check
      --test                Test flag to show graphics and check error
```
