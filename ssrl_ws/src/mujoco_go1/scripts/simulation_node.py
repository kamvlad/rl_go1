#!/usr/bin/env python3
from threading import Thread, Lock

from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import PoseStamped

from unitree_legged_msgs.msg import LowState
from unitree_legged_msgs.msg import LowCmd

from ssrl_ros_go1_msgs.msg import Reset

import mujoco
import mujoco.viewer
import rospy
import time



def viewer_loop(viewer):
    fps = 25
    rendering_rate = rospy.Rate(fps)
    while viewer.is_running():
        viewer.sync()
        rendering_rate.sleep()


if __name__ == '__main__':
    rospy.init_node('mujoco_go1')
    
    
    control_dt_sec = 0.001
    simmulation_steps_per_control = 2
    simulation_dt_sec = control_dt_sec / simmulation_steps_per_control

    ROBOT = "go1" # Robot name, "go2", "b2", "b2w", "h1", "go2w", "g1" 
    ROBOT_SCENE = "/workspace/submodules/unitree_mujoco/unitree_robots/" + ROBOT + "/scene.xml" # Robot scene

    mj_model = mujoco.MjModel.from_xml_path(ROBOT_SCENE)
    mj_model.opt.timestep = simulation_dt_sec
    mj_data = mujoco.MjData(mj_model)
    mujoco.mj_resetDataKeyframe(mj_model, mj_data, 0)
    
    viewer = mujoco.viewer.launch_passive(mj_model, mj_data)
    viewer_thread = Thread(target=viewer_loop, args=(viewer, ), name='viewer_py')
    viewer_thread.start()    
    
    num_motor = mj_model.nu
    
    lowCmd = None
    def low_cmd_callback(lowCmdSrc):
        global lowCmd
        lowCmd = lowCmdSrc

    state_pub = rospy.Publisher('low_state', LowState, queue_size=10)
    cmd_sub = rospy.Subscriber('low_cmd', LowCmd, low_cmd_callback, tcp_nodelay=True)

    vicon_pose_pub = rospy.Publisher('vrpn_client_node/quad/pose',
                                     PoseStamped,
                                     queue_size=10)
    vicon_vel_pub = rospy.Publisher('vrpn_client_node/quad/twist',
                                    TwistStamped,
                                    queue_size=10)

    def reset_callback(msg):
        mujoco.mj_resetDataKeyframe(mj_model, mj_data, 0)

    reset_sub = rospy.Subscriber('reset', Reset, reset_callback, tcp_nodelay=True)

    control_rate = rospy.Rate(1 / control_dt_sec)
    try:
        while not rospy.is_shutdown() and viewer.is_running():
            start = time.perf_counter()

            with viewer.lock():
                for _ in range(simmulation_steps_per_control):
                    if lowCmd is not None:
                        for i in range(num_motor):
                            mj_data.ctrl[i] = (
                                lowCmd.motorCmd[i].tau +
                                lowCmd.motorCmd[i].Kp * (lowCmd.motorCmd[i].q - mj_data.sensordata[i]) +
                                lowCmd.motorCmd[i].Kd * (lowCmd.motorCmd[i].dq - mj_data.sensordata[i + num_motor])
                            )

                    mujoco.mj_step(mj_model, mj_data)

            num_motor = 12
            dim_motor_sensor = 3 * num_motor
            state = LowState()

            for i in range(num_motor):
                state.motorState[i].q = mj_data.sensordata[i]
                state.motorState[i].dq = mj_data.sensordata[
                    i + num_motor
                ]
                state.motorState[i].tauEst = mj_data.sensordata[
                    i + 2 * num_motor
                ]

            state.imu.quaternion[0] = mj_data.sensordata[
                dim_motor_sensor + 0
            ]
            state.imu.quaternion[1] = mj_data.sensordata[
                dim_motor_sensor + 1
            ]
            state.imu.quaternion[2] = mj_data.sensordata[
                dim_motor_sensor + 2
            ]
            state.imu.quaternion[3] = mj_data.sensordata[
                dim_motor_sensor + 3
            ]

            state.imu.gyroscope[0] = mj_data.sensordata[
                dim_motor_sensor + 4
            ]
            state.imu.gyroscope[1] = mj_data.sensordata[
                dim_motor_sensor + 5
            ]
            state.imu.gyroscope[2] = mj_data.sensordata[
                dim_motor_sensor + 6
            ]

            state.imu.accelerometer[0] = mj_data.sensordata[
                dim_motor_sensor + 7
            ]
            state.imu.accelerometer[1] = mj_data.sensordata[
                dim_motor_sensor + 8
            ]
            state.imu.accelerometer[2] = mj_data.sensordata[
                dim_motor_sensor + 9
            ]
            state_pub.publish(state)

            pose = PoseStamped()
            pose.pose.position.x = mj_data.qpos[0]
            pose.pose.position.y = mj_data.qpos[1]
            pose.pose.position.z = mj_data.qpos[2]
            pose.pose.orientation.w = mj_data.qpos[3]
            pose.pose.orientation.x = mj_data.qpos[4]
            pose.pose.orientation.y = mj_data.qpos[5]
            pose.pose.orientation.z = mj_data.qpos[6]

            vicon_pose_pub.publish(pose)

            twist = TwistStamped()
            
            twist.twist.linear.x = mj_data.cvel[1][3]
            twist.twist.linear.y = mj_data.cvel[1][4]
            twist.twist.linear.z = mj_data.cvel[1][5]

            vicon_vel_pub.publish(twist)


            # if control_rate.remaining().secs < 0:
            #     print((time.perf_counter() - start) * 1000)
            #     rospy.logwarn("simulation too slow. try reduce simulation_steps_per_control")
            control_rate.sleep()
    except KeyboardInterrupt:
        pass
    
    viewer.close()
    viewer_thread.join()
