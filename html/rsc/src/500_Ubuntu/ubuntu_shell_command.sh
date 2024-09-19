# 시스템 정보 출력

# 리눅스 배포판 정보 확인
lsb_release -a
# 우분투 IP 주소 출력
hostname -I
# 시스템 정보 출력
uname -a
# 호스트 정보 출력
hostnamectl
# 사용자 아이디 출력
whoami
# 아이디 정보 출력
id
# 현재 날짜 및 시각 출력
date

# 터미널 사용 팁

# 터미널 화면 지우기
clear

# 파일 정보 조회

# 현재 작업 디렉토리 출력
pwd
# 현재 폴더의 파일 이름 출력
ls
# 숨긴 파일 이름 출력
ls -a
# 파일 정보 출력 (숨긴 파일 제외)
ls -l
# 모든 파일 목록 출력 (숨긴 파일 포함)
ls -al
# 재귀적 파일 정보 조회
ls -alR
ls -lR
ls -R

# 디렉토리 이동

# 상위 폴더 이동
cd ..
pwd
# 홈 디렉토리 이동
cd !
pwd 
# 특정 디렉토리 이동
cd Desktop
pwd
# 최상위 디렉토리 이동
cd /
pwd
ls
# 홈 디렉토리 이동
cd 
pwd

# 파일 관리
# 파일 생성
touch abc.txt
# 파일 목록 출력
ls 
# 텍스트 화면 출력
echo "Hello"
echo Good Morning
# 출력 내용을 파일로 저장
echo "Hello" > abc.txt
# 파일 내용 화면 출력
cat abc.txt
# 출력 내용을 파일에 추가
echo "Good Morning" >> abc.txt
# 파일 내용 화면 출력
cat abc.txt
# 파일 복사
cp abc.txt def.txt
# 파일 목록 출력
ls
# 파일 내용 화면 출력
cat abc.txt
# 파일 이름 변경
mv def.txt ghi.txt
# 파일 내용 화면 출력
cat ghi.txt
# 파일 삭제
rm ghi.txt
# 파일 목록 출력
ls
# 심롤릭 링크 바로 가기 생성
ln -s abc.txt def.txt
# 파일 내용 화면 출력
cat def.txt
# 하드 링크 생성
ln abc.txt ghi.txt
# 출력 내용 파일 추가
echi "Nice to meet you" >> abc.txt
# 파일 내용 화면 출력
cat ghi.txt

# 디렉토리 관리










