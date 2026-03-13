source install/setup.bash
ros2 launch rm_nav_bringup bringup_real.launch.py \
world:=YOUR_WORLD_NAME \
mode:=mapping  \
lio:=fastlio \
lio_rviz:=False \
nav_rviz:=True