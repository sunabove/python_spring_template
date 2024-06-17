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
# 영상구분	data	4	필	ir105	영상구분 -적외영상(ir105) -가시영상(vi006) -수증기영상(wv069) -단파적외영상(sw038) -RGB 컬러(rgbt) -RGB 주야간합성(rgbdn)
# 지역구분	area	2	필	ko	지역구분 -전구(fd) -동아시아(ea) -한반도(ko)
# 시간	time	8	필	20200423	년월일(YYYYMMDD)
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



