cmake_minimum_required(VERSION 3.8)
project(rm_serial_driver)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# =====================
# 依赖库
# =====================
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# =====================
# 头文件路径
# =====================
include_directories(
  include
  /usr/include
  include/serial
)

# =====================
# 源文件
# =====================
add_executable(${PROJECT_NAME}
  src/rm_serial_driver.cpp
)

# =====================
# 链接依赖库
# =====================
find_package(geometry_msgs REQUIRED)
ament_target_dependencies(${PROJECT_NAME}
  rclcpp
  std_msgs
  geometry_msgs
)

# 链接系统中的 libserial.so
target_link_libraries(${PROJECT_NAME}
  serial
)

# =====================
# 安装规则
# =====================
install(TARGETS ${PROJECT_NAME}
  DESTINATION lib/${PROJECT_NAME}
)

# 安装 launch 文件
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

# 安装参数文件
install(DIRECTORY params
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
