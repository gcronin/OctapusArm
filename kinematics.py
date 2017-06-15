import serial
import math

theta0 = 75
theta1 = -8
theta2 = -15
theta0Rad = math.radians(theta0)
theta1Rad = math.radians(theta1)
theta2Rad = math.radians(theta2)

# KINEMATICS SETUP

# fixed geometry distances
lz = 4.9
ly = 8.7
lw = 4.3
lA = 2.0
lB = 3.65
lC = 4.56
lD = 0.34

# pulse definitions (theta in degrees)
p0 = (theta0 + 125.3)/0.09843
p1 = (theta1 + 90.5)/0.1025
p2 = (138.4 - theta2)/0.09864
p0 = int(p0)
p1 = int(p1)
p2 = int(p2)

#end effector locations
x = -lz + math.cos(theta2Rad) * (lB * math.cos(theta1Rad) + lC * math.cos(theta0Rad - theta1Rad) ) 
y = ly + lA + lB * math.sin(theta1Rad) - lC * math.sin(theta0Rad - theta1Rad) + lD
z = lw - math.sin(theta2Rad) * (lB * math.cos(theta1Rad) + lC * math.cos(theta0Rad - theta1Rad) )


print("Going to Location: {x:3.1f}, {y:3.1f}, {z:3.1f}".format(**locals()))
print("Angles: {theta0:3.1f}, {theta1:3.1f}, {theta2:3.1f}".format(**locals()))
print("Pulses: {p0:4.0f}, {p1:4.0f}, {p2:4.0f}".format(**locals()))

servoCommand = "#0P" + str(p0) + " #1P" + str(p1) + " #2P" + str(p2) + "\r"
ser = serial.Serial('COM7', 9600, timeout=5)
ser.write(servoCommand.encode('utf-8'))

#ser.write(b'#2P2200\r')
#ser.write(b'#1P920\r')
#ser.write(b'#0P800\r')
#ser.write(b'#2P2200T10000\r')
#ser.write(b'#0P1500 #1P1500 #2P1500\r')
#ser.write(b'#0P1000 #1P1000 #2P1000T3000\r')
