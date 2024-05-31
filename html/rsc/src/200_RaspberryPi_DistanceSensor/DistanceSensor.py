from gpiozero import DistanceSensor
distanceSensor = DistanceSensor(echo=17, trigger=4)
while 1 :
    print( distanceSensor.distance*100, "cm" )