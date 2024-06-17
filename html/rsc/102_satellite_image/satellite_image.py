# 기상 위성 영상 조회
# https://nmsc.kma.go.kr/homepage/html/satellite/viewer/selectNewSatViewer.do?dataType=operSat
#
# 기상청_위성영상 조회서비스 신청
# https://www.data.go.kr/data/15058167/openapi.do
#
# OpenAPI 정보
#
# 위성구분, 영상구분, 지역구분, 시간 조건을 이용하여 MTSAT 위성 이미지파일 정보를 조회하는 기능
# 요청주소 http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit
# 서비스URL http://apis.data.go.kr/1360000/SatlitImgInfoService
#
# 요청변수(Request Parameter)
#
# 항목명(국문)	항목명(영문)	항목크기	항목구분	샘플데이터	항목설명
# 서비스키	ServiceKey	100	필	-	공공데이터포털에서 받은 인증키
# 페이지 번호	pageNo	4	필	1	페이지번호 Default: 1
# 한 페이지 결과 수	numOfRows	4	필	10	한 페이지 결과 수
# 응답자료 형식	dataType	4	옵	XML	요청자료형식(XML/JSON) Default: XML
# 위성구분	sat	1	필	G2	위성구분 -G2: 천리안위성 2A호
#
# 영상구분	data	4	필	ir105	영상구분 -적외영상(ir105) -가시영상(vi006) -수증기영상(wv069) -단파적외영상(sw038) -RGB 컬러(rgbt) -RGB 주야간합성(rgbdn)
#
# 지역구분	area	2	필	ko	지역구분 -전구(fd) -동아시아(ea) -한반도(ko)
#
# 시간	time	8	필	20200423	년월일(YYYYMMDD)
#
#
# 출력결과(Response Element)
#
# 항목명(국문)	항목명(영문)	항목크기	항목구분	샘플데이터	항목설명
# 결과코드	resultCode	2	필	00	결과코드
# 결과메시지	resultMsg	100	필	NOMAL SERVICE	결과메시지
# 한 페이지 결과 수	numOfRows	4	필	10	한 페이지 결과 수
# 페이지 번호	pageNo	4	필	1	페이지번호
# 데이터 총 개수	totalCount	4	필	1	데이터 총 개수
# 응답자료 형식	dataType	4	필	XML	요청자료형식(XML/JSON) Default: XML
# 파일배열	satImgC-file	400	필	예제 참조	위성영상 이미지 파일명 배열 -파일명 마지막 부분 # 년월일시분은 UTC(한국 표준시 -9시간) 기준에 따름
#

import importlib
import subprocess
import sys

# 동적 패키지 임포트
def install_and_import(package):
    try:
        # 패키지 임포트 시도
        importlib.import_module(package)
    except ImportError:
        # 패키지가 설치되어 있지 않으면 설치
        print(f"{package} 패키지가 설치되어 있지 않습니다. 설치를 시도합니다.")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        # 설치 후 다시 임포트 시도
        importlib.import_module(package)
    pass
pass

# 동적 패키지 임포트

for package in [ "requests", "pathlib" ]  :
    install_and_import(package)
pass

import requests
import pathlib
import json

# dictionary key를 속성으로 접근하는 클래스
class AttrDict:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                value = AttrDict(value)
            pass
        
            self.__dict__[key] = value
        pass
    pass
pass

# 1. 기상청 API 키 설정
# 기상청에서 발급받은 API 키를 입력하세요.
API_KEY = "YOUR_API_KEY" 
API_KEY = "VYvCIN07GWWXrxMyV7Gyyqs%2Bp7acaRleqrBZntsNR5%2F5Bwpy5H4uwE%2B7Rz2tiQWjSKttTX1QgapIc8hJQ1szRw%3D%3D"

def load_satellite_image( date, area, image_klass ) : 

    # 2. API 요청 URL 구성
    base_url = 'http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit'

    params = {
        'serviceKey': API_KEY,
        'numOfRows': 10000,  # 한 번에 조회할 데이터 수
        'pageNo': 1,      # 페이지 번호
        'dataType': 'JSON',  # 데이터 타입 (JSON 또는 XML)
        'sat': 'g2',       # 위성 종류 (예: G2 - 천리안2A)
        # 영상구분 : 적외영상(ir105), 가시영상(vi006), 수증기영상(wv069), 단파적외영상(sw038), 
        #           RGB컬러(rgbt), RGB주야간합성(rgbdn)
        'data' : image_klass,
        'area' : area, # 지역구분 : 전구(fd), 동아시아(ea), 한반도(ko) 
        'time' : date, # 조회 날짜 (예: 2024년 1월 1일) 
    }

    # 3. API 요청 보내기
    response = requests.get(base_url, params=params)

    # 4. 응답 데이터 처리 및 파일 저장
    if response.status_code == 200:
        jsonData = None 
        
        try :
            jsonData = response.json() 
        except:
            pass
        pass

        if jsonData is None :
            print( "Response fail" ) 

            return
        pass

        jsonData = AttrDict( jsonData )

        resultCode = jsonData.response.header.resultCode
        resultMsg = jsonData.response.header.resultMsg

        print( "resultCode: ", resultCode )
        print( "resultMsg: ", resultMsg )

        if resultCode != "00" :
            print( "Result fail" )
        elif resultCode == "00" :
            print( "Result success" )
        pass

        #print( "Response: ", response.text )
        
        # 저장할 파일명 설정 (예: 조회 날짜와 시간 기준으로 파일명 설정)
        file_name = f"satellite_image_{params['time']}_{params['area']}_{params['data']}.json"
        
        from pathlib import Path
        src_dir = Path( __file__ ).resolve().parent

        # JSON 데이터를 파일로 저장
        with open( src_dir.joinpath( file_name ), 'w', encoding='utf-8') as file:
            file.write( response.text )
        pass
        
        print(f"파일이 성공적으로 저장되었습니다: {file_name}")
    else :
        print(f"API 요청 실패: {response.status_code}")
        print(response.text)
    pass

pass

if __name__ == "__main__" :
    
    date = "20240616"
    area = "ko"
    image_klass = "ir105"

    load_satellite_image( date, area, image_klass )
pass

