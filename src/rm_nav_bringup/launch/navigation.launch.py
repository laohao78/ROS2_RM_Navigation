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
    # Get the launch directory
    navigation2_launch_dir = os.path.join(get_package_share_directory('rm_navigation'), 'launch')
    rm_nav_bringup_dir = get_package_share_directory('rm_nav_bringup')

    # 外参数-world
    world = LaunchConfiguration('world')
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value='RMUL2026H',
        description='Select world (map file, pcd file, world file share the same name prefix as the this parameter)')

    # 外参数-use_sim_time
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')
        
 
    # Create the launch configuration variables
    use_nav_rviz = LaunchConfiguration('nav_rviz')
    declare_nav_rviz_cmd = DeclareLaunchArgument(
        'nav_rviz',
        default_value='True',
        description='Visualize navigation2 if true')

    ################################### navigation2 parameters start ##################################
    nav2_map_dir = PathJoinSubstitution([rm_nav_bringup_dir, 'map', world]), ".yaml"
    nav2_params_file_dir = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'nav2_params_sim.yaml')
    ################################### navigation2 parameters end ####################################

    # Specify the actions
    start_navigation2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(navigation2_launch_dir, 'bringup_rm_navigation.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': nav2_map_dir,
            'params_file': nav2_params_file_dir,
            'nav_rviz': use_nav_rviz}.items()
    )

    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_nav_rviz_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_use_sim_time_cmd)

    ld.add_action(start_navigation2)

    return ld
