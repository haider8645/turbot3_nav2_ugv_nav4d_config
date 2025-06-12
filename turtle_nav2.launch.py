import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def launch_setup(context, *args, **kwargs):

    tasks = []

    # Get parameters from launch args
    nav2_parameters = LaunchConfiguration('nav2_param_path').perform(context)
    rviz_configuration = LaunchConfiguration('rviz_config_path').perform(context)

    tasks.append(
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[nav2_parameters]
        )
    )

    tasks.append(
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_configuration]
        )
    )

    return tasks

def generate_launch_description():
    bringup_share = FindPackageShare('arter_bringup')

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),

        DeclareLaunchArgument(
            "rviz_config_path",

            description="Path to the RViz config file"
        ),

        DeclareLaunchArgument(
            "nav2_param_path",
            description="Path to the Nav2 parameter YAML file"
        ),

        OpaqueFunction(function=launch_setup)
    ])

