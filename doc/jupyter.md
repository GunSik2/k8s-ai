# Jupyter 설치

## 수동 배포 설치
- 네임스페이스 생성
```
$ kubectl create namespace jupyter
```
- 설치
```
$ kubectl apply -f jupyter.yml
$ kubectl logs -f jupyter-5d6487c957-hd4ch -n jupyter

[I 02:34:28.976 NotebookApp] The Jupyter Notebook is running at:
[I 02:34:28.976 NotebookApp] http://(jupyter-7dcd5cb48b-w452g or \
                             127.0.0.1):8888/?token=5fe2b2ee958214e421ecf3e5871d2612cb39f199fa489214
[I 02:34:28.976 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```
- jupyter.yml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: jupyter
  name: jupyter
  namespace: jupyter
spec:
  replicas: 1
  selector:
    matchLabels:
      run: jupyter
  template:
    metadata:
      labels:
        run: jupyter
    spec:
      containers: 
      - image: jupyter/scipy-notebook:abdb27a6dfbb
        name: jupyter

---
apiVersion: v1
kind: Service
metadata:
  name: jupyter
  namespace: jupyter
  labels:
    run: jupyter
spec:
  ports:
    - port: 8888
      targetPort: 8888
      protocol: TCP
  selector:
    run: jupyter

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: jupyter3
  namespace: jupyter
spec:
  rules:
  - host: jupyter3.jupyter.14.49.44.246.xip.io
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: jupyter
            port:
              number: 8888
```

## [Helm Jupyter 설치](https://github.com/gradiant/charts)
```
$ helm repo add gradiant https://gradiant.github.io/charts/
$ helm install --name jupyter gradiant/jupyter
$ helm del --purge jupyter
```

## 참고
- https://kubernetes.io/ko/docs/concepts/services-networking/connect-applications-service/
