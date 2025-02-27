# Before start on host
```bash
git submodule update --init --recursive
```

# Build docker
Inside dir ```rl_go1/docker``` run
```bash
docker build -t rma-conda -f RMA_Dockerfile
```

# Start Docker
Inside dir: ```rl_go1```

```bash
xhost si:localuser:root
docker run --rm -it --ipc=host --gpus all --net=host -v .:/workspace --volume=$HOME/.Xauthority:/root/.Xauthority:rw -e NVIDIA_DRIVER_CAPABILITIES=all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged rma-conda bash
```

# After docker started init env
```bash
source /rma_entry.sh
cd /workspace
```

## Применение политик на роботе

Запуск политики в симуляторе mujoco  
```python3 ./src/policy.py```

Запуск в симуляторе mujoco, с пропуском стадии поднятия робота:  
```python3 ./src/policy.py -s```

Запуск на реальном роботе:  
```python3 ./src/policy.py -r```

## Управление роботом
Управление клавишами:  
* a - назад
* s - стоп
* d - вперед

Запуск политики в симуляторе mujoco  
```python3 ./src/control.py```

Запуск в симуляторе mujoco, с пропуском стадии поднятия робота:  
```python3 ./src/control.py -s```

Запуск на реальном роботе:  
```python3 ./src/control.py -r```


## Программа поднятия робота на ноги
Если хотим запускать в симуляторе, то изменяем в standup.py real = False, если на реальном роботе, то real = True

Запускаем код поднятия робота:
```python3 ./src/standup.py```
