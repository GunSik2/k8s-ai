# GPU 테스트
## CUDA 버전 확인

* nvidia-smi 명령은 엉뚱한 버전으로 표시될 수 있으니 주의 필요
```
$ cat /usr/local/cuda/version.txt
CUDA Version 10.0.130
CUDA Patch Version 10.0.130.1

$ ls -l /usr/local/| grep cuda
lrwxrwxrwx  1 root root   20 Mar 18  2020 cuda -> /usr/local/cuda-10.0
drwxr-xr-x 20 root root 4096 Mar 18  2020 cuda-10.0
drwxr-xr-x 17 root root 4096 Mar 18  2020 cuda-10.1
drwxr-xr-x 18 root root 4096 Mar 18  2020 cuda-8.0
drwxr-xr-x 19 root root 4096 Mar 18  2020 cuda-9.0
drwxr-xr-x 19 root root 4096 Mar 18  2020 cuda-9.2

$ /usr/local/cuda/bin/nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2018 NVIDIA Corporation
Built on Sat_Aug_25_21:08:01_CDT_2018
Cuda compilation tools, release 10.0, V10.0.130

$ /usr/bin/nvidia-smi 
Thu Mar 25 15:40:01 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.64       Driver Version: 440.64       CUDA Version: 10.2     |
```

## CUDnn 버전 확인
```
$ cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2
#define CUDNN_MAJOR 7
#define CUDNN_MINOR 5
#define CUDNN_PATCHLEVEL 1
```
## Tensorflow GPU 확인 
```
import keras
import tensorflow as tf

tf.debugging.set_log_device_placement(True)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Create some tensors
a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
c = tf.matmul(a, b)

print(c)

# https://www.tensorflow.org/guide/gpu
```

![image](https://user-images.githubusercontent.com/11453229/112426656-ab568500-8d7b-11eb-9067-10b64b000561.png)


## Jupyter notebook GPU 확인
```
import os

def is_available():

    """
        Check NVIDIA with nvidia-smi command
        Returning code 0 if no error, it means NVIDIA is installed
        Other codes mean not installed
    """
    code = os.system('nvidia-smi')
    return code == 0

print(is_available())
```
