cmake_minimum_required( VERSION 3.10 )
project( OpenCVExample )

set( OpenCV_DIR "C:/opencv/build" ) # OpenCV directory
set( CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE )
set( OpenCV_INCLUDE_DIR "C:/opencv/build/install/include" ) # include directories

find_package( OpenCV REQUIRED ) # find OpenCV
include_directories( OpenCV_INCLUDE_DIR ) # include directories
add_executable( opencv_dll_example example.cpp ) # add executable
target_link_libraries( opencv_dll_example PRIVATE ${OpenCV_LIBS} ) # link libraries

message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    config: ${OpenCV_DIR}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIR}")
message(STATUS "    libraries: ${OpenCV_LIBS}")