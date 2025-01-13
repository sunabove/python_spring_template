import cv2
import time

# 웹캠 열기 (0은 기본 카메라를 의미)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("프로그램이 시작되었습니다. 종료하려면 'q'를 입력하세요.")  # 콘솔 메시지

# 현재 시간 저장
start_time = time.time()
frame_count = 0

while True:
    # 카메라에서 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    # FPS 계산
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # 텍스트 추가 (FPS, 경과 시간, 종료 안내 메시지)
    fps_text = f"FPS: {fps:.2f}"
    elapsed_text = f"Elapsed Time: {elapsed_time -20:.2f} s"
    quit_text = "Press 'q' to quit."

    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, elapsed_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, quit_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 영상 표시
    cv2.imshow("Camera", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("프로그램이 종료되었습니다.")
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
