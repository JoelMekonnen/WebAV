from genericpath import isfile
import os
from PIL import Image
import numpy as np
import math
import cv2
import hexdump
from django.core.files.storage import default_storage

class ClassifierTools:
    def __init__(self, filelocation, fileName):
        self.fileLocation = filelocation # the directory to save the file
        self.fileName = fileName
    def convertListToImage(self, fileInput, imageName):
        int_num = list()
        lines = fileInput.readlines()
        file_lines = [line[9:] for line in lines]
        file_val = [myLine.strip().split(' ') for myLine in file_lines]
        for fileLines in file_val:
            line_list = []
            for num in fileLines:
                if len(num) < 2:
                    continue
                else:
                    if num[0] == '?' or num[1] == '?':
                        continue
                    else:
                       num = num.lstrip('\x00').rstrip('\x00')
                       if num ==  '':
                          continue
                       else:
                         int_num.append(int(num, 16))
        IMAGE_COUNT = len(int_num)
        IMAGE_WIDTH = int(math.sqrt(IMAGE_COUNT))
        IMAGE_HEIGHT = int(IMAGE_COUNT / IMAGE_WIDTH)
        NEW_NUM = int_num[0:IMAGE_HEIGHT * IMAGE_WIDTH]
        image_array = np.array(NEW_NUM)
        np.reshape(image_array, (IMAGE_WIDTH, IMAGE_HEIGHT), order='C')
        myImage = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT))
        myImage.putdata(image_array.flatten())
        name = ('.').join(imageName.split('.')[:-1])
        myImage.save(self.fileLocation + name + ".png", format="png")
        img = cv2.imread(self.fileLocation + name + ".png")
        resizedImage = cv2.resize(img, (64, 64), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.fileLocation + name + ".png", resizedImage)
        fileInput.close()
        return self.fileLocation + name + ".png"

   
    def image_generator(self):
        imgFile = ('.').join(self.fileName.split('.')[:-1])
        imageInput = self.fileLocation + imgFile + ".byte"
        if os.path.isdir(imageInput):
            file_list = os.listdir(imageInput)
            for files in file_list:
                myFile = open(imageInput + "\\" + files, 'r')
                return self.convertListToImage(myFile, files)
        elif os.path.isfile(imageInput):
            myFile = open(imageInput, 'r')
            return self.convertListToImage(myFile, self.fileName)
        else:
            print("wrong input entered please try again")
    
    def hex_generator(self):
        PE_input = self.fileLocation + self.fileName
        print(PE_input)
        if os.path.isdir(PE_input):
            file_list = os.listdir(PE_input)
            os.mkdir(PE_input + "_bytes")
            dir_name = PE_input + "_bytes"
            for files in file_list:
                myFile = open(PE_input + "\\" + files, 'rb')
                fileName = ('.').join(files.split('.')[:-1])
                hexd = open( dir_name + "\\" + fileName + ".byte", 'w')
                print(files)
                for line in myFile:
                    line_val = hexdump.hexdump(line, result='generator')
                    for lines in line_val:
                        nLine = lines[0:58].strip()
                        if len(nLine) < 58:
                            continue
                        hexd.writelines(nLine + "\n")
            self.image_generator()
        elif os.path.isfile(PE_input):
            myFile = open(PE_input, 'rb')
            fileName = ('.').join(self.fileName.split('.')[:-1])
            hexd = open(self.fileLocation + fileName + ".byte", 'w')
            for line in myFile:
                line_val = hexdump.hexdump(line, result='generator')
                for lines in line_val:
                    nLine = lines[0:58].strip()
                    if len(nLine) < 58:
                        continue
                    hexd.writelines(nLine + "\n")
            # myFile = open(PE_input, 'r')
            return 
        else:
            print("wrong input entered please try again")

if __name__ == "__main__":
    fileName = input("please insert filename:")
    myClass = ClassifierTools()
    myClass.image_generator(fileName)

