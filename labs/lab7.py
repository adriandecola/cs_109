'''
Author: Adrian deCola
Date: November 6, 2020
Purpose: This program makes multiple functions and tests them in different ways,
mostly using the testHarness function. We especially make use of finding our
expected result by using a random seed and manually doing what we want in
terminal.
'''

from testHarness import * #importing the testHarness function(for tests of
                          #fruitful functions)
import random

# This function repeatietly asks the user for an integer until the user types
#q and quits. It then returns a list that contains the number of integers
#entered, the average of all the integers, the minimum integer, and the
#maximum integer all in that order.
def numberStats():
    i=0 #initialization
    sum=0
    ans=""
    avg=None
    max=None
    min=None
    while ans!='q': #condition
        ans = input("Give me an integer(or q to quit): ")
        if ans!= 'q':
            i += 1 #advance
            ans = int(ans)
            if max==None or max<=ans:
                max = ans
            if min==None or min>=ans:
                min = ans
            sum += ans
            avg = sum / i
    list = [i, avg, min, max]
    return list

# This function builds a string of randomly selected lowercase letters until
#both the minLength and minVowels is reached then returns the string
def easyVowel(minLength, minVowels):
    string=""
    i=0 #i corresponds to the number of vowels
    j=0 #j corresponds to the length of the string
    vowels = ['a', 'e', 'i', 'o', 'u']
    while i < minVowels or j < minLength:
        randChar = chr(ord('a') + random.randint(0, 25))
        string += randChar
        j += 1
        if randChar in vowels:
            i += 1
    return string

# This function builds a DNA sequene of the set minimum length and set minimum
#"C"s, while also not adding any Gs when the set maximum "G"s is reached
def randomDNA(minLength, minCs, maxGs):
    sequence=""
    i=0 #corresponds to length
    j=0 #corresponds to #Cs
    k=0 #corresponds to #Gs
    nucleotides = ['A', 'C', 'G', 'T']
    while i < minLength or j < minCs:
        nucl = random.choice(nucleotides)
        if nucl=='G':
            k += 1
        if nucl == 'C':
            j += 1
        if not(nucl=='G' and k>maxGs):
            sequence += nucl
            i += 1
    return sequence

# This function
def listMinMax(aList):
    min=None
    minIndex=None
    max=None
    maxIndex=None
    for i in range(len(aList)):
        element = aList[i]
        if min == None or min > element:
            min=element
            minIndex=i
        if max == None or max < element:
            max=element
            maxIndex=i
    return [min, minIndex, max, maxIndex]

# This function builds a string from characters in the list possibleChars of a
#random length between 1 and maxStringLength
def buildString(maxStringLength, possibleChars):
    string=""
    stringLength = random.randint(1, maxStringLength)
    for i in range(stringLength):
        string += random.choice(possibleChars)
    return string

# This function builds a list of strings where the strings each have a random
#length between 1 and maxStringLength and the characters of the string are
#chosen randomly from the list possibleChars. This continues until the number
#of characters in the list is at least minCharCount long.
def buildList(maxStringLength, possibleChars, minCharCount):
    zList=[]
    i=0 #corresponds to character count
    while i < minCharCount:
        element = buildString(maxStringLength, possibleChars)
        zList.extend([element])
        i += len(element)
    return zList

