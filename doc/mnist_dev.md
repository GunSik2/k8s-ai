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



