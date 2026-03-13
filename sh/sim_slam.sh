source install/setup.bash
ros2 launch rm_nav_bringup bringup_sim.launch.py \
world:=RMUL2026H \
mode:=mapping \
lio:=fastlio \
lio_rviz:=False \
nav_rviz:=True