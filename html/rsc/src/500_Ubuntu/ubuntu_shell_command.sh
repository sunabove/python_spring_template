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
# 디렉토리 만들기
mkdir abc
mkdir abc/def
# 파일 목록 조회
ls
# 폴더 목록 조회
ls abc
# 디렉토리 만들기( -p 옵션 사용 )
mkdir -p abc
# 디렉토리 만들기 (에러 발생)
mkdir abc
# 디렉토리 복가
cp -r abc def
# 파일 목록 조회
ls
# 디렉토리 이름 변경
mv def ghi
# 파일 목록 조회
ls
# 디렉토리 삭제 (에러 발생)
rm ghi
# 디렉토리 삭제
rm -r ghi
# 파일 목록 조회
ls

# 파일 내용 출력
# 샘플 파일 생성
ls -al >> abc.txt
# 파일 내용 출력
cat abc.txt
# 한 페이지씩 파일 출력
more abc.txt
# 파일의 첫 10줄 출력 
head abc.txt
# 파일의 마지막 10줄 출력
tail abc.txt

# 와일드 카드 사용
# 파일 복사
cp abc.txt abd.txt
# 파일 조회 (* 와일드 카드)
ls *.txt
# 파일 조회 (? 와일드 카드)
ls ab?.txt
# 파일 조회 (대괄호 와일드 카드)
ls ab[cd].txt
ls ab[c-e].txt
# 파일 조회 (중괄호 와일드 카드)
ls ab{c,d}.txt
# 홈 디렉토리 와일드 카드 (~)
ls ~

# 파일 권한 관리
# 폴더 생성
mkdir -p abc
# 폴더 이동
cd abc
# 폴더 생성
mkdir ghi
# 파일 정보 출력
ls -l
# 숫자로 파일 권한 설정
chmod -R 755 ghi
# 파일 정보 출력
ls -l
# 기호로 파일 권한 설정
chmod u+rwx,g+rx,o-r ghi
# 파일 정보 출력
ls -l

# 유용한 명령어들
# ls 도움말 출력
mans ls
# man 도울말 출력
man man
# ls 경로 출력
which ls
# which 경로 출력
which which
# 파일 단어 검색
grep Hello abc.txt
grep hello abc.txt
grep hello abc.txt -i
grep hello abc.txt -i -n

# 프로세스 관리
# 현재 쉘 프로세스 출력
ps
# 프로세스 아이디로 프로세스 강제 종료
kill -i {프로세스ID}
# ping 프로세스 실행 (두번째 터미널에서)
ping google.com
# 프로세스 이름으로 프로세스 강제 종료
killall ping

# 관리자 권한으로 명령어 실행
# 사용자 아이디 출력
whoami
# 관리자 아이디 출력
sudo whoami
# 프로그램 목록 업데이트
sudo apt update
# 프로그램 업그레이드
sudo apt upgrade

# 명령어 조합
# 여러 줄 명령어 입력 (\)
echo "Hello! Good Morning! Nice\
to meet you! "
# 여러 명령어 입력 ( ; )
whoami ; hostname -I ; pwd
# 두 개의 명령어 AND 연산 실행 (&&)
whoami && hostname -I && pwd
whoami && mkdir abc && pwd
whoami && mkdir -p abc && pwd
# 관리자 권한으로 프로그램 목록 업데이트 결과가 있으면,
# 관리자 권한으로 프로그램들을 업그레이드
sudo apt update && sudo apt upgrade -y 
# 파일 정보 출력을 파이프(|)로 연결하여 한 페이지씩 조회
ls -al | more
# 파일 정보 출력에서 ba 문자가 있는 줄만을 조회
ls -al | grep ba

# 명령어 단축
# clear 명령어를 c 명령어로 단축
alias c="clear"
# 단축 명령어 목록 조회
alias
# 단축 명령어 해제
unalias c
# 현재 줄 임시 단축 해제
\ls
\c

# 쉘 환경 설정
# tilde 편집기 설처
sudo apt install tilde -y
# .bashrc 편집
tilde ~/.bashrc
# 파일 최하단에 아래 내용 추가
alias c="clear"
hostname -I
echo "Hello... Good Moring!"
# 수정한 .bashrc 실행
source .bashrc
. .bashrc

# 명령어 이력 관리
# 명령어 이력 출력
history
# 최초 123 번째 명령어 실행
!123
# 최근 3번째 명령어 실행
!-3
# 직적 명령어 실행
!!
# 이전 명령어 수정
sudu apt update
^du^do
ls -al abf
^bf^bc
# 이전 명령어의 마지막 인수
touch my_text.txt
rm !$

# 파일 검색
# 홈 디렉토리 아래에서 abc.txt 파일 검색
find ~ -name "abc.txt"
# 홈 디렉토리 아래에서 ab*.txt 파일 검색
find ~ -name "ab*.txt"
# 홈 디렉토리 아래에서 파일 크기가 20MB 이상 파일 검색
find ~ -size +20M
# 홈 디렉토리 아래에서 파일 수정일이 하루 이내인 파일 검색
find ~ -mtime -1
# 홈 디렉토리 아래에서 폴더 검색 및 한 페이지 씩 출력
find ~ -type d | more
# 홈 디렉토리 아래에서 일반 파일 검색 및 한 페이지 씩 출력
find ~ -type f | more
# abc 폴더 아래의 bak 확장자 파일들을 모두 삭제
find abc -name *.bak -exec rm {} \; 
# abc 폴더 아래의 모든 폴더들의 권한을 755로 설정
find abc -type d -exec chmod 755 {} \;
# abc 폴더 아래의 모든 파일들의 권한을 644로 설정
find abc -type f -exec chmod 644 {} \;
# abc 폴더 아래의 크기가 10M Byte 이상인 mp3 파일들을 모두 삭제
find ~ -type f -name *.mp3 -size +10M -exec rm {} \;

# 끝