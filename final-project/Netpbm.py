'''
Author: Adrian deCola
Date: November 23, 2020
Purpose: This program creates a class, Netpbm, which just takes in the filename
for a PGM or PPM file. The class contains many methods thatchange the instance
variables of the class, which in turn change a range of properties on the image
whether it is a PGM or PPM file. These methods include: changing the brightness,
inverting the image color, rotating the image, flipping the image, posterizing
the image, cropping the image, converting a PPM image to grayscale/PGM, applying
a glass effect to the image, halving an image, and doubling an image. These
methods and the class Netpbm can be calles by a GUI, Fauxtoshop, which easily
allows us to change these properties of an image.

Note: The file is effecient and condensed; however, in someplaces it could be
slightly more condensed but I left the modularity because I wanted to leave them
as notes to my self if I ever need as how there is different ways to go about
reading interpreting and modulizing the code for the different file types PPM
and PGM.
'''

import copy
import random

class Netpbm:
    def __init__(self, filename):
        [self.__header, self.__pixels] = self.__readImage(filename)
        #python specific^^

    #This method opens the filename, readint it and creates a two element
    #list of the header list and the pixels list.
    def __readImage(self, filename):
        inputFile = open(filename, "r")
        header = self.__readHeader(inputFile)
        if header[0].upper() == "P2":
            pixels = self.__readPGMPixels(inputFile)
        #Only PPMs
        else:
            pixels = self.__readPPMPixels(inputFile)
        inputFile.close
        imageInfo = [header, pixels]
        return imageInfo

    #This method reads and interprets the header lines of a PGM or PPM file.
    #It returns them in a list
    def __readHeader(self, inputFile):
        magicNum = inputFile.readline().strip()
        comment = inputFile.readline().strip()
        dimensions = inputFile.readline().split()
        for i in range(2):
            dimensions[i]=int(dimensions[i])
        maxColorNum = int(inputFile.readline().strip())
        header = [magicNum, comment, dimensions, maxColorNum]
        return header

    #This method builds a list of the pixel values inside a PGM file
    def __readPGMPixels(self, inputFile):
        pixels = []
        line = inputFile.readline()
        while line != '':
            values = line.split()
            pixels.extend(values)
            line = inputFile.readline()
        #Converting pixel list to integers.
        for i in range(len(pixels)):
            pixels[i] = int(pixels[i])
        return pixels

    #This method builds a list of the pixel values inside a PPM file.
    #It returns a list that contains a list of the reds, a list of the greens,
    #and a list of the blues all in order
    def __readPPMPixels(self, inputFile):
        reds = []; greens = []; blues = []
        allPixelsList = inputFile.read().split()
        #Converting to integers
        for i in range(len(allPixelsList)):
            allPixelsList[i] = int(allPixelsList[i])
        #Splitting into lists of reds, greens, and blues
        for i in range(len(allPixelsList)):
            if i%3 == 0:
                reds.append(allPixelsList[i])
            if i%3 == 1:
                greens.append(allPixelsList[i])
            if i%3 == 2:
                blues.append(allPixelsList[i])
        pixels = [reds, greens, blues]
        return pixels


    def isPGM(self):
        return True if self.__header[0].upper() == "P2" else False

    def getMagicNumber(self):    return self.__header[0]
    def getComment(self):        return self.__header[1]
    def getNumCols(self):        return self.__header[2][0]
    def getNumRows(self):        return self.__header[2][1]
    def getMaxLevel(self):       return self.__header[3]

    def getHeader(self):      return copy.deepcopy(self.__header)
    def getPixels(self):      return copy.deepcopy(self.__pixels)

    #This method writes a new file, which is the same as the one defined by
    #self, with the name of the parameter 'filename'
    def writeImage(self, filename):
        outputFile = open(filename, "w")
        self.__writeHeader(outputFile)
        if self.__header[0].upper() == "P2":
            self.__writePGMPixels(outputFile)
        #Only PPMs
        else:
            self.__writePPMPixels(outputFile)
        outputFile.close

    #This method writes the header for the file into outputFile based
    #on the header list passed through the parameter header
    def __writeHeader(self, outputFile):
        outputFile.write(str(self.__header[0]) + "\n")
        outputFile.write(str(self.__header[1]) + "\n")
        outputFile.write(str(self.__header[2][0]) + " " + \
        str(self.__header[2][1]) + "\n")
        outputFile.write(str(self.__header[3]) + "\n")

    #This method writes the pixel payload for a PGM file into outputFile
    #creating a new line after 30 pixels or the number of columns of the image
    #has been reached: whichever is shorter
    def __writePGMPixels(self, outputFile):
        #Choosing a number for when to write a new line
        if 30 < self.__header[2][0]:
            newLineArgument = 30
        else:
            newLineArgument = self.__header[2][0]
        #Writing pixel payload
        for i in range(len(self.__pixels)):
            outputFile.write(str(self.__pixels[i]) + " ")
            if (i + 1) % newLineArgument == 0:
                outputFile.write("\n")

    #This method writes the pixel payload for a PPM file into outputFile
    #creating a new line after 10 pixels or the number of columns of the image
    #has been reached: whichever is shorter
    def __writePPMPixels(self, outputFile):
        #Choosing a number for when to write a new line
        if 10 < self.__header[2][0]:
            newLineArgument = 10
        else:
            newLineArgument = self.__header[2][0]
        #Writing pixel payload
        for i in range(len(self.__pixels[0])):
            outputFile.write(f"{self.__pixels[0][i]} {self.__pixels[1][i]} " +
                             f"{self.__pixels[2][i]}   ")
            if (i + 1) % newLineArgument == 0:
                outputFile.write("\n")

    # This method changes the brightness of the image stored in the instance
    #variables. Amount is an assumed to be an integer
    def changeBrightness(self, amount):
        #PGMS
        if self.__header[0].upper() == "P2":
            for i in range(len(self.__pixels)):
                self.__pixels[i] = self.__pixels[i] + amount
                #correcting so pixels are all in gray scale max value range
                if self.__pixels[i] < 0:
                    self.__pixels[i] = 0
                if self.__pixels[i] > self.__header[3]:
                    self.__pixels[i] = self.__header[3]
        #Only PPMs
        else:
            for i in range(3):
                for j in range(len(self.__pixels[i])):
                    self.__pixels[i][j] = self.__pixels[i][j] + amount
                    if self.__pixels[i][j] < 0:
                        self.__pixels[i][j] = 0
                    if self.__pixels[i][j] > self.__header[3]:
                        self.__pixels[i][j] = self.__header[3]

    #This method inverts the colors of the imve stored in the instance
    #variables
    def invert(self):
        #PGMS
        if self.__header[0].upper() == "P2":
            for i in range(len(self.__pixels)):
                self.__pixels[i] = self.__header[3] - self.__pixels[i]
        #Only PPMs
        else:
            for i in range(3):
                for j in range(len(self.__pixels[i])):
                    self.__pixels[i][j]=self.__header[3] - self.__pixels[i][j]

    #This method rotates an image clockwise if rotateRight = True or is not
    #specified and counterclockwise if rotateRight = False, PPM or PGM
    def rotate(self, rotateRight = True):
        #Swapping rows and columns and updating
        rows = self.__header[2][0]
        columns = self.__header[2][1]
        self.__header[2][0] = columns
        self.__header[2][1] = rows
        pixels_pgm = []; pixels_ppm = [[], [], []]
        for r in range(rows):
            for c in range(columns):
                if self.__header[0].upper() == "P2":    #PGMs
                    if rotateRight == True:             #clockwise
                        index = rows*(columns - c - 1)+r
                        pixels_pgm.append(self.__pixels[index])
                    else:                               #counterclockwise
                        index = (rows*c) + (rows - r - 1)
                        pixels_pgm.append(self.__pixels[index])
                else:                                   #PPMs
                    for i in range(3):
                        if rotateRight == True:         #clockwise
                            index = rows*((columns - c) - 1)+r
                            pixels_ppm[i].append(self.__pixels[i][index])
                        else:                           #counterclockwise
                            index = (rows*c) + (rows - r - 1)
                            pixels_ppm[i].append(self.__pixels[i][index])
        if self.__header[0].upper() == "P2":            #PGMs
            self.__pixels = pixels_pgm
        else:                                           #PPMs
            self.__pixels = pixels_ppm

    #This method flips the image vertically if vertical = True or is not
    #specified and horizontally if verticle = False
    def flip(self, vertical = True):
        rows = self.__header[2][1]
        columns = self.__header[2][0]
        pixels_pgm = []; pixels_ppm = [[], [], []]
        for r in range(rows):
            for c in range(columns):
                if self.__header[0].upper() == "P2":    #PGMs
                    pixels = []
                    if vertical == True:                #flip vertically
                        index = columns*(rows-r-1) + c
                        pixels_pgm.append(self.__pixels[index])
                    else:                               #flip horizontally
                        index = columns*(r) + columns - c - 1
                        pixels_pgm.append(self.__pixels[index])
                else:                                   #PPMs
                    pixels = [[], [], []]
                    for i in range(3):
                        if vertical == True:            #flip vertically
                            index = columns*(rows-r-1) + c
                            pixels_ppm[i].append(self.__pixels[i][index])
                        else:                           #flip horizontally
                            index = columns*(r) + columns - c - 1
                            pixels_ppm[i].append(self.__pixels[i][index])
        if self.__header[0].upper() == "P2":            #PGMs
            self.__pixels = pixels_pgm
        else:                                           #PPMs
            self.__pixels = pixels_ppm

    #This method posterizes so that the number of colors shown(reds, greens,
    #and blues each for PPMs) is numLevels, and updates the header
    def posterize(self, numLevels):
        maxLevel = self.__header[3]
        binWidth = (maxLevel + 1) / numLevels
        self.__header[3] = numLevels - 1
        #PGM
        if self.__header[0].upper() == "P2":
            for i in range(len(self.__pixels)):
                self.__pixels[i] = int(self.__pixels[i] // binWidth)
        #PPM
        else:
            for i in range(3):
                for j in range(len(self.__pixels[i])):
                    self.__pixels[i][j] = int(self.__pixels[i][j] // binWidth)

    #This method crops an image, it assumes the arguments are integers
    def crop(self, upperLeftRow, upperLeftColumn, lowerRightRow, lowerRightColumn):
        numCols = lowerRightColumn - upperLeftColumn + 1
        numRows = lowerRightRow - upperLeftRow + 1
        #PGM
        if self.__header[0].upper() == "P2":
            pixels = []
            for r in range(numRows):
                for c in range(numCols):
                    index = (upperLeftRow + r) * self.__header[2][0] + \
                            upperLeftColumn + c
                    pixels.append(self.__pixels[index])
            self.__pixels = pixels
        #PPM
        else:
            pixels = [[], [], []]
            for i in range(3):
                for r in range(numRows):
                    for c in range(numCols):
                        index = (upperLeftRow + r) * self.__header[2][0] + \
                                upperLeftColumn + c
                        pixels[i].append(self.__pixels[i][index])
            self.__pixels = pixels
        self.__header[2][0] = numCols
        self.__header[2][1] = numRows

    #This method connverts a PPM to PGM, making it grayscale according to the
    #accepted formula: p = 0.2126r + 0.7152g + 0.0722b
    def toGrayscale(self):
        if self.__header[0].upper() != "P2":
            pixels = []
            for i in range(len(self.__pixels[0])):
                pixels.append(round(0.2126*self.__pixels[0][i] + 0.7152*\
                              self.__pixels[1][i] + 0.0722*self.__pixels[2][i]))
        self.__pixels = pixels
        self.__header[0] = "P2"

    #This method provides the effect of looking through a glass object at the
    #image. It randomly grabs a pixel that is between radius rows and radius
    #columns away from the current pixel and replaces it. If it chooses a row
    #or column out of the location it chooses a new one.
    def glass(self, radius):
        #Creating list with new pixel locations
        pixelLoc = []
        rows = self.__header[2][1]
        cols = self.__header[2][0]
        for i in range(rows * cols):
            r_0 = i // cols; c_0 = i % cols   #determining the current pixel
            r = -1; c = -1                    #setting outside while loop range
            while not 0<=r<rows:
                rowOffset = random.randint(-radius, radius)
                r = r_0 + rowOffset
            while not 0<=c<cols:
                colOffset = random.randint(-radius, radius)
                c = c_0 + colOffset
            Index = r*cols + c
            pixelLoc.append(Index)
        #PGM
        if self.__header[0].upper() == "P2":
            pixels = []
            for i in range(len(self.__pixels)):
                pixels.append(self.__pixels[(pixelLoc[i])])
        #PPM
        else:
            pixels = [[], [], []]
            for i in range(3):
                for j in range(len(self.__pixels[i])):
                    pixels[i].append(self.__pixels[i][pixelLoc[j]])
        self.__pixels = pixels

    #This method halves an image dimensions, grabbing the top left pixels of
    #of what used to be a square of 4 pixels. If the number of rows or columns
    #are odd, then the method ignores the last ones.
    def halve(self):
        oddColumnsIndicator = False
        rows = self.__header[2][1] // 2
        columns = self.__header[2][0] / 2
        if columns % 1 != 0:
            oddColumnsIndicator = True
        columns = int(columns)
        pgmPixels = []; ppmPixels = [[], [], []]
        self.__header[2][0] = columns; self.__header[2][1] = rows
        for r in range(rows):
            for c in range(columns):
                index = (2*r)*(2*columns) + 2*c
                if oddColumnsIndicator:
                    index = ((2*r)*(2*columns) + 2*r) + 2*c
                #PGMs
                if self.__header[0].upper() == "P2":
                    pgmPixels.append(self.__pixels[index])
                #PPMs
                else:
                    for i in range(3):
                        pixels = [[], [], []]
                        ppmPixels[i].append(self.__pixels[i][index])
        #assigning new self.__pixels
        if self.__header[0].upper() == "P2":
            self.__pixels = pgmPixels
        else:
            self.__pixels = ppmPixels

    #This method doubles dimensions of an image, in essence making each pixel
    #in the original image four pixels(if we were looking at it like a grid)
    def double(self):
        #reading useful variables and empty lists, and updating header
        rows_i = self.__header[2][1]
        columns_i = self.__header[2][0]
        rows = self.__header[2][1] = rows_i * 2
        columns = self.__header[2][0] = columns_i * 2
        rowsDoubled_pgm = []; bothDoubled_pgm = []
        rowsDoubled_ppm = [[], [], []]; bothDoubled_ppm = [[], [], []]
        if self.__header[0].upper() == "P2":                 #PGMs
            for r in range(rows_i):                          #for each row
                rowToAppend = self.__pixels[columns_i*r : columns_i*(r+1)]
                #doubling rows
                rowsDoubled_pgm.extend(rowToAppend)
                rowsDoubled_pgm.extend(rowToAppend)
            for k in range(len(rowsDoubled_pgm)):            #doubling columns
                bothDoubled_pgm.append(rowsDoubled_pgm[k])
                bothDoubled_pgm.append(rowsDoubled_pgm[k])
            self.__pixels = bothDoubled_pgm
        else:                                                #PPMs
            for i in range(3):                               #for each color
                for r in range(rows_i):                      #for each row
                    rowToAppend = self.__pixels[i][columns_i*r : columns_i*(r+1)]
                    #doubling rows
                    rowsDoubled_ppm[i].extend(rowToAppend)
                    rowsDoubled_ppm[i].extend(rowToAppend)
                for k in range(len(rowsDoubled_ppm[i])):     #doubling columns
                    bothDoubled_ppm[i].append(rowsDoubled_ppm[i][k])
                    bothDoubled_ppm[i].append(rowsDoubled_ppm[i][k])
            self.__pixels = bothDoubled_ppm

    #I will do this method later...
    def gaussianBlur(self, radius):
        print(f"The radius is {radius}.")

def main():
    '''
    image = Netpbm("images/pgms/h.pgm")
    print(f"Magic #:    {image.getMagicNumber()}")
    print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
    print(f"Header:     {image.getHeader()}")
    print(f"Pixels:     {image.getPixels()}")
    print(image.isPGM())
    image.rotate(True)
    print(f"Magic #:    {image.getMagicNumber()}")
    print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
    print(f"Header:     {image.getHeader()}")
    print(f"Pixels:     {image.getPixels()}")
    '''
main()
