#!/usr/bin/env python

from launch import LaunchDescription
from launch_ros.descriptions import ComposableNode
from launch_ros.actions import ComposableNodeContainer
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Declare launch arguments
    fqdn_arg = DeclareLaunchArgument(
        'fqdn',
        default_value='192.168.26.26',
        description='FQDN or IP address of the Qb2 device'
    )
    
    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='Root',
        description='Frame ID for the point cloud'
    )
    
    point_cloud_topic_arg = DeclareLaunchArgument(
        'point_cloud_topic',
        default_value='/bf/points_raw',
        description='Topic name for publishing point cloud'
    )

    container = ComposableNodeContainer(
        name="blickfeld_qb2_component",
        namespace="",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[
            ComposableNode(
                package="blickfeld_qb2_ros2_driver",
                plugin="blickfeld::ros_interop::Qb2Driver",
                name="blickfeld_qb2_driver",
                parameters=[
                    {
                        "fqdn": LaunchConfiguration('fqdn'),
                        "frame_id": LaunchConfiguration('frame_id'),
                        "point_cloud_topic": LaunchConfiguration('point_cloud_topic'),
                        "use_measurement_timestamp": False,
                        "publish_intensity": True,
                        "publish_point_id": True,
                    }
                ],
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
        ],
        output="screen",
    )
    
    return LaunchDescription([
        fqdn_arg,
        frame_id_arg,
        point_cloud_topic_arg,
        container
    ])
