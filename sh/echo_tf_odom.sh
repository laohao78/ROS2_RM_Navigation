ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map odom
# 机器人在全局地图中的真实位姿
ros2 run tf2_ros tf2_echo map base_link
ros2 run tf2_ros tf2_echo odom base_link

ros2 topic list
ros2 topic echo /pose
ros2 topic echo /odom
ros2 topic echo /Odometry