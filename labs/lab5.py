'''
Author:   Adrian deCola
Date:     2 November, 2020
Purpose:  This program creates multiple fruitful functions that preform
various duties. We create a main() function where we test all of our
functions, keeping variables out of the global space, and display the tests
in a straight forward way that shows what we are testing, the result of the
test, and the expected result of the test. We also describe each of our
function and utilize self describing code wherever possible.
'''

# This fruitful function returns the absoluteValue of the parameter num.
# It is assumed that the parameter num is an integer or floating point.
def absoluteValue(num):
    if num>0:
        return num
    else:
        return num * -1   #converts a non-positive num to non-negative

# This function returns the reciprocal of the parameter num unless num is 0
# in that case, it returns the "not a number" value.
# It is assumed that the parameter num is an integer or floating point.
def reciprocal(num):
    if num==0:
        return float("Nan")
    else:
        return (1.0 / num)

# This function returns True if the parameter int is even and false if it
# is odd. It is assumed that the parameter int is an integer.
def isEven(int):
    if int % 2 == 1:
        return False
    else:
        return True

# This function returns the largest floating-point number out of its three
# parameters by using only if statements and compound conditions.
# It is assumed that the parameters are floating-point numbers.
def maxValueOne(float1, float2, float3):
    if float1>=float2 and float1>=float3:
            return float1
    if float2>=float1 and float2>=float3:
            return float2
    if float3>=float1 and float3>=float2:
            return float3

# This function returns the largest floating-point number out of its three
# parameters by using nested if statements.
# It is assumed that the parameters are floating-point numbers.
def maxValueTwo(float1, float2, float3):
    if float1>float2:
        if float1>float3:
            return float1
        if float1<=float3:
            return float3
    if float2>=float1:
        if float2>float3:
            return float2
        if float2<=float3:
            return float3

# This function returns the largest floating-point number out of its three
# parameters by using nested if/else/elif statements.
# It is assumed that the parameters are floating-point numbers.
def maxValueThree(float1, float2, float3):
    if float1>float2:
        if float1>float3:
            return float1
        else:
            return float3
    else:
        if float2>float3:
            return float2
        else:
            return float3

def main():
    # Testing the absoluteValue function
    num = 4; expected = 4
    print("\nTesting absoluteValue(" + str(num) + "): \n    Result: " + \
    str(absoluteValue(num)) + "     Expected: " + str(expected))
    num = -92; expected = 92
    print("Testing absoluteValue(" + str(num) + "): \n    Result: " + \
    str(absoluteValue(num)) + "     Expected: " + str(expected))
    num = 1936.282; expected = 1936.282
    print("Testing absoluteValue(" + str(num) + "): \n    Result: " + \
    str(absoluteValue(num)) + "     Expected: " + str(expected))
    num = 0; expected = 0
    print("Testing absoluteValue(" + str(num) + "): \n    Result: " + \
    str(absoluteValue(num)) + "     Expected: " + str(expected))
    num = -0.192; expected = 0.192
    print("Testing absoluteValue(" + str(num) + "): \n    Result: " + \
    str(absoluteValue(num)) + "     Expected: " + str(expected))

    # Testing the reciprocal function
    num = 4; expected = .25
    print("\nTesting reciprocal(" + str(num) + "): \n    Result: " + \
    str(reciprocal(num)) + "     Expected: " + str(expected))
    num = 0; expected = float("Nan")
    print("Testing reciprocal(" + str(num) + "): \n    Result: " + \
    str(reciprocal(num)) + "     Expected: " + str(expected))
    num = -102; expected = 1.0 / (-102)
    print("Testing reciprocal(" + str(num) + "): \n    Result: " + \
    str(reciprocal(num)) + "     Expected: " + str(expected))
    num = 15.6; expected = 1.0 / 15.6
    print("Testing reciprocal(" + str(num) + "): \n    Result: " + \
    str(reciprocal(num)) + "     Expected: " + str(expected))
    num = -10; expected = -.1
    print("Testing reciprocal(" + str(num) + "): \n    Result: " + \
    str(reciprocal(num)) + "     Expected: " + str(expected))
    num = 4; expected = .25

    # Testing the isEven function
    int = 6; expected = True
    print("\nTesting isEven(" + str(int) + "): \n    Result: " + \
    str(isEven(int)) + "     Expected: " + str(expected))
    int = 13; expected = False
    print("Testing isEven(" + str(int) + "): \n    Result: " + \
    str(isEven(int)) + "     Expected: " + str(expected))
    int = 0; expected = True
    print("Testing isEven(" + str(int) + "): \n    Result: " + \
    str(isEven(int)) + "     Expected: " + str(expected))
    int = -193332; expected = True
    print("Testing isEven(" + str(int) + "): \n    Result: " + \
    str(isEven(int)) + "     Expected: " + str(expected))
    int = 102941; expected = False
    print("Testing isEven(" + str(int) + "): \n    Result: " + \
    str(isEven(int)) + "     Expected: " + str(expected))

    # Testing the maxValueOne function
    float1 = 6; float2 = 39; float3 = 10; expected = 39
    print("\nTesting maxValueOne(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueOne(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = 0; float2 = -28; float3 = 94; expected = 94
    print("Testing maxValueOne(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueOne(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = -382; float2 = -38; float3 = -261; expected = -38
    print("Testing maxValueOne(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueOne(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = -2; float2 = -2; float3 = -2; expected = -2
    print("Testing maxValueOne(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueOne(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = 3; float2 = 3; float3 = 1; expected = 3
    print("Testing maxValueOne(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueOne(float1, float2, float3)) + \
    "     Expected: " + str(expected))

    # Testing the maxValueTwo function
    float1 = 6; float2 = 39; float3 = 10; expected = 39
    print("\nTesting maxValueTwo(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueTwo(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = 0; float2 = -28; float3 = 94; expected = 94
    print("Testing maxValueTwo(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueTwo(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = -382; float2 = -38; float3 = -261; expected = -38
    print("Testing maxValueTwo(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueTwo(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = -2; float2 = -2; float3 = -2; expected = -2
    print("Testing maxValueTwo(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueTwo(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = 3; float2 = 3; float3 = 1; expected = 3
    print("Testing maxValueTwo(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueTwo(float1, float2, float3)) + \
    "     Expected: " + str(expected))

    # Testing the maxValueThree function
    float1 = 6; float2 = 39; float3 = 10; expected = 39
    print("\nTesting maxValueThree(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueThree(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = 0; float2 = -28; float3 = 94; expected = 94
    print("Testing maxValueThree(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueThree(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = -382; float2 = -38; float3 = -261; expected = -38
    print("Testing maxValueThree(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueThree(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = -2; float2 = -2; float3 = -2; expected = -2
    print("Testing maxValueThree(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueThree(float1, float2, float3)) + \
    "     Expected: " + str(expected))
    float1 = 3; float2 = 3; float3 = 1; expected = 3
    print("Testing maxValueThree(" + str(float1) + ", " + str(float2) + \
    ", " + str(float3) + "): \n    Result: " + \
    str(maxValueThree(float1, float2, float3)) + \
    "     Expected: " + str(expected))

main()
