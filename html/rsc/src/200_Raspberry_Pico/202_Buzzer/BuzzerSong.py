# picozero 패키지에서 Speaker 임포트하여 부저 제어
from picozero import Speaker
# time 모듈에서 sleep 함수를 임포트하여 시간 지연 사용
from time import sleep

# GPIO 15번 핀에 부저 연결
buzzer = Speaker(4)

# '나비야'의 음계와 리듬
melody = [
    ('G4', 0.4), ('E4', 0.4), ('E4', 0.8),  # 나비야 / 솔미미
    ('F4', 0.4), ('D4', 0.4), ('D4', 0.8),  # 나비야 / 파레레 
    ('C4', 0.4), ('D4', 0.4), ('E4', 0.4), ('F4', 0.4), # 이리 날아 / 도레미파 
    ('G4', 0.4), ('G4', 0.4), ('G4', 0.8), # 오너라 / 솔솔솔
    
    ('G4', 0.4), ('E4', 0.4), ('E4', 0.4), ('E4', 0.4),  # 노랑나비 / 솔미미미 
    ('F4', 0.4), ('D4', 0.4), ('D4', 0.8),  # 흰나비 / 파레레 
    ('C4', 0.4), ('E4', 0.4), ('G4', 0.4), ('G4', 0.4), # 춤을추며 / 도미솔솔 
    ('E4', 0.4), ('E4', 0.4), ('E4', 0.8), # 오너라 / 미미미
    
    ('D4', 0.4), ('D4', 0.4), ('D4', 0.4), ('D4', 0.4),  # 봄바람에 / 레레레레
    ('D4', 0.4), ('E4', 0.4), ('F4', 0.8),  # 꽃잎도 / 레미파
    ('E4', 0.4), ('E4', 0.4), ('E4', 0.4), ('E4', 0.4), # 방긋방긋 / 미미미미 
    ('E4', 0.4), ('F4', 0.4), ('G4', 0.8), # 웃으며 / 미파솔
    
    ('G4', 0.4), ('F4', 0.4), ('F4', 0.8),  # 참새도 / 솔미미
    ('F4', 0.4), ('D4', 0.4), ('D4', 0.8),  # 짹짹짹 / 파레레
    ('C4', 0.4), ('E4', 0.4), ('G4', 0.4), ('G4', 0.4), # 노래하며 / 도미솔솔 
    ('E4', 0.4), ('E4', 0.4), ('E4', 0.8), # 춤춘다 / 미미미
]

# 노래 재생
for (note, duration) in melody:
    buzzer.play(note.lower(), duration=duration)  # 주파수 설정
    buzzer.off()       # 음이 끝나면 부저 끔
    sleep(0.1)         # 음 사이의 간격
pass

buzzer.close()  # 부저 자원 해제 


