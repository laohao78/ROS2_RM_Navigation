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

    rm_nav_bringup_dir = get_package_share_directory('rm_nav_bringup')
    navigation2_launch_dir = os.path.join(get_package_share_directory('rm_navigation'), 'launch')


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

    # 外参数-mode
    declare_mode_cmd = DeclareLaunchArgument(
        'mode',
        default_value='',
        description='Choose mode: nav, mapping')    

    ################################## slam_toolbox parameters start ##################################
    slam_toolbox_map_dir = PathJoinSubstitution([rm_nav_bringup_dir, 'map', world])
    slam_toolbox_localization_file_dir = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'mapper_params_localization_sim.yaml')
    slam_toolbox_mapping_file_dir = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'mapper_params_online_async_sim.yaml')
    ################################### slam_toolbox parameters end ###################################

    ################################### navigation2 parameters start ##################################
    nav2_map_dir = PathJoinSubstitution([rm_nav_bringup_dir, 'map', world]), ".yaml"
    nav2_params_file_dir = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'nav2_params_sim.yaml')
    ################################### navigation2 parameters end ####################################

    ################################ icp_registration parameters start ################################
    icp_pcd_dir = PathJoinSubstitution([rm_nav_bringup_dir, 'PCD', world]), ".pcd"
    icp_registration_params_dir = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'icp_registration_sim.yaml')
    ################################# icp_registration parameters end #################################

    ############################# pointcloud_downsampling parameters start ############################
    pointcloud_downsampling_config_dir = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'pointcloud_downsampling_sim.yaml')
    ############################# pointcloud_downsampling parameters start ############################

    declare_localization_cmd = DeclareLaunchArgument(
        'localization',
        default_value='',
        description='Choose localization method: slam_toolbox, amcl, icp')

    start_localization_group = GroupAction(
        condition = LaunchConfigurationEquals('mode', 'nav'),
        actions=[
            Node(
                condition = LaunchConfigurationEquals('localization', 'slam_toolbox'),
                package='slam_toolbox',
                executable='localization_slam_toolbox_node',
                name='slam_toolbox',
                parameters=[
                    slam_toolbox_localization_file_dir,
                    {'use_sim_time': use_sim_time,
                    'map_file_name': slam_toolbox_map_dir,
                    'map_start_pose': [0.0, 0.0, 0.0]}
                ],
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(navigation2_launch_dir,'localization_amcl_launch.py')),
                condition = LaunchConfigurationEquals('localization', 'amcl'),
                launch_arguments = {
                    'use_sim_time': use_sim_time,
                    'params_file': nav2_params_file_dir}.items()
            ),

            TimerAction(
                period=7.0,
                actions=[
                    Node(
                        condition=LaunchConfigurationEquals('localization', 'icp'),
                        package='icp_registration',
                        executable='icp_registration_node',
                        output='screen',
                        parameters=[
                            icp_registration_params_dir,
                            {'use_sim_time': use_sim_time,
                                'pcd_path': icp_pcd_dir}
                        ],
                        # arguments=['--ros-args', '--log-level', ['icp_registration:=', 'DEBUG']]
                    )
                ]
            ),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(navigation2_launch_dir, 'map_server_launch.py')),
                condition = LaunchConfigurationNotEquals('localization', 'slam_toolbox'),
                launch_arguments={
                    'use_sim_time': use_sim_time,
                    'map': nav2_map_dir,
                    'params_file': nav2_params_file_dir,
                    'container_name': 'nav2_container'}.items())
        ]
    )

    start_mapping = Node(
        condition = LaunchConfigurationEquals('mode', 'mapping'),
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[
            slam_toolbox_mapping_file_dir,
            {'use_sim_time': use_sim_time,}
        ],
    )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_localization_cmd)
    ld.add_action(declare_mode_cmd)
    ld.add_action(declare_world_cmd)

    ld.add_action(start_localization_group)
    ld.add_action(start_mapping)

    return ld