from ssrl_ros_go1.controller import Controller, yaw_from_quat
import time


class DummyListener:
    def stop(self):
        print('Stop dummy listener')


class AutoController(Controller):

    def __init__(self, cfg, data_path):
        super().__init__(cfg, data_path)

    def start_keyboard_listener(self):
        self.listener = DummyListener()

        while self.qped_state != 'off':
            time.sleep(0.1)
        
        self.standing_up_count = 0
        self.qped_state = "standing_up"
        self.publish_quadruped_state()

        while self.qped_state != 'stand':
            time.sleep(0.1)
        
        self.step_count = 0
        if self.is_straight_task:
            self.start_yaw = yaw_from_quat(self.obs[self.env._quat_idxs])
        # Don't count steps when the obs hist is still filling up
        self.max_rollout_steps += self.obs_history_length + 1
        self.open_bag()
        self.qped_state = "walk"
        self.publish_quadruped_state()

        while self.qped_state != 'off':
            time.sleep(0.1)
        
        self.shutdown_flag = True
        print('Done!')
