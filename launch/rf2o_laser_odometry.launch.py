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

    # Diagonal (x, y, z, roll, pitch, yaw); z/roll/pitch are not estimated
    pose_covariance_diagonal = [0.01, 0.01, 1e3, 1e3, 1e3, 0.01]
    twist_covariance_diagonal = [0.0025, 0.0025, 1e3, 1e3, 1e3, 0.005]

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
            'freq' : 20.0,
            'pose_covariance_diagonal' : pose_covariance_diagonal,
            'twist_covariance_diagonal' : twist_covariance_diagonal}],
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
            'freq' : 20.0,
            'pose_covariance_diagonal' : pose_covariance_diagonal,
            'twist_covariance_diagonal' : twist_covariance_diagonal}],
        condition=IfCondition(LaunchConfiguration('use_two_lidars')),
    )

    return LaunchDescription([
        use_sim_time_arg,
        use_two_lidars_arg,
        rf2o_node,
        rf2o_rear_node,
    ])
