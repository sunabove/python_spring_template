# c++ opencv project using opencv_world.lib

cmake_minimum_required( VERSION 3.10 )
project( OpenCV_Static_Example )

# C++ 표준 설정
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(BUILD_SHARED_LIBS OFF)
set(OpenCV_STATIC ON)
add_definitions(-DOPENCV_STATIC)
# UTF-8 인코딩 강제 적용
add_compile_options(/utf-8)
add_link_options(/ignore:4099)

set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")

set( OpenCV_DIR "C:/opencv/build" ) # OpenCV directory
set( CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE )
set( OpenCV_INCLUDE_DIR "C:/opencv/build/install/include" ) # include directories

# OpenCV를 정적 라이브러리로 사용하도록 설정
set(BUILD_SHARED_LIBS OFF)
set(OpenCV_STATIC ON)

find_package( OpenCV REQUIRED ) # find OpenCV

add_executable( opencv_static main.cpp ) # add executable
include_directories( "C:/opencv/build/install/include" ) # include directories

target_link_directories( opencv_static PRIVATE "C:/opencv/build/install/x64/vc17/staticlib" )

# 디버그 모드와 릴리즈 모드의 라이브러리 분리
target_link_libraries(opencv_static PRIVATE
    $<$<CONFIG:Debug>:opencv_world4120d.lib>
    $<$<CONFIG:Debug>:opencv_img_hash4120d.lib>
    $<$<CONFIG:Debug>:aded.lib>
    $<$<CONFIG:Debug>:IlmImfd.lib>
    $<$<CONFIG:Debug>:ippicvmt.lib>
    $<$<CONFIG:Debug>:ippiwd.lib>
    $<$<CONFIG:Debug>:ittnotifyd.lib>
    $<$<CONFIG:Debug>:libjpeg-turbod.lib>
    $<$<CONFIG:Debug>:libopenjp2d.lib>
    $<$<CONFIG:Debug>:libpngd.lib>
    $<$<CONFIG:Debug>:libprotobufd.lib>
    $<$<CONFIG:Debug>:libtiffd.lib>
    $<$<CONFIG:Debug>:libwebpd.lib>
    $<$<CONFIG:Debug>:zlibd.lib>

    $<$<CONFIG:Release>:opencv_world4120.lib>
    $<$<CONFIG:Release>:opencv_img_hash4120.lib>
    $<$<CONFIG:Release>:ade.lib>
    $<$<CONFIG:Release>:IlmImf.lib>
    $<$<CONFIG:Release>:ippicvmt.lib>
    $<$<CONFIG:Release>:ippiw.lib>
    $<$<CONFIG:Release>:ittnotify.lib>
    $<$<CONFIG:Release>:libjpeg-turbo.lib>
    $<$<CONFIG:Release>:libopenjp2.lib>
    $<$<CONFIG:Release>:libpng.lib>
    $<$<CONFIG:Release>:libprotobuf.lib>
    $<$<CONFIG:Release>:libtiff.lib>
    $<$<CONFIG:Release>:libwebp.lib>
    $<$<CONFIG:Release>:zlib.lib>
)

message(STATUS "OpenCV library status:")
message(STATUS "현재 빌드 모드: ${CMAKE_BUILD_TYPE}")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    config: ${OpenCV_DIR}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIR}")
message(STATUS "    OpenCV_LIB_PATH: ${OpenCV_LIB_PATH}")
message(STATUS "    libraries: ${OpenCV_LIBS}")