'''
Author: Adrian deCola
Date: 3 November, 2020
Purpose: This program makes many fruitful functions that each do their own
unique thing, which are explained above the functions. It also utilized a
main() function and a testFunction() function that builds tests that display
f strings of what we are testing, the result and the expected result in a neat
and understandable way. It tests each function for many possible combinations
of parameters. 
'''

# This function returns the time(or off), as a string that the alarmclock
# should be set to depending on the day of the week and whether or not you are
# on vacation.
# This function assumes the day is an interger between 0 and 6 inclusive
# and that onVacation is a boolean.
def alarm_clock(day, onvacation):
  if onvacation==False:
    if day!=0 and day!=6:
      return '7:00'
    else:
      return '10:00'
  else:
    if day!=0 and day!=6:
      return '10:00'
    else:
      return 'off'

# This functions returns the integer values either 0, 1, or 2 corresponding to
# what the speeding ticket is.
def caught_speeding(speed, isBirthday):
    if isBirthday==False:
        if speed<=60:
            return 0
        elif speed<=80:
            return 1
        else:
            return 2
    else:
        speed += -5 #Gives 5 [speed] of leeway
        if speed<=60:
            return 0
        elif speed<=80:
            return 1
        else:
            return 2

# This function takes adds the parameters a, b, and c until one of the
# arguments is 13. If one of the arguments is 13, then it does not add that
# argument or any of the arguments to the right of it.
# It is assumed that the parameters a, b, and c are integers
def lucky_sum(a, b, c):
    if a!=13:
        if b!=13:
            if c!=13:
                return a + b + c
            else:
                return a + b
        else:
            return a
    else:
        return 0

# This funcition returns True, if the parameters b or c differ to a by at most
# 1 and the other differs to a and the other(close one) by 2 or more,
# and False otherwise.
# It is assumed that a, b, and c are integers.
def close_far(a, b, c):
    if (abs(a-b)<=1 or abs(a-c)<=1) and \
    (abs(a-b)>=2 or abs(a-c)>=2) \
    and abs(b-c)>=2:
        return True
    else:
        return False

# This function rounds the parameter to the in the tens place. A number with
# a 5 in the ones place is rounded up. It is assumed that num is and integer.
def round10(num):
    if num%10>=5:
        num = (num // 10 + 1) * 10
    else:
        num = num // 10 * 10
    return num

# This functiontakes the rounded integers of a, b, and c to the tens place
# (5 in the ones place is rounded up) and then returns the sum of those
# integers. It is assumed that the parameters a, b, and c are integers.
def round_sum(a, b, c):
    sum = round10(a) + round10(b) + round10(c)
    return sum

# This function takes the parameter: the function we are testing, the expected
# result of the test, and then arguments nescessary for the function we are
# testing. It then prints the test showing what we are testing, the expected
# result, and the actual result of what we are testing.
def testFunction(function, expected, *args):
    fname = str(function).split()[1] # getting the function name as a string
    # getting the arguments as a correct looking string if there is only one
    # entry in the tuple(so that it doesn't display like: ([arg1],)
    # otherwise a tuple displays okay when passed into an f string
    vals = args if len(args)!=1 else "(" + str(args[0]) + ")"
    print(f"Testing {fname}{vals}:\n           " + \
          f"Result: {function(*args)}       " + \
          f"Expected: {expected}")

def main():
    # Testing the alarm_clock function
    print()
    day=1; onVacation = False; expected= "7:00"
    testFunction(alarm_clock, expected, day, onVacation)
    day=0; onVacation=False; expected= "10:00"
    testFunction(alarm_clock, expected, day, onVacation)
    day=3; onVacation=True; expected= "10:00"
    testFunction(alarm_clock, expected, day, onVacation)
    day=6; onVacation=True; expected= "off"
    testFunction(alarm_clock, expected, day, onVacation)
    day=6; onVacation=False; expected= "10:00"
    testFunction(alarm_clock, expected, day, onVacation)
    # Testing the caught_speeding function
    print()
    speed=53; isBirthday=False; expected=0
    testFunction(caught_speeding, expected, speed, isBirthday)
    speed=60; isBirthday=False; expected=0
    testFunction(caught_speeding, expected, speed, isBirthday)
    speed=69; isBirthday=False; expected=1
    testFunction(caught_speeding, expected, speed, isBirthday)
    speed=65; isBirthday=True; expected=0
    testFunction(caught_speeding, expected, speed, isBirthday)
    speed=70; isBirthday=True; expected=1
    testFunction(caught_speeding, expected, speed, isBirthday)
    speed=90; isBirthday=False; expected=2
    testFunction(caught_speeding, expected, speed, isBirthday)
    speed=87; isBirthday=True; expected=2
    testFunction(caught_speeding, expected, speed, isBirthday)
    # Testing the lucky_sum function
    print()
    a=1; b=2 ;c=3; expected=6
    testFunction(lucky_sum, expected, a, b, c)
    a=1; b=2 ;c=13; expected=3
    testFunction(lucky_sum, expected, a, b, c)
    a=1; b=13 ;c=-7; expected=1
    testFunction(lucky_sum, expected, a, b, c)
    a=13; b=202 ;c=-3; expected=0
    testFunction(lucky_sum, expected, a, b, c)
    a=13; b=13 ;c=3; expected=0
    testFunction(lucky_sum, expected, a, b, c)
    a=-11; b=2 ;c=13; expected=-9
    testFunction(lucky_sum, expected, a, b, c)
    a=0; b=-2 ;c=-13; expected=-15
    testFunction(lucky_sum, expected, a, b, c)
    # Testing the close_far function
    print()
    a=1; b=2; c=10; expected=True
    testFunction(close_far, expected, a, b, c)
    a=1; b=2; c=3; expected=False
    testFunction(close_far, expected, a, b, c)
    a=-1; b=10; c=0; expected=True
    testFunction(close_far, expected, a, b, c)
    a=8; b=6; c=9; expected=True
    testFunction(close_far, expected, a, b, c)
    a=4; b=3; c=5; expected=False
    testFunction(close_far, expected, a, b, c)
    # Testing the round_sum function
    print()
    a=16; b=17; c=20; expected=60
    testFunction(round_sum, expected, a, b, c)
    a=12; b=9; c=-20; expected=0
    testFunction(round_sum, expected, a, b, c)
    a=0; b=7; c=0; expected=10
    testFunction(round_sum, expected, a, b, c)
    a=25; b=25; c=34; expected=90
    testFunction(round_sum, expected, a, b, c)
    a=-16; b=-17; c=-29; expected=-70
    testFunction(round_sum, expected, a, b, c)

main()
