cmake_minimum_required(VERSION 3.10)
project(OpenCV_Static_Example)

# C++ 표준 설정
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# OpenCV를 정적 라이브러리로 사용하도록 설정
set(BUILD_SHARED_LIBS OFF)
set(OpenCV_STATIC ON)
add_definitions(-DOPENCV_STATIC)

# UTF-8 인코딩 강제 적용
add_compile_options(/utf-8)
add_link_options(/ignore:4099)

# 멀티스레딩 런타임 라이브러리 사용 설정
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")

# OpenCV 디렉토리 설정
set(OpenCV_DIR "C:/opencv/build")  # OpenCV CMake 경로
set(OpenCV_INCLUDE_DIR "${OpenCV_DIR}/install/include")  # OpenCV 헤더 경로
set(OpenCV_LIB_DIR "${OpenCV_DIR}/install/x64/vc17/staticlib")  # OpenCV 라이브러리 경로

set( CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE )
find_package(OpenCV REQUIRED)

# OpenCV 버전 문자열 생성 (예: 4120)
set(OpenCV_VERSION_STR "${OpenCV_VERSION_MAJOR}${OpenCV_VERSION_MINOR}${OpenCV_VERSION_PATCH}")

# 실행 파일 생성
add_executable(opencv_static main.cpp)

# include 경로 추가
#target_include_directories(opencv_static PRIVATE ${OpenCV_INCLUDE_DIRS})
include_directories( ${OpenCV_INCLUDE_DIR} )

# 라이브러리 경로 추가
target_link_directories(opencv_static PRIVATE ${OpenCV_LIB_DIR})

# 디버그 및 릴리즈 라이브러리 설정
target_link_libraries(opencv_static PRIVATE
    $<$<CONFIG:Debug>:opencv_world${OpenCV_VERSION_STR}d.lib opencv_img_hash${OpenCV_VERSION_STR}d.lib>
    $<$<CONFIG:Debug>:aded.lib IlmImfd.lib ippicvmt.lib ippiwd.lib ittnotifyd.lib>
    $<$<CONFIG:Debug>:libjpeg-turbod.lib libopenjp2d.lib libpngd.lib libprotobufd.lib>
    $<$<CONFIG:Debug>:libtiffd.lib libwebpd.lib zlibd.lib>

    $<$<CONFIG:Release>:opencv_world${OpenCV_VERSION_STR}.lib opencv_img_hash${OpenCV_VERSION_STR}.lib>
    $<$<CONFIG:Release>:ade.lib IlmImf.lib ippicvmt.lib ippiw.lib ittnotify.lib>
    $<$<CONFIG:Release>:libjpeg-turbo.lib libopenjp2.lib libpng.lib libprotobuf.lib>
    $<$<CONFIG:Release>:libtiff.lib libwebp.lib zlib.lib>
)

# 디버깅 메시지 출력
message(STATUS "OpenCV library status:")
message(STATUS "    현재 빌드 모드: ${CMAKE_BUILD_TYPE}")
message(STATUS "    OpenCV version: ${OpenCV_VERSION}")
message(STATUS "    OpenCV_DIR: ${OpenCV_DIR}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
