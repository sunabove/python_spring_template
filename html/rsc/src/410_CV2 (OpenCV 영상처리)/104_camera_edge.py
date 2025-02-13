import cv2
import time

# 카메라 열기 (0은 기본 카메라를 의미)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 콘솔 메시지 출력
print("프로그램이 시작되었습니다. 종료하려면 'q'를 입력하세요.")

# 현재 시간 저장
start_time = time.time()
frame_count = 0

while True:
    # 카메라에서 프레임 읽기
    ret, frame = camera.read()
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    # 이미지 그레이스케일로 변환 (Canny 경계선 추출을 위해)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Canny 경계선 추출
    edges = cv2.Canny(gray_frame, 100, 200)

    # FPS 계산
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # 텍스트 추가 (FPS, 경과 시간, 종료 안내 메시지)
    fps_text = f"FPS: {fps:.2f}"
    elapsed_text = f"Elapsed Time: {elapsed_time:.2f} s"
    quit_text = "Press 'q' to quit."

    font = cv2.FONT_HERSHEY_SIMPLEX
    # 원본 프레임에 텍스트 추가
    cv2.putText(frame, fps_text, (10, 30), font, 1, (0, 255, 0), 2)
    cv2.putText(frame, elapsed_text, (10, 70), font, 1, (255, 0, 0), 2)
    cv2.putText(frame, quit_text, (10, 110), font, 1, (0, 0, 255), 2)

    # 경계선선 프레임에 텍스트 추가
    cv2.putText(edges, "Edge", (10, 30), font, 1, (255, 255, 255), 2) 

    # 원본과 엣지 프레임을 수평으로 결합
    combined_frame = cv2.hconcat([frame, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)])

    # 결합된 영상 표시
    cv2.imshow("Original and Edge Detection", combined_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("프로그램이 종료되었습니다.")
        break

# 자원 해제
camera.release()
cv2.destroyAllWindows()
