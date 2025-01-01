from brax.training.agents.ssrl import train as ssrl
from brax.robots.go1 import networks as go1_networks
from brax.evaluate import evaluate
from omegaconf import OmegaConf


def main():
    cfg = OmegaConf.load('submodules/ssrl/ssrl/scripts/configs/go1.yaml')
    
    (sac_network_factory, model_network_factory) = go1_networks.ssrl_network_factories(cfg)
        


if __name__ == '__main__':
    main()