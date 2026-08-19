from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock if true'
    )

    rf2o_node = Node(
        package='rf2o_laser_odometry',
        executable='rf2o_laser_odometry_node',
        name='rf2o_laser_odometry',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            # Robo real so tem o hokuyo frontal ativo (ver hokuyo.launch.py);
            # esse eh o topico onde ele (ou a bridge do Gazebo) publica.
            'laser_scan_topic' : '/laser_scan_front',
            'odom_topic' : '/odom_rf2o',
            # publish_tf=False: o EKF (ekf.launch.py) ja publica odom -> base_footprint,
            # fundindo esse /odom_rf2o com o dead-reckoning de roda (imu_odom_node).
            # Se o rf2o tambem publicasse TF, os dois brigariam pela mesma transform.
            'publish_tf' : False,
            'base_frame_id' : 'base_footprint',
            'odom_frame_id' : 'odom',
            'init_pose_from_topic' : '',
            'freq' : 20.0}],
    )

    return LaunchDescription([
        use_sim_time_arg,
        rf2o_node,
    ])
