# Tensorflow + Jupyter + GPU

- Image: tensorflow/tensorflow:latest-gpu-py3-jupyter
- Deployment
```
$ kubectl create namespace jupyter
```
- Deployment yaml
```
$ cat jupyter-gpu.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: jupyter-gpu
  name: jupyter-gpu
  namespace: jupyter
spec:
  replicas: 1
  selector:
    matchLabels:
      run: jupyter-gpu
  template:
    metadata:
      labels:
        run: jupyter-gpu
    spec:
      containers: 
      - image: tensorflow/tensorflow:latest-gpu-py3-jupyter
        name: jupyter-gpu
        resources: 
          limits: 
            nvidia.com/gpu: 1 
        ports:
        - containerPort: 8888
          name: jupyter
        - containerPort: 6006
          name: tensorboard
```
- Deployment
```
$ kubectl create -f jupyter-gpu.yaml
$ kubectl get pods --namespace jupyter
NAME                          READY   STATUS    RESTARTS   AGE
jupyter-7dcd5cb48b-w452g      1/1     Running   1          25h
jupyter-gpu-797845649-72h5n   1/1     Running   0          3m7s
```

- Jupyter 접속 토큰 확인
```
$ kubectl logs jupyter-gpu-797845649-72h5n --namespace jupyter
[C 04:05:25.460 NotebookApp]     
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://jupyter-gpu-797845649-72h5n:8888/?token=c6cdb2331a32d451a493d66de70bc56999f249e55f33f269
     or http://127.0.0.1:8888/?token=c6cdb2331a32d451a493d66de70bc56999f249e55f33f269
```
- Ingress 추가 후 접속 : 80 => jupyter-gpu:8888
- Jupyter 접속 후 GPU 확인 
```
from tensorflow.python.client import device_lib

def get_available_devices():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos]

print(get_available_devices())
```

- tf examples
  - https://github.com/tensorflow/docs/tree/master/site/en/tutorials
