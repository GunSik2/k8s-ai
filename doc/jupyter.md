# Jupyter 설치

- 수동 배포 
```
$ kubectl create namespace jupyter

$ cat jupyter.yaml
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
      dnsPolicy: ClusterFirst
      restartPolicy: Always

$ kubectl create -f jupyter.yaml

$ kubectl get pods --namespace jupyter

$ pod_name=$(kubectl get pods --namespace jupyter --no-headers | awk '{print $1}’) 

$ kubectl logs --namespace jupyter ${pod_name}
[I 02:34:28.976 NotebookApp] The Jupyter Notebook is running at:
[I 02:34:28.976 NotebookApp] http://(jupyter-7dcd5cb48b-w452g or 127.0.0.1):8888/?token=5fe2b2ee958214e421ecf3e5871d2612cb39f199fa489214
[I 02:34:28.976 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).


$ kubectl port-forward --namespace jupyter $pod_name 8888:8888
```

## [Helm Jupyter 설치](https://github.com/gradiant/charts)
```
$ helm repo add gradiant https://gradiant.github.io/charts/
$ helm install --name jupyter gradiant/jupyter
$ helm del --purge jupyter
```

