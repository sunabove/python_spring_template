# camera_photo.py

# picamzero 라이브러리에서 Camera 모듈을 가져옴 (카메라 제어)
from picamzero import Camera
# time 모듈에서 sleep 함수 가져옴 (잠시 대기할 때 사용)
from time import sleep

# 사진 찍기
# 만약 전역 변수에 'cam'이 이미 있다면 삭제 (이전 카메라 인스턴스를 지움)
if "cam" in globals() : del cam

# 새로운 카메라 객체(cam) 생성
cam = Camera()

# 0.1초 대기 (카메라가 준비될 시간을 주기 위함)
sleep( 0.1 )

# 'test.jpg' 이름으로 사진을 찍고 파일 이름을 반환받음
file_name = cam.take_photo('test.jpg')

# 사진이 찍혔다는 메시지를 출력 (파일 이름 포함)
print( f"A Photo({file_name}) was taken." )

# 사진 출력
# matplotlib의 pyplot을 plt로, image 모듈을 mpimg로 가져옴 (이미지 표시 및 읽기)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 촬영한 이미지를 읽어와 화면에 표시
plt.imshow( mpimg.imread(file_name) ) 
plt.show()  # 이미지를 화면에 출력

# 카메라 해제
del cam
