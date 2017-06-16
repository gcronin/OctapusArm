import serial
import math
from random import randint

# desired end effector location
xo = -1.1
yo = 16.8
zo = 8.1

# initial guess, these are midrange for servos
theta0 = 22
theta1 = 63
theta2 = -10
theta0Rad = math.radians(theta0)
theta1Rad = math.radians(theta1)
theta2Rad = math.radians(theta2)

# global for linear regression
theta_delta = 1.0   #how much theta values change for each iteration
sign_theta0change = 1   # either 1 or -1... are we increasing or decreasing theta0?
sign_theta1change = 1
sign_theta2change = 1
cost = 0
previousCost = 0

# fixed geometry distances
lz = 4.9
ly = 8.7
lw = 4.3
lA = 2.0
lB = 3.65
lC = 4.56
lD = 0.34

#end effector locations
x = -lz + math.cos(theta2Rad) * (lB * math.cos(theta1Rad) + lC * math.cos(theta0Rad - theta1Rad) ) 
y = ly + lA + lB * math.sin(theta1Rad) - lC * math.sin(theta0Rad - theta1Rad) + lD
z = lw - math.sin(theta2Rad) * (lB * math.cos(theta1Rad) + lC * math.cos(theta0Rad - theta1Rad) )

def updateThetaRads():
    global theta0
    global theta1
    global theta2
    global theta0Rad
    global theta1Rad
    global theta2Rad
    theta0Rad = math.radians(theta0)
    theta1Rad = math.radians(theta1)
    theta2Rad = math.radians(theta2)


def updateEndEffectorLocation():
    global theta0Rad
    global theta1Rad
    global theta2Rad
    global x
    global y
    global z
    lz = 4.9
    ly = 8.7
    lw = 4.3
    lA = 2.0
    lB = 3.65
    lC = 4.56
    lD = 0.34
    x = -lz + math.cos(theta2Rad) * (lB * math.cos(theta1Rad) + lC * math.cos(theta0Rad - theta1Rad) ) 
    y = ly + lA + lB * math.sin(theta1Rad) - lC * math.sin(theta0Rad - theta1Rad) + lD
    z = lw - math.sin(theta2Rad) * (lB * math.cos(theta1Rad) + lC * math.cos(theta0Rad - theta1Rad) )

def CalculateCost():
    global previousCost
    global cost
    previousCost = cost
    updateThetaRads()
    updateEndEffectorLocation()
    cost = (x - xo)**2 + (y - yo)**2 + (z - zo)**2

def LinearRegression():
    global theta_delta
    global sign_theta0change
    global sign_theta1change
    global sign_theta2change
    global theta0
    global theta1
    global theta2
    global cost
    global previousCost
    WhichThetaToChange = randint(0,2)  #randomly pick one of the angles to change
    if(WhichThetaToChange == 0):     
        theta0 += sign_theta0change*theta_delta  #change theta0
    elif(WhichThetaToChange == 1):  
        theta1 += sign_theta1change*theta_delta  #change theta1
    else:    
        theta2 += sign_theta2change*theta_delta  #change theta2

    CalculateCost()
    if(cost > previousCost):  #we are farther away... optimization went in wrong direction
        if(WhichThetaToChange == 0):  
            sign_theta0change *= -1  #next time change theta0 in opposite direction
        elif(WhichThetaToChange == 1):
            sign_theta1change *= -1  #next time change theta1 in opposite direction
        else:
            sign_theta2change *= -1  #next time change theta2 in opposite direction

def checkThetas():
    global theta0, theta1, theta2
    if(theta0 < -47 or theta0 > 91):
        return 0
    if(theta1 < -8 or theta1 > 136):
        return 0
    if(theta2 < -79 or theta2 > 60):
        return 0
    return 1

for x in range(0,1000):
    LinearRegression()
    print('Theta0: {0:.0f}'.format(theta0), ' Theta1: {0:.0f}'.format(theta1), ' Theta2: {0:.0f}'.format(theta2),' xdiff: {0:.1f}'.format(x-xo), '  ydiff: {0:.1f}'.format(y-yo),  '  zdiff: {0:.1f}'.format(z-zo))
if(checkThetas()):
    print("Thetas ok")
else:
    print("Thetas out of range")
