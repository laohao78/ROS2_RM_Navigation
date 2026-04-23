# RM_Navigation - ROS2 导航仿真与实车系统

> 基于ROS2的全向移动机器人导航系统，支持Gazebo仿真和真实机器人部署

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![ROS2](https://img.shields.io/badge/ROS2-Humble-green)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange)

## 📋 项目概述

MY_nav 是一个功能完整的ROS2导航解决方案，集成了以下核心功能：

- **感知模块**：Livox Mid360激光雷达、IMU数据处理
- **定位模块**：Fast-LIO、Point-LIO、SLAM-Toolbox、AMCL、ICP等多种定位算法
- **规划模块**：Navigation2框架、TEB局部规划器、全局路径规划
- **仿真环境**：Gazebo Classic 11仿真环境（RMUL/RMUC地图）
- **实车支持**：完整的硬件驱动与参数配置

## 🚀 快速开始

### 系统要求

- **操作系统**：Ubuntu 22.04 LTS
- **ROS2版本**：Humble
- **Gazebo**：Classic 11.10.0+
- **编译器**：GCC 11+

### 安装依赖

```bash
# 安装系统依赖
sudo apt update && sudo apt install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-pointcloud-to-laserscan \
    gazebo-classic

# 安装Livox SDK2
git clone https://github.com/Livox-SDK/Livox-SDK2.git
cd Livox-SDK2
mkdir build && cd build
cmake .. && make -j && sudo make install
```

### 编译项目

```bash
cd /home/ros2/Desktop/MY_nav
colcon build --symlink-install
source install/setup.bash
```

## 📖 使用指南

### 仿真模式 - 边建图边导航

```bash
ros2 launch rm_nav_bringup bringup_sim.launch.py \
    world:=RMUL2026H \
    mode:=mapping \
    lio:=fastlio \
    lio_rviz:=False \
    nav_rviz:=True
```

### 仿真模式 - 已知地图导航

```bash
ros2 launch rm_nav_bringup bringup_sim.launch.py \
    world:=RMUL2026H \
    mode:=nav \
    lio:=fastlio \
    localization:=slam_toolbox \
    lio_rviz:=False \
    nav_rviz:=True
```

### 真实机器人 - 边建图边导航

```bash
ros2 launch rm_nav_bringup bringup_real.launch.py \
    world:=YOUR_MAP_NAME \
    mode:=mapping \
    lio:=fastlio \
    lio_rviz:=False \
    nav_rviz:=True
```

### 真实机器人 - 已知地图导航

```bash
ros2 launch rm_nav_bringup bringup_real.launch.py \
    world:=YOUR_MAP_NAME \
    mode:=nav \
    lio:=fastlio \
    localization:=slam_toolbox \
    lio_rviz:=False \
    nav_rviz:=True
```

### 可选参数说明

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `world` | `RMUL`, `RMUC`, `RMUL2026H` | 仿真地图或真实地图名称 |
| `mode` | `mapping`, `nav` | 建图模式或导航模式 |
| `lio` | `fastlio`, `pointlio` | 选择定位算法 |
| `localization` | `slam_toolbox`, `amcl`, `icp` | 定位方式（仅nav模式） |
| `nav_rviz` | `True`, `False` | 是否启动可视化 |

## 📁 项目结构

```
MY_nav/
├── src/
│   ├── driver/                    # 硬件驱动
│   │   ├── livox_ros_driver2/    # Livox雷达驱动
│   │   ├── livox_sdk2/           # Livox SDK
│   │   └── rm_serial_driver/     # 串口通信
│   ├── gazebo/                    # Gazebo仿真相关
│   │   ├── pb_rm_simulation/     # 仿真环境
│   │   └── livox_laser_simulation/ # 雷达仿真
│   ├── localization/              # 定位模块
│   │   ├── FAST_LIO/             # Fast-LIO算法
│   │   ├── point_lio/            # Point-LIO算法
│   │   └── icp_registration/     # ICP定位
│   ├── navigation/                # 导航模块
│   │   ├── teb_local_planner/    # TEB局部规划
│   │   ├── costmap_converter/    # 代价地图转换
│   │   └── rm_navigation/        # Nav2集成
│   ├── processing/                # 数据处理
│   │   ├── imu_complementary_filter/ # IMU滤波
│   │   ├── pointcloud_to_laserscan/  # 点云转扫描
│   │   └── linefit_ground_segmentation/ # 地面分割
│   └── rm_nav_bringup/           # 启动配置
├── build/                         # 编译输出
├── install/                       # 安装输出
├── README.md                      # 项目文档
└── LICENSE                        # 开源许可证
```

## 🔧 核心功能模块

### 感知系统
- **雷达**：Livox Mid360 点云传感器
- **IMU**：9轴惯性测量单元
- **处理**：点云滤波、地面分割、格式转换

### 定位系统
- **Fast-LIO**：实时SLAM系统，约10Hz输出
- **Point-LIO**：高频率定位，支持100+Hz输出
- **SLAM-Toolbox**：动态环境定位效果好
- **AMCL**：粒子滤波经典算法
- **ICP**：点云配准定位

### 规划系统
- **全局规划**：Dijkstra算法（NavfnPlanner）
- **局部规划**：TEB（Timed Elastic Band）轨迹优化
- **代价地图**：多层融合（静态层、障碍层、膨胀层、时空体素层）

### 坐标系统
```
map → odom → base_link
  ↓        ↓         ↓
全局定位  里程计   机器人本体
（SLAM）  （驱动）
```

## 🎮 遥控与测试

### 键盘遥控
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### 模拟速度指令
```bash
python3 src/rm_driver/rm_serial_driver/src/test_cmd_vel_pub.py
```

## 📊 话题接口

### Gazebo仿真话题
- `/clock` - 仿真时钟
- `/cmd_vel_chassis` - 底盘速度指令
- `/livox/lidar` - 雷达点云数据
- `/livox/imu` - IMU数据
- `/joint_states` - 关节状态

### 导航核心话题
- `/goal_pose` - 导航目标点
- `/initialpose` - 初始位姿
- `/cmd_vel_nav` - 导航速度指令
- `/global_plan` - 全局路径
- `/local_plan` - 局部路径

## 🛠️ 实车适配指南

### 1. 雷达IP配置
编辑 `src/rm_nav_bringup/config/reality/MID360_config.json`：
```json
{
  "lidar_configs": {
    "ip": "YOUR_LIDAR_IP"
  }
}
```

### 2. 雷达位姿标定
编辑 `src/rm_nav_bringup/config/reality/measurement_params_real.yaml`：
```yaml
lidar_to_base_link:
  x: 0.0          # 雷达到机器人中心的X距离
  y: 0.0          # 雷达到机器人中心的Y距离
  z: 0.0          # 雷达到机器人中心的Z距离
```

### 3. 传感器高度配置
编辑 `src/rm_nav_bringup/config/reality/segmentation_real.yaml`：
```yaml
sensor_height: 0.0  # 雷达距地面高度
```

### 4. 地图文件准备
将地图文件放在对应目录：
```
src/rm_nav_bringup/map/
└── YOUR_MAP_NAME.yaml
└── YOUR_MAP_NAME.pgm

src/rm_nav_bringup/PCD/
└── YOUR_MAP_NAME.pcd
```

## 📝 地图管理

### 保存地图

#### 建图模式下保存PCD
```bash
# 1. 在fastlio配置中启用保存：
# src/rm_nav_bringup/config/reality/fastlio_mid360_real.yaml
pcd_save_en: true
pcd_path: "/path/to/YOUR_MAP_NAME.pcd"

# 2. 运行建图，然后保存
ros2 service call /map_save std_srvs/srv/Trigger
```

#### 保存SLAM-Toolbox地图
在RViz中使用SLAM-Toolbox提供的保存功能生成：
- `YOUR_MAP_NAME.pgm` - 栅格地图图像
- `YOUR_MAP_NAME.yaml` - 地图元数据
- `YOUR_MAP_NAME.data` - 位姿图数据
- `YOUR_MAP_NAME.posegraph` - 位姿图结构

## 🐛 故障排查

### 雷达不识别
```bash
# 查看设备
ls /dev/ttyACM* /dev/ttyUSB*

# 检查USB权限
sudo usermod -aG dialout $USER
# 重新登录生效
```

### TF不连通
```bash
# 查看TF树
ros2 run tf2_tools view_frames
python3 -m tf2_tools.view_frames  # 生成frames.pdf
```

### 定位漂移
- 调整LIO参数中的运动模型
- 检查地面分割高度配置
- 增加SLAM-Toolbox的闭环检测阈值

## 📚 算法参考

- **Fast-LIO**: https://github.com/hku-mars/FAST_LIO
- **Navigation2**: https://docs.nav2.org/
- **SLAM-Toolbox**: https://github.com/SteveMacenski/slam_toolbox
- **TEB Local Planner**: http://wiki.ros.org/teb_local_planner

## 📜 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

## 🙏 致谢

感谢以下开源项目的支持：
- ROS2 & Navigation2
- Gazebo Classic
- Livox SDK & Driver
- Fast-LIO & Point-LIO
- SLAM-Toolbox
- TEB Local Planner

---

**最后更新**：2026年4月23日
