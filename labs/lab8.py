'''
Author: Adrian deCola
Date: November 29, 2020
Purpose: This program creates functions that preform multiple tasks and tests
them using the testHarness function. It makes use of organization and explains
what each function does above it. It also utilizes dictionaries for the first
time. 
'''
from testHarness import * #importing the testHarness function(for tests of
                          #fruitful functions)

#This function takes in a string, removes all the whitespace and punctuation,
#and then returns a list of all the characters in the string.
def splitAndStrip(string):
    list1 = []
    notallowed = "., ;:?!\n\t"
    for i in range(len(string)):
        if not string[i] in notallowed:
            list1.extend(string[i])
    return list1

#This function accepts a list of integers in sorted order and returns a list
#ith all adjacent duplicates removed. It assumes the list has length.
def removeDuplicates(listOfIntsSorted):
    list1 = []
    list1.append(listOfIntsSorted[0])
    for i in range(1, len(listOfIntsSorted)):
        if not listOfIntsSorted[i] == list1[-1]:
            list1.append(listOfIntsSorted[i])
    return list1

#This function takes a list of strings and returns the index of the the minimum-
#length string. If there are multiple occurences of a strings with the same
#lengths then the function returns the index of the first occurance of a string
#of that length.
def findMinString(listOfStrings):
    index = None
    length = None
    for i in range(len(listOfStrings)):
        currentString = listOfStrings[i]
        if index == None or len(currentString) < length:
            index = i
            length = len(currentString)
    return index

#This function finds the mode in a list of integer. If there are multiple
#integers with the max amount of occurances, then the functions returns the
#average of those integers, as is the mode.
def findMode(listOfInts):
    #Creating integer counter
    intCounter = {}
    for i in range(len(listOfInts)):
        integer = listOfInts[i]
        if integer in intCounter:
            intCounter[integer] += 1
        else:
            intCounter[integer] = 1
    #Finding most populus integers
    popularInts = []
    maxOccurance = None
    for i in range(len(listOfInts)):
        integer = listOfInts[i]
        if maxOccurance == None or maxOccurance == intCounter[integer]:
            popularInts.append(integer)
            maxOccurance = intCounter[integer]
        elif maxOccurance < intCounter[integer]:
            popularInts = [integer]
            maxOccurance = intCounter[integer]
    #Calculating the mode
    sum = 0
    for i in range(len(popularInts)):
        sum += popularInts[i]
    mode = sum / (i + 1)
    if mode % 1 == 0:
        mode = int(mode)
    return mode




def main():
    #Testing the splitAndStrip function
    string = "Hi,\n\t Adrian!"; expectedResult = ["H", "i", "A", "d", "r", "i", "a", "n"]
    testHarness(splitAndStrip, string, expected = expectedResult)
    string = "\nMiDdLe\t !"; expectedResult = ["M", "i", "D", "d", "L", "e"]
    testHarness(splitAndStrip, string, expected = expectedResult)
    string = "TEST,\n., \t!t e s t"; expectedResult = ["T", "E", "S", "T", "t", "e", "s", "t"]
    testHarness(splitAndStrip, string, expected = expectedResult)
    string = "H  ,.  e   l   l  o\n\t ,.!"; expectedResult = ["H", "e", "l", "l", "o"]
    testHarness(splitAndStrip, string, expected = expectedResult)
    string = ",.\n\t.,"; expectedResult = []
    testHarness(splitAndStrip, string, expected = expectedResult)
    #Testing the removeDuplicates function
    listOfIntsSorted = [2, 2, 3, 5, 7, 7, 7, 7, 10, 13, 13]
    expectedResult = [2, 3, 5, 7, 10, 13]
    testHarness(removeDuplicates, listOfIntsSorted, expected = expectedResult)
    listOfIntsSorted = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    expectedResult = [5]
    testHarness(removeDuplicates, listOfIntsSorted, expected = expectedResult)
    listOfIntsSorted = [-5, -3, -2, -2, -1, 6, 6]
    expectedResult = [-5, -3, -2, -1, 6]
    testHarness(removeDuplicates, listOfIntsSorted, expected = expectedResult)
    listOfIntsSorted = [-3, 3, -2, 2, -3, 3, -2, 2]
    expectedResult = [-3, 3, -2, 2, -3, 3, -2, 2]
    testHarness(removeDuplicates, listOfIntsSorted, expected = expectedResult)
    listOfIntsSorted = [1]
    expectedResult = [1]
    testHarness(removeDuplicates, listOfIntsSorted, expected = expectedResult)
    #Testing the findMinString function
    listOfStrings = ["Hello", "Hola", "Hi", "Bonjour"]
    expectedResult = 2
    testHarness(findMinString, listOfStrings, expected = expectedResult)
    listOfStrings = ["High", "JId", "fjdiD", "K"]
    expectedResult = 3
    testHarness(findMinString, listOfStrings, expected = expectedResult)
    listOfStrings = ["What"]
    expectedResult = 0
    testHarness(findMinString, listOfStrings, expected = expectedResult)
    listOfStrings = ["Find", "Kind", "Wind"]
    expectedResult = 0
    testHarness(findMinString, listOfStrings, expected = expectedResult)
    listOfStrings = ["djfionsnkIFNGK", "djfiosnkIFNGK"]
    expectedResult = 1
    testHarness(findMinString, listOfStrings, expected = expectedResult)
    #Testing the findMinString function
    listOfInts = [8,2,8,9,3,1,8,2,7]
    expectedResult = 8
    testHarness(findMode, listOfInts, expected = expectedResult)
    listOfInts = [7]
    expectedResult = 7
    testHarness(findMode, listOfInts, expected = expectedResult)
    listOfInts = [1, 1, 2, 2, 4, 4]
    expectedResult = 7 / 3
    testHarness(findMode, listOfInts, expected = expectedResult)
    listOfInts = [5, 9, 9, 3, 5, 6, 5, 2, 5]
    expectedResult = 5
    testHarness(findMode, listOfInts, expected = expectedResult)
    listOfInts = [0, 4, 6, 4, 0]
    expectedResult = 2
    testHarness(findMode, listOfInts, expected = expectedResult)

main()
