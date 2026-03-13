## 机器人导航参数说明

### 1. 机器人运动相关
- **max_vel_x / max_vel_y / max_vel_theta**  
  最大速度（影响安全与性能）
- **acc_lim_x / acc_lim_y / acc_lim_theta**  
  最大加速度（影响响应与安全）
- **robot_radius**  
  机器人半径（影响避障与路径规划）
- **xy_goal_tolerance / yaw_goal_tolerance**  
  到达目标的容差（影响导航精度）

---

### 2. 局部/全局代价地图
- **resolution**  
  地图分辨率（影响精度与计算量）
- **inflation_radius / cost_scaling_factor**  
  膨胀参数（影响避障距离与路径选择）
- **plugins**  
  地图层插件（决定障碍物处理方式）

---

### 3. TEB 局部规划器
- **dt_ref / controller_frequency**  
  控制频率与轨迹分辨率（影响运动平滑性）
- **min_obstacle_dist / inflation_dist**  
  障碍物距离（影响安全性）
- **enable_homotopy_class_planning**  
  是否多路径规划（影响复杂场景表现）

---

### 4. AMCL 定位
- **max_particles / min_particles**  
  粒子数（影响定位精度与速度）
- **`laser_model_type`**  
  激光模型（影响定位效果）
- **`base_frame_id / global_frame_id / odom_frame_id`**  
  坐标系设置（必须正确）

---

### 5. 速度平滑器
- **max_velocity / min_velocity / max_accel / max_decel**  
  速度与加速度限制（影响运动安全）

---

### 6. 其他
- **`use_sim_time`**  
  是否使用仿真时间（仿真/实车切换时需注意）
- **`scan_topic`**  
  激光雷达话题名（需与实际设备一致）