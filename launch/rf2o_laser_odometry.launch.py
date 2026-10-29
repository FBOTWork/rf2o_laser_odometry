from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock if true'
    )

    use_two_lidars_arg = DeclareLaunchArgument(
        'use_two_lidars',
        default_value='true',
        description='Also run rf2o on the rear lidar if true'
    )

    rf2o_node = Node(
        package='rf2o_laser_odometry',
        executable='rf2o_laser_odometry_node',
        name='rf2o_laser_odometry',
        output='screen',
        ros_arguments=['--log-level', 'rf2o_laser_odometry:=ERROR'],
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'laser_scan_topic' : '/laser_scan_front',
            'odom_topic' : '/odom_rf2o',
            'publish_tf' : False,
            'base_frame_id' : 'base_footprint',
            'odom_frame_id' : 'odom',
            'init_pose_from_topic' : '',
            'freq' : 20.0}],
    )

    rf2o_rear_node = Node(
        package='rf2o_laser_odometry',
        executable='rf2o_laser_odometry_node',
        name='rf2o_laser_odometry_rear',
        output='screen',
        ros_arguments=['--log-level', 'rf2o_laser_odometry_rear:=ERROR'],
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'laser_scan_topic' : '/laser_scan_rear',
            'odom_topic' : '/odom_rf2o_rear',
            'publish_tf' : False,
            'base_frame_id' : 'base_footprint',
            'odom_frame_id' : 'odom',
            'init_pose_from_topic' : '',
            'freq' : 20.0}],
        condition=IfCondition(LaunchConfiguration('use_two_lidars')),
    )

    return LaunchDescription([
        use_sim_time_arg,
        use_two_lidars_arg,
        rf2o_node,
        rf2o_rear_node,
    ])
