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

    # 获取路径-rm_nav_bringup_dir
    rm_nav_bringup_dir = get_package_share_directory('rm_nav_bringup')


    # 外参数-use_sim_time
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')


    ########################## linefit_ground_segementation parameters start ##########################
    segmentation_params = os.path.join(rm_nav_bringup_dir, 'config', 'simulation', 'segmentation_sim.yaml')
    ########################## linefit_ground_segementation parameters end ############################



    bringup_imu_complementary_filter_node = Node(
        package='imu_complementary_filter',
        executable='complementary_filter_node',
        name='complementary_filter_gain_node',
        output='screen',
        parameters=[
            {'do_bias_estimation': True},
            {'do_adaptive_gain': True},
            {'use_mag': False},
            {'gain_acc': 0.01},
            {'gain_mag': 0.01},
        ],
        remappings=[
            ('/imu/data_raw', '/livox/imu'),
        ]
    )

    bringup_linefit_ground_segmentation_node = Node(
        package='linefit_ground_segmentation_ros',
        executable='ground_segmentation_node',
        output='screen',
        parameters=[segmentation_params]
    )

    bringup_pointcloud_to_laserscan_node = Node(
        package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
        remappings=[('cloud_in',  ['/segmentation/obstacle']),
                    ('scan',  ['/scan'])],
        parameters=[{
            'target_frame': 'livox_frame',
            'transform_tolerance': 0.01,
            'min_height': -1.0,
            'max_height': 0.1,
            'angle_min': -3.14159,  # -M_PI/2
            'angle_max': 3.14159,   # M_PI/2
            'angle_increment': 0.0043,  # M_PI/360.0
            'scan_time': 0.3333,
            'range_min': 0.45,
            'range_max': 10.0,
            'use_inf': True,
            'inf_epsilon': 1.0
        }],
        name='pointcloud_to_laserscan'
    )

    bringup_fake_vel_transform_node = Node(
        package='fake_vel_transform',
        executable='fake_vel_transform_node',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'spin_speed': 5.0 # rad/s 
        }]
    )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    
    ld.add_action(bringup_imu_complementary_filter_node)
    ld.add_action(bringup_linefit_ground_segmentation_node)
    ld.add_action(bringup_pointcloud_to_laserscan_node)
    ld.add_action(bringup_fake_vel_transform_node)

    return ld

