from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

params_file = os.path.join(
    get_package_share_directory('rm_serial_driver'),
    'params',
    'params.yaml'
)

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rm_serial_driver',
            executable='rm_serial_driver',
            name='rm_serial_driver',
            parameters=[params_file],
            output='screen'
        )
    ])