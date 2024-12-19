import argparse
import config

import math
import time
import torch
import numpy as np
from collections import deque
import utils

import time
import simulation
import command
import standup
from freedogs2py_bridge import RealGo1

import control


def main(args):
    device = 'cpu'

    prop_enc_pth = 'src/models/prop_encoder_1200.pt'
    mlp_pth = 'src/models/mlp_1200.pt'
    mean_file = 'src/models/mean1200.csv'
    var_file = 'src/models/var1200.csv'

    prop_loaded_encoder = torch.jit.load(prop_enc_pth).to(device)
    loaded_mlp = torch.jit.load(mlp_pth).to(device)
    loaded_mean = np.loadtxt(mean_file, dtype=np.float32)[0]
    loaded_var = np.loadtxt(var_file, dtype=np.float32)[0]
    clip_obs = 10

    action_mean = np.array([0.05,  0.8, -1.4, -0.05,  0.8, -1.4, 0.05,  0.8, -1.4,-0.05,  0.8, -1.4], dtype=np.float32)
    Kp = 35
    Kd = 0.6
    act_history = deque([np.zeros((1, 12)) for _ in range(4)], maxlen=4)
    
    calc_latent_every_steps = 2
    control_freq_hz = 100
    cycle_duration_s = 1.0 / control_freq_hz
    print('Expected cycle duration:', math.ceil(cycle_duration_s * 1000.0), 'ms')

    if args.real:
        conn = RealGo1()
    else:
        conn = simulation.Simulation(config) 
        if args.standpos:
            conn.set_keyframe(3)
        else:
            conn.set_keyframe(0)
    
    conn.start()
    if not args.standpos:
        standup.standup(conn)
    
    obs = control.to_observation(conn.wait_latest_state(), act_history)
    obs_history = deque([obs]*50, maxlen=51)
    
    step = 0
    latent_p = None
    with torch.no_grad():
        while args.real or conn.viewer.is_running():
            start_time = time.time()

            control.push_history(obs_history, control.to_observation(conn.wait_latest_state(), act_history))
            obs = np.concatenate(
                [np.concatenate(obs_history), np.zeros(28, dtype=np.float32)]
            )
            obs = control.normalize_observation(obs, loaded_mean, loaded_var, clip_obs)
            obs_torch = torch.from_numpy(obs).cpu().reshape(1, -1)
    
            with torch.no_grad():
                if step%calc_latent_every_steps== 0:
                    latent_p = prop_loaded_encoder(obs_torch[:,:42*50])
                action_ll = loaded_mlp(
                    torch.cat([obs_torch[:,42*50:42*(50 + 1)], latent_p], 1)
                )
            # normalize action
            control.push_history(act_history, action_ll)
            action = act_history[0][0] * 0.4 + action_mean
            
            cmd = command.Command(q=action, Kp=[Kp]*12, Kd=[Kd]*12)
            # cmd.clamp_q()
            conn.send(cmd.robot_cmd())
                       
            duration = time.time() - start_time
            if duration < cycle_duration_s:
                time.sleep(cycle_duration_s - duration)
            else:
                print('too slow:', math.ceil(duration * 1000), 'ms')
            step += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--real', action='store_true')
    parser.add_argument('-s', '--standpos', action='store_true')
    main(parser.parse_args())
