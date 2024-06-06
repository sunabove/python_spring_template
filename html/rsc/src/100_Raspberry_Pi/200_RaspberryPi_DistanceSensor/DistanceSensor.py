from gpiozero import DistanceSensor
distanceSensor = DistanceSensor(echo=17, trigger=4)
while 1 :
    #print("\b"*40, distanceSensor.distance*100, "cm", end="")
    print( distanceSensor.distance*100, "cm" )
