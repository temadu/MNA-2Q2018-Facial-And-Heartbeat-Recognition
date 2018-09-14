import argparse
from argparse import RawTextHelpFormatter
import picturetaker
import os
import facespca
import faceskernelpca
import time

WEBCAM_ON = False


def checkPositive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError(
             "%s is an invalid positive int value" % value)
    return ivalue

def checkBetweenOneAndTen(value):
    ivalue = int(value)
    if ivalue <= 0 or ivalue > 10:
         raise argparse.ArgumentTypeError(
             "%s is an invalid int value. Must be between 1 and 10" % value)
    return ivalue

def argumentParser():
    parser = argparse.ArgumentParser(description='This program checks if a person is an enemy of the state.\n'
                                                 'You can add or remove a person from the DB and then use magic to check if he exists in it by using the webcam.\n'
                                                 'LONG LIVE TRUMPERINO!', formatter_class=RawTextHelpFormatter)

    # LIST PERSONS IN DB
    parser.add_argument(
        '-l',
        '--list',
        help="Shows a list of the people in the DB\n\n",
        action='store_true'
    )

    # ADD PERSON
    parser.add_argument(
        '-a',
        '--add',
        help="Add a person to DB. If no --imagepath is provided, it will try to use the camera.",
        action='store_true'
    )

    parser.add_argument(
        '--name',
        help="Name of the person to add.\n\n",
        default='NO NAME'
    )

    # REMOVE PERSON
    parser.add_argument(
        '-r',
        '--remove',
        help="Remove a person from DB by using his id. (Check id by using -l or --list)\n\n",
        default=-1,
        metavar="ID",
        type=checkPositive
    )

    # CHECK EXISTANCE
    parser.add_argument(
        '-q',
        '--query',
        help="Check if a person is in the DB by using a photograph",
        action='store_true'
    )

    parser.add_argument(
        '--imagesNum',
        help="Number images per subject",
        default=10,
        dest='imgPerSubject',
        type=checkBetweenOneAndTen
    )

    parser.add_argument(
        '--trainImagesNum',
        help="Number of training images per subject",
        default=7,
        dest='trainingImgPerSubject',
        type=checkBetweenOneAndTen
    )

    parser.add_argument(
        '--testImagesNum',
        help="Number of testing images per subject",
        default=3,
        dest='testingImgPerSubject',
        type=checkBetweenOneAndTen
    )

    parser.add_argument(
        '--method',
        help='Method used to perform the face recognition',
        default="pca",
        choices=['pca', 'kpca']
    )

    parser.add_argument(
        '--dbpath',
        help="Path to the database to use when querying.",
        default='db/',
        dest='dbPath'
    )

    parser.add_argument(
        '--imagepath',
        help="Path of file to check"
    )

    parser.add_argument(
        '--test',
        help="Test flag to show graphics and check error\n\n",
        action='store_true'
    )

    return parser


def main():
  WEBCAM_ON = picturetaker.checkWebcamAvailability()
  # get parser
  parser = argumentParser()
  parsedArgs = parser.parse_args()
  print(parsedArgs)
  picturetaker.setDBDir(parsedArgs.dbPath)

  if parsedArgs.list:
    picturetaker.listDB()
  elif parsedArgs.remove != -1:
    if parsedArgs.remove > -1:
      picturetaker.removePerson(parsedArgs.remove)
  elif parsedArgs.add:
    picturetaker.addPerson(parsedArgs.name)
  elif parsedArgs.query:
    print(parsedArgs)
    imageToAnalizePath = parsedArgs.imagepath
    if imageToAnalizePath == None:
      imageToAnalizePath = picturetaker.takeTempPic()
    # LEVANTAR LA IMAGEN
    imageToAnalize = facespca.im.imread(imageToAnalizePath)/255.0
    
    # HACER PCA O KPCA
    result = -1

    start = time.time()
    if(parsedArgs.method == 'pca'):
        result = facespca.pca(imageToAnalize, parsedArgs.trainingImgPerSubject,
                              parsedArgs.testingImgPerSubject, parsedArgs.dbPath, parsedArgs.test)
    else:
        result = faceskernelpca.kpca(imageToAnalize, parsedArgs.trainingImgPerSubject,
                                     parsedArgs.testingImgPerSubject, parsedArgs.dbPath, parsedArgs.test)
    # DEVOLVER
    print("You are person {}: {}".format(result,picturetaker.getPersonName(result)))
    end = time.time()
    print("Estimated processing time:{}".format(end - start))
    

    # LIMPIAR
    picturetaker.deleteTempPic()
  else:
    parser.print_help()
  
  exit(0)


if __name__ == "__main__":
    main()
