cmake_minimum_required(VERSION 3.10)
project(obstacles_plugin)

find_package(gazebo REQUIRED)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)

include_directories(${GAZEBO_INCLUDE_DIRS})
add_compile_options(${GAZEBO_CXX_FLAGS})

# 列出所有源文件（带 src/ 前缀）
set(OBSTACLE_SOURCES
    src/obstacle1.cc
    src/obstacle2.cc
    src/obstacle3.cc
    src/obstacle4.cc
    src/obstacle5.cc
    src/obstacle6.cc
    src/obstacle7.cc
    src/obstacle8.cc
    src/obstacle9.cc
    src/obstacle10.cc
    src/obstacle11.cc
    src/obstacle12.cc
    src/obstacle13.cc   # 你有 obstacle13.cc！别漏了
    src/obstacles.cc
)

foreach(src_file ${OBSTACLE_SOURCES})
    get_filename_component(target_name ${src_file} NAME_WE)
    add_library(${target_name} SHARED ${src_file})
    target_link_libraries(${target_name} ${GAZEBO_LIBRARIES})
endforeach()