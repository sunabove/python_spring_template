# moisture_test.py
from gpiozero import MotionSensor

motionSensor = MotionSensor(14)

count = 0
def water_detected( ):
    global count
    count += 1
    
    print( f"[{count:2d}] Water Detected!")  # 물이 감지되었음을 출력
pass

def water_not_detected( ):
    global count
    count += 1

    print( f"[{count:2d}] No Water Detected!")  # 물이 감지되지 않음을 출력
pass

motionSensor.when_motion = water_detected
motionSensor.when_no_motion = water_not_detected

input( "Press Enter to quit...\n" )
print( "Good bye!")