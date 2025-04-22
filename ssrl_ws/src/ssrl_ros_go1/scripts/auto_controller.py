#!/usr/bin/env python
from pathlib import Path
import rospy
from omegaconf import DictConfig
from hydra.core.global_hydra import GlobalHydra
from hydra import compose, initialize
from ssrl_ros_go1_msgs.msg import Reset
from ssrl_ros_go1.auto_controller import AutoController


def main(cfg: DictConfig):
    try:
        data_path = Path(__file__).parent.parent / 'data'
        node = AutoController(cfg, data_path)
        node.run()
        
    except rospy.ROSInterruptException:
        print("ROSInterruptException")
        pass


if __name__ == '__main__':
    GlobalHydra.instance().clear()
    initialize(config_path="configs")
    cfg = compose("go1.yaml")
    main(cfg)
