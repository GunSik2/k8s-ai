# MNIST 개발 사례

## 목표 환경


## 개발환경 구성
### GPU 환경 구성

#### GUDA / CUDnn 버전 확인
#### GPU Docker 환경 구성
#### Docker GPU 시험
- Docker 이미지 환경이 GPU 사용 가능한지 확인
```
$ docker run --runtime=nvidia -it -p 8881:8888 --ipc=host ufoym/deepo:all-jupyter-py36-cu100 bash
# vi tf.py

import tensorflow as tf

tf.debugging.set_log_device_placement(True)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Create some tensors
a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
c = tf.matmul(a, b)

print(c)

# python tf.py  2>/dev/null
Num GPUs Available:  2
tf.Tensor(
[[22. 28.]
 [49. 64.]], shape=(2, 2), dtype=float32)
```
#### Kubernetes 환경 구성

## 모델 빌드
### MNIST 모델 개발

## 어플리케이션 배포
### Streamlit 어플리케이션 개발



