# Jupyter-GPU 설치

## 수동 배포 설치
- 네임스페이스 생성
```
$ kubectl create namespace jupyter
```
- 설치
```
$ kubectl apply -f jupyter-gpu.yml
$ kubectl logs -f jupyter-5d6487c957-hd4ch -n jupyter-gpu

[I 02:34:28.976 NotebookApp] The Jupyter Notebook is running at:
[I 02:34:28.976 NotebookApp] http://(jupyter-7dcd5cb48b-w452g or \
                             127.0.0.1):8888/?token=5fe2b2ee958214e421ecf3e5871d2612cb39f199fa489214
[I 02:34:28.976 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```
- jupyter-gpu.yml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: jupytergpu
  name: jupytergpu
  namespace: jupyter
spec:
  replicas: 1
  selector:
    matchLabels:
      run: jupytergpu
  template:
    metadata:
      labels:
        run: jupytergpu
    spec:
      containers: 
      - image: kopkop/jupyter-scipy-notebook-gpu
        name: jupytergpu

---

apiVersion: v1
kind: Service
metadata:
  name: jupytergpu
  namespace: jupyter
  labels:
    run: jupytergpu
spec:
  ports:
    - port: 8888
      targetPort: 8888
      protocol: TCP
  selector:
    run: jupytergpu

---

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: jupytergpu
  namespace: jupyter
spec:
  rules:
  - host: jupytergpu.jupyter.14.49.44.246.xip.io
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: jupytergpu
            port: 
              number: 8888
```


## 참고
- https://hub.docker.com/r/kopkop/jupyter-scipy-notebook-gpu/
