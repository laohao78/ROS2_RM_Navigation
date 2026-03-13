source install/setup.bash
ros2 launch rm_nav_bringup bringup_sim.launch.py \
world:=RMUL2026H \
mode:=nav \
lio:=fastlio \
localization:=slam_toolbox \
lio_rviz:=False \
nav_rviz:=True