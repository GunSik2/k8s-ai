# MNIST 개발 사례

## 목표 환경


## 개발환경 구성
### GPU 환경 구성
#### GPU 장치 확인
```
$ sudo lshw -C display
  *-display:0 UNCLAIMED   
       description: VGA compatible controller
       product: GD 5446
       vendor: Cirrus Logic
       physical id: 2
       bus info: pci@0000:00:02.0
       version: 00
       width: 32 bits
       clock: 33MHz
       capabilities: vga_controller
       configuration: latency=0
       resources: memory:fa000000-fbffffff memory:fe050000-fe050fff memory:fe040000-fe04ffff
  *-display:1
       description: 3D controller
       product: NVIDIA Corporation
       vendor: NVIDIA Corporation
       physical id: 6
       bus info: pci@0000:00:06.0
       version: a1
       width: 64 bits
       clock: 33MHz
       capabilities: pm bus_master cap_list
       configuration: driver=nvidia latency=0
       resources: iomemory:200-1ff iomemory:300-2ff irq:11 memory:fc000000-fcffffff memory:2000000000-27ffffffff memory:3000000000-3001ffffff
```
#### GUDA / CUDnn 버전 확인
- nvidia-smi 명령은 엉뚱한 버전으로 표시될 수 있으니 주의 필요 (smi 실행 버전을 그대로 표시)
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
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Quadro RTX 6000     On   | 00000000:00:06.0 Off |                    0 |
| N/A   42C    P0    68W / 250W |  21516MiB / 22698MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  Quadro RTX 6000     On   | 00000000:00:07.0 Off |                    0 |
| N/A   40C    P0    68W / 250W |  21772MiB / 22698MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
...
```
- CUDnn 버전
```
$ cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2 
#define CUDNN_MAJOR 7 
#define CUDNN_MINOR 5 
#define CUDNN_PATCHLEVEL 1
```
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
- 배포
```
kubectl apply -f deepo.yml
```
- 배포 설정 파일 (deepo.yml) 
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: deepo-pvc
  namespace: jlab
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: longhorn

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deepo
  namespace: jlab
  labels:
    name: deepo
spec:
  replicas: 1
  selector:
    matchLabels:
      name: deepo
  template:
    metadata:
      labels:
        name: deepo
    spec:
      securityContext:
        runAsUser: 0
        fsGroup: 0
      containers:
      - name: deepo
        image: ufoym/deepo:all-jupyter-py36-cu100
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8888
        command:
        - /bin/bash
        - -c
        - |
          jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='xxxx' --notebook-dir='/root'
        volumeMounts:
        - name: deepo-data
          mountPath: /root
        resources:
          requests:
            memory: 500Mi
            cpu: 250m
          limits:
            nvidia.com/gpu: 1
      restartPolicy: Always
      volumes:
      - name: deepo-data
        persistentVolumeClaim:
          claimName: deepo-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: deepo
  namespace: jlab
  labels:
    name: deepo
spec:
  ports:
    - port: 8888
      targetPort: 8888
      protocol: TCP
      name: jupyter
    - port: 8501
      targetPort: 8501
      protocol: TCP
      name: streamlit
  selector:
    name: deepo

---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: deepo
  namespace: jlab
spec:
  rules:
  - host: deepo.jlab.14.49.xxx.xxx.xip.io
    http:
      paths:
      - backend:
          serviceName: deepo
          servicePort: 8888

---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: streamlit
  namespace: jlab
spec:
  rules:
  - host: streamlit.jlab.14.49.xxx.xxx.xip.io
    http:
      paths:
      - backend:
          serviceName: deepo
          servicePort: 8501
```
## 모델 빌드
### MNIST 모델 개발
```
#!/usr/bin/env python
# coding: utf-8

# # Setup

import matplotlib.pyplot as plt 
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# # Prepare Data

# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")


# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

plt.imshow(x_train[0])
plt.show()

# # Build Model

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)

model.summary()


# Train the model


batch_size = 128
epochs = 15
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

# Evaluate the trained model

score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Visualize model

plt.figure(figsize=(18, 6))

# 에포크별 정확도
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label="accuracy")
plt.plot(history.history["val_accuracy"], label="val_accuracy")
plt.title("accuracy")
plt.legend()

# 에포크별 손실률
plt.subplot(1,2,2)
plt.plot(history.history["loss"], label="loss")
plt.plot(history.history["val_loss"], label="val_loss")
plt.title("loss")
plt.legend()

plt.show()

# # Save model

model.save("./mnist.h5")

# # load model

model2 = keras.models.load_model("./mnist.h5")
# when error occured : AttributeError: 'str' object has no attribute 'decode'
# pip install 'h5py<3.0.0'
```

## 어플리케이션 배포
### Streamlit 어플리케이션 개발
- Streamlit 환경 설치
```
pip install streamlit 
pip install streamlit-drawable-canvas
```
- Streamlit 실행
```
streamlit run mnistapp.py
```
* 에러 발생시 조치
```
pip install --upgrade protobuf
pip install --upgrade tensorflow
pip install --upgrade keras
```

