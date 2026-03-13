source install/setup.bash
ros2 launch rm_nav_bringup bringup_real.launch.py \
world:=long \
mode:=nav \
lio:=fastlio \
localization:=slam_toolbox \
lio_rviz:=False \
nav_rviz:=True