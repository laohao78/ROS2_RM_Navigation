# 启动动态障碍地图
```sh
# 启动 Gazebo 加载该 world
gazebo /home/ros2/Desktop/pb_rmsimulation/src/rm_simulation/pb_rm_simulation/world/obstacles/worlds/obstacle1.world --verbose
```


- src/obstacle1.cc:







# 运动路径库编译
```sh
# 1. 进入插件目录
cd src/rm_simulation/pb_rm_simulation/world/obstacles

# 2. 创建build目录（若已存在，先清空）
mkdir -p build && cd build
rm -rf *  # 清空旧编译文件（可选）

# 3. 执行cmake（解析优化后的CMakeLists.txt）
cmake ..

# 4. 仅编译obstacle1（快速，不用等所有插件）
cd build
make obstacle1

# 5. 验证.so文件是否生成到lib目录
cd ..
ls lib
```