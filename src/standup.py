import time
from freedogs2py_bridge import RealGo1
import simulation

import config
import positions
import utils


def standup(conn, viewer = None):
    phase = 0
    phase_cycles = 0

    stand_command = positions.stand_command_2()
    while viewer is None or viewer.is_running():
        state = conn.wait_latest_state()
        
        if phase == 0:
            if phase_cycles >= 100:
                phase = 1
                phase_cycles = 0
        elif phase == 1:
            if phase_cycles >= 100:
                phase = 2
                phase_cycles = 0
                init_q = utils.q_vec(state)
            conn.send(positions.laydown_command().robot_cmd())
        elif phase == 2:
            q_step = utils.interpolate(init_q, stand_command.q, phase_cycles, 500)
            cmd = stand_command.copy(q = q_step)
            conn.send(cmd.robot_cmd())
            if phase_cycles == 500:
                return state, cmd        

        phase_cycles += 1
        time.sleep(0.01)
    return state

def main():
    config.ENABLE_SIMULATION = True

    real = False
    conn = None

    if not real:
        conn = simulation.Simulation(config)
        conn.set_keyframe(0)
        conn.start()
        viewer = conn.viewer
    else:
        conn = RealGo1()
        conn.start()
        viewer = None

    time.sleep(0.2)

    _, cmd = standup(conn, viewer)
    while viewer is None or viewer.is_running():
        conn.send(cmd.robot_cmd())
        time.sleep(0.01)


if __name__ == '__main__':
    main()