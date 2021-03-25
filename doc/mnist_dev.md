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

## 어플리케이션 배포
### Streamlit 어플리케이션 개발



