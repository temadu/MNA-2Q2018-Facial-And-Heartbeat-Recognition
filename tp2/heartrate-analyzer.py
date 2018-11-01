import argparse
from argparse import RawTextHelpFormatter
import os
import time
import heartrate

WEBCAM_ON = False


def checkPositive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError(
             "%s is an invalid positive int value" % value)
    return ivalue


def checkBetweenTenAndTwoHundred(value):
    ivalue = int(value)
    if ivalue < 10  or ivalue > 200:
         raise argparse.ArgumentTypeError(
             "%s is an invalid int value. Must be between 10 and 200" % value)
    return ivalue


def argumentParser():
    parser = argparse.ArgumentParser(description='This program checks if a person in the database by using photoplethysmography.\n'
                                                 , formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '--minFilter',
        help="Filter min",
        type=checkBetweenTenAndTwoHundred
    )


    parser.add_argument(
        '--maxFilter',
        help="Filter max",
        default=200,
        type=checkBetweenTenAndTwoHundred
    )

    parser.add_argument(
        '--videoPath',
        help="Path of video to check"
    )

    parser.add_argument(
        '--test',
        help="Test flag to show graphics and check error\n\n",
        action='store_true'
    )

    return parser


def main():
  # get parser
  parser = argumentParser()
  parsedArgs = parser.parse_args()
  start = time.time()
  isTest = False
  if parsedArgs.test:
      isTest = True

  if parsedArgs.videoPath:
    heartrate.analyze(parsedArgs.videoPath, isTest, parsedArgs.minFilter, parsedArgs.maxFilter)
    end = time.time()
    print("Estimated processing time:{}".format(end - start))

  else:
    parser.print_help()

  exit(0)


if __name__ == "__main__":
    main()
