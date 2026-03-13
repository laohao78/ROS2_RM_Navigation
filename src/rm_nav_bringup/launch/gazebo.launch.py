import os
import yaml

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, TimerAction
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch.conditions import LaunchConfigurationEquals, LaunchConfigurationNotEquals, IfCondition


def generate_launch_description():
    
    # 路径-pb_rm_simulation_launch_dir
    pb_rm_simulation_launch_dir = os.path.join(get_package_share_directory('pb_rm_simulation'), 'launch')
    
    # 外参数-use_sim_time
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')
        
    # 外参数-world
    world = LaunchConfiguration('world')
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value='RMUL2026H',
        description='Select world (map file, pcd file, world file share the same name prefix as the this parameter)')
    
    ################################ robot_description parameters start ###############################
    launch_params = yaml.safe_load(open(os.path.join(
    get_package_share_directory('rm_nav_bringup'), 'config', 'simulation', 'measurement_params_sim.yaml')))
    robot_description = Command(['xacro ', os.path.join(
    get_package_share_directory('rm_nav_bringup'), 'urdf', 'sentry_robot_sim.xacro'),
    ' xyz:=', launch_params['base_link2livox_frame']['xyz'], ' rpy:=', launch_params['base_link2livox_frame']['rpy']])
    ################################# robot_description parameters end ################################

    # 启动仿真
    start_rm_simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pb_rm_simulation_launch_dir, 'rm_simulation.launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'world': world,
            'robot_description': robot_description,
            'rviz': 'False'}.items()
    )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_world_cmd)
    
    ld.add_action(start_rm_simulation)

    return ld