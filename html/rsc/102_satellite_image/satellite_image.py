#
# 기상 위성 영상 조회
# https://nmsc.kma.go.kr/homepage/html/satellite/viewer/selectNewSatViewer.do?dataType=operSat
#
# 기상청_위성영상 조회서비스 신청
# https://www.data.go.kr/data/15058167/openapi.do
#
# OpenAPI 정보
#
# 위성구분, 영상구분, 지역구분, 시간 조건을 이용하여 MTSAT 위성 이미지파일 정보를 조회하는 기능
#
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
# 영상구분	data	4	필	ir105	영상구분 -적외영상(ir105) -가시영상(vi006) 
#        -수증기영상(wv069) -단파적외영상(sw038) -RGB 컬러(rgbt) -RGB 주야간합성(rgbdn)
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
# 파일배열	satImgC-file	400	필	예제 참조	위성영상 이미지 파일명 배열 
#    - 파일명 마지막 부분 년월일시분은 UTC(한국 표준시 -9시간) 기준에 따름
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
from pathlib import Path
from datetime import datetime, timedelta

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

def load_satellite_image( api_key ) : 

    # 현재 소스 폴더
    srcDir = Path( __file__ ).resolve().parent

    # 2. API 요청 URL 구성
    base_url = 'http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit'

    date = "20240616"
    yesterday = datetime.today() - timedelta(days=1)
    date = ( yesterday ).strftime('%Y%m%d')

    area = "ko"
    image_klass = "ir105"

    print( f"date = {date}, area = {area}, image_klass = {image_klass}" )

    dateYmd = date[0:4] + "-" + date[4:6] + "-" + date[6:]

    dataDir = srcDir.joinpath( "data" )
    dataDir.mkdir(parents=1, exist_ok=1)

    if not dataDir.exists() or not dataDir.is_dir() :
        print( f"데이터 폴더가 없습니다." )

        return -1
    pass

    imgDir = dataDir.joinpath( dateYmd )
    imgDir.mkdir(parents=1, exist_ok=1)

    if not imgDir.exists() or not imgDir.is_dir() :
        print( f"이미지 폴더({imgDir.name})가 없습니다.")

        return -1
    pass

    completeTxt = imgDir.joinpath( "complete.txt" )

    if completeTxt.exists() :
        print( "이미 완료되었습니다." )

        return -1
    pass

    params = {
        'serviceKey': api_key,
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
    if response.status_code != 200:
        print(f"API 요청 실패: {response.status_code}")
        print(response.text)

        return -1
    pass
    
    jsonData = None 
    
    try :
        jsonData = response.json() 
    except:
        pass
    pass

    if jsonData is None :
        print( "Response fail. 잠시후 다시 시도하세요." ) 

        return -1
    pass

    jsonData = AttrDict( jsonData )

    resultCode = jsonData.response.header.resultCode
    resultMsg = jsonData.response.header.resultMsg

    print( "resultCode: ", resultCode )
    print( "resultMsg: ", resultMsg )

    if resultCode != "00" :
        print( "resultCode: 실패. 잠시후 재 시도" )

        return -1
    elif resultCode == "00" :
        print( "resultCode: 성공" )
    pass

    # 저장할 파일명 설정 (예: 조회 날짜와 시간 기준으로 파일명 설정)
    file_name = f"satellite_image_{params['time']}_{params['area']}_{params['data']}.json"

    # JSON 데이터를 파일로 저장
    with open( srcDir.joinpath( file_name ), 'w', encoding='utf-8') as file:
        file.write( response.text )
    pass
    
    print(f"파일이 성공적으로 저장되었습니다: {file_name}")

    item = jsonData.response.body.items.item[0]
    imgUrls = item[ "satImgC-file" ]
    imgUrls = imgUrls.replace( "[","" )
    imgUrls = imgUrls.replace( "]","" )
    imgUrls = imgUrls.replace( ", ","," )
    imgUrls = imgUrls.strip().split(",")

    for i, imgUrl in enumerate( imgUrls ) :
        try:
            # HTTP GET 요청을 보내서 이미지 데이터 가져오기
            response = requests.get( imgUrl )
            response.raise_for_status()  # HTTP 에러가 발생하면 예외 발생

            imgFileName = imgUrl[ imgUrl.rindex( "/") + 1 : ]
            imgFile = imgDir.joinpath( imgFileName )
            # 이미지 데이터를 파일로 저장
            with open( imgFile, 'wb') as file:
                file.write(response.content)

                print( f"[{i:04d}] 이미지가 성공적으로 저장되었습니다: { imgFileName }" )
            pass
            
        except Exception as e:
            print( f"[{i:04d}] 이미지 다운로드 중 오류가 발생했습니다: {e}" )
        pass
    pass

    completeTxt.touch( exist_ok=True )
    print(f"완료 파일이 생성되었습니다. { completeTxt.name }")

pass

if __name__ == "__main__" :

    # 1. 기상청 API 키 설정
    # 기상청에서 발급받은 API 키를 입력하세요.
    API_KEY = "YOUR_API_KEY" 
    API_KEY = "VYvCIN07GWWXrxMyV7Gyyqs%2Bp7acaRleqrBZntsNR5%2F5Bwpy5H4uwE%2B7Rz2tiQWjSKttTX1QgapIc8hJQ1szRw%3D%3D"

    if 1 : 
        load_satellite_image( API_KEY )
    pass
pass
