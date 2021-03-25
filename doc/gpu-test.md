# GPU 테스트

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
