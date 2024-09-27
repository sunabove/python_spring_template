#!/usr/bin/python3

cmds = """
# vmware 데스크톱 툴 설치
sudo apt install open-vm-tools-desktop

# 프로그램 목록 업데이트
sudo apt update

# 프로그램 업그레이드
sudo apt upgrade -y

# 불필요 프로그램 삭제
sudo apt autoremove -y

# 필요시 재부팅
# sudo reboot

# python으로 python3 명령어 실행하는 프로그램
sudo apt install python-is-python3

# python pip 패키지 관리자 설치
sudo apt install python3-pip -y

# 파이썬 설정툴 설치
sudo apt install python3-setuptools -y

# 소프트웨어 소스 관리 도구 설치
sudo apt install software-properties-common -y

# 빌드 도구 설치
sudo apt install build-essential -y

# D-Bus API 설치
sudo apt install libdbus-glib-1-dev -y

# GObject Introspection을 지원하는 개발 패키지
sudo apt install libgirepository1.0-dev -y

# 파이썬 국제화(I18N)와 현지화(L10N) 서비스를 제공
sudo apt install gettext -y

# rsync 패키지 설치
sudo apt install librsync-dev -y

# cairo2 패키지 설치
sudo apt install libcairo2-dev -y

# systemd 패키지 설치
sudo apt install libsystemd-dev -y

# cups2 패키지 설치
sudo apt install libcups2-dev -y

# sudo apt install python3-pyqt5 -y
# sudo apt purge python3-pyqt5

# openblas 개발 패키지 설치
sudo apt install libopenblas-dev -y

# 파이썬 EXTERNALLY 제거
sudo rm /usr/lib/python3*/EXTERN*

# pip 패키지 관리자 업그레이드
sudo pip3 install pip --upgrade 

# dbus 패키지 설치
sudo pip3 install dbus-python

# packaging 패키지 설치
sudo pip3 install packaging

# pipdate 패키지 업데이트 관리자 설치
sudo pip3 install pipdate

# json-stats 패키지 설치
sudo pip3 install jetson-stats

# qtbase5 패키지 설치
sudo apt install qtbase5-dev -y

# samba 관련 프로그램 설치
sudo apt install smbclient libmaus2-2 libmaus2-dev -y

# glib2 관련 라이브러리 설치
sudo apt install libglib2.0-dev libsmbclient-dev libcups2-dev -y

# 불필요 프로그램 삭제
sudo apt autoremove -y

# 모든 파이썬 패키지 업데이트
sudo -H pipdate

"""

# os 모듈을 임포트하여 시스템 명령어 실행에 사용
import os 

# 명령어 문자열을 줄 단위로 나누어 리스트로 변환
cmds = cmds.strip().splitlines()

# 리스트의 각 명령어를 순차적으로 처리
for idx, cmd in enumerate(cmds):
    # 명령어 앞뒤 공백을 제거
    cmd = cmd.strip()

    # 명령어가 빈 문자열인 경우, 다음 루프로 넘어감
    if len(cmd) == 0:
        continue  # do nothing
    
    # 명령어가 주석(#)으로 시작하는 경우
    elif cmd.startswith("#"):
        # 주석에 "sudo"가 포함된 경우
        if "sudo" in cmd:
            pass  # 아무 작업도 하지 않음
        else:
            # 주석을 출력하여 현재 진행 상황을 사용자에게 알림
            print()
            print(cmd, flush=1)
        pass

        continue
    
    # 명령어가 주석이 아니고 실행 가능한 경우
    else:
        # 명령어를 출력하여 사용자에게 알림
        print()
        print(cmd, flush=1)

        # 명령어를 시스템에서 실행
        os.system(cmd)
    pass
pass