def main():
    '''
    #Testing the numberStats function
    print(numberStats()) #Entered: q; Result: [0, None, None, None]
    print(numberStats()) #Entered: 5, 2, 3, 9, q; Result: [4, 4.75, 2, 9]
    print(numberStats()) #Entered: 0, 0, 0, -200, 100, q;
                         #Result: [6, -16.5, -200, 100]
    print(numberStats()) #Entered: -2, -1, 0, 1, 2; Result: [5, 0.0, -2, 2]
    '''
    #Testing the easyVowel function
    random.seed(747259); minLength=10; minVowels=3;
    expectedResult = "ofixzymrwphga"
    testHarness(easyVowel, minLength, minVowels, expected=expectedResult)
    random.seed(747258); minLength=15; minVowels=1;
    expectedResult = "uhaatwpwhzproac"
    testHarness(easyVowel, minLength, minVowels, expected=expectedResult)
    random.seed(747257); minLength=0; minVowels=3;
    expectedResult = "bshtifxii"
    testHarness(easyVowel, minLength, minVowels, expected=expectedResult)
    random.seed(747256); minLength=1; minVowels=5;
    expectedResult = "amymfhlirwideblhnqxvi"
    testHarness(easyVowel, minLength, minVowels, expected=expectedResult)
    random.seed(747255); minLength=5; minVowels=0;
    expectedResult = "cejmt"
    testHarness(easyVowel, minLength, minVowels, expected=expectedResult)
    random.seed(747254); minLength=0; minVowels=0;
    expectedResult = ""
    testHarness(easyVowel, minLength, minVowels, expected=expectedResult)
    #Testing the randomDNA function
    random.seed(123456); minLength=10 ; minCs=5 ; maxGs=1
    expectedResult = "GACAAAAACTCACTAC"
    testHarness(randomDNA, minLength, minCs, maxGs, expected=expectedResult)
    random.seed(123457); minLength=20 ; minCs=0 ; maxGs=0
    expectedResult = "TTAACCCTCCACATATTTCC"
    testHarness(randomDNA, minLength, minCs, maxGs, expected=expectedResult)
    random.seed(123458); minLength=0 ; minCs=0 ; maxGs=0
    expectedResult = ""
    testHarness(randomDNA, minLength, minCs, maxGs, expected=expectedResult)
    random.seed(123459); minLength=10 ; minCs=5 ; maxGs=0
    expectedResult = "TATCCCAAATCC"
    testHarness(randomDNA, minLength, minCs, maxGs, expected=expectedResult)
    random.seed(123460); minLength=0 ; minCs=10 ; maxGs=20
    expectedResult = "AATGTCAGGAAAGTTACTGTGCGCGAAGGCGCCGCTTAGTCTAC"
    testHarness(randomDNA, minLength, minCs, maxGs, expected=expectedResult)
    random.seed(123461); minLength=0 ; minCs=0 ; maxGs=10
    expectedResult = ""
    testHarness(randomDNA, minLength, minCs, maxGs, expected=expectedResult)
    #Testing the listMinMax function
    aList=[1, 6, 3, 7]; expectedResult=[1, 0, 7, 3]
    testHarness(listMinMax, aList, expected=expectedResult)
    aList=[]; expectedResult=[None, None, None, None]
    testHarness(listMinMax, aList, expected=expectedResult)
    aList=[-293, -3, -8, -38, -3947]; expectedResult=[-3947, 4, -3, 1]
    testHarness(listMinMax, aList, expected=expectedResult)
    aList=[6, -39, 0, 53, -6]; expectedResult=[-39, 1, 53, 3]
    testHarness(listMinMax, aList, expected=expectedResult)
    aList=[5, 5, 5, 5, 5, 5]; expectedResult=[5, 0, 5, 0]
    testHarness(listMinMax, aList, expected=expectedResult)
    #Testing the buildList function
    random.seed(123456); maxStringLength=4; minCharCount=17
    possibleChars=['a', 'b', 'c', 'd'];
    expectedResult = ["aba", "a", "aab", "babd", "aba", "ddba"]
    testHarness(buildList, maxStringLength, possibleChars, minCharCount, \
    expected=expectedResult)
    random.seed(123457); maxStringLength=5; minCharCount=20
    possibleChars=['z', 'b', 't', 's', 'V'];
    expectedResult = ["stV", "Vzzb", "btb", "sbtbz", "bzs", "Vzsst"]
    testHarness(buildList, maxStringLength, possibleChars, minCharCount, \
    expected=expectedResult)
    random.seed(123458); maxStringLength=6; minCharCount=10
    possibleChars=['a'];
    expectedResult = ["aa", "aaa", "a", "aaaa"]
    testHarness(buildList, maxStringLength, possibleChars, minCharCount, \
    expected=expectedResult)
    random.seed(123459); maxStringLength=7; minCharCount=15
    possibleChars=['Y', 'N'];
    expectedResult = ["NYNYN", "YY", "NYNYNNN", "YY"]
    testHarness(buildList, maxStringLength, possibleChars, minCharCount, \
    expected=expectedResult)
    random.seed(123460); maxStringLength=1; minCharCount=6
    possibleChars=['u', 'e', 'q', 'p'];
    expectedResult = ["u", "q", "e", "q", "u", "u"]
    testHarness(buildList, maxStringLength, possibleChars, minCharCount, \
    expected=expectedResult)

main()
