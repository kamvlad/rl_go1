# rl_go1

После клонирования репозитория устанавливаем следующие зависимости, если не установлены:
```
sudo snap install plotjuggler
pip install cbor2 mujoco
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```
Далее подгружаем сабмодули:
```
git submodule update --init --recursive
pip install -e submodules/free-dog-sdk/
```

## Применение политик на роботе

Запуск политики в симуляторе mujoco  
```python3 ./src/policy.py```

Запуск в симуляторе mujoco, с пропуском стадии поднятия робота:  
```python3 ./src/policy.py -s```

Запуск на реальном роботе:  
```python3 ./src/policy.py -r```

## Программа поднятия робота на ноги
Если хотим запускать в симуляторе, то изменяем в standup.py real = False, если на реальном роботе, то real = True

Запускаем код поднятия робота:
```
python3 ./src/standup.py
```


## Возможные ошибки
Если выдает ошибку, то попробуйте следующую команду и повторите предыдущую команду:
```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```

Проблемы с MESA для симмуляции [link](https://stackoverflow.com/questions/72110384/libgl-error-mesa-loader-failed-to-open-iris):
```
cd /home/$USER/miniconda/lib
mkdir backup  # Create a new folder to keep the original libstdc++
mv libstd* backup  # Put all libstdc++ files into the folder, including soft links
cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6  ./ # Copy the c++ dynamic link library of the system here
ln -s libstdc++.so.6 libstdc++.so
ln -s libstdc++.so.6 libstdc++.so.6.0.19
```
