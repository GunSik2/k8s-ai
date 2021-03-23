# JupyterHub 설치

## 설치
- 설정파일
```
$ openssl rand -hex 32
B7d0f0d62657360ad1018b0f8dc93b4bf38e33e3b13be83e0c69579467cd586f

$ cat config.yml
proxy:
  secretToken: "b7d0f0d62657360ad1018b0f8dc93b4bf38e33e3b13be83e0c69579467cd586f“
```
- 설치
```
$ helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
$ helm repo update

$ helm upgrade --install jhub jupyterhub/jupyterhub \
  --namespace jhub  \
  --version=0.9.0 \
  --values config.yml
```
- 확인
```
$ kubectl get pod --namespace jhub
NAME                              READY   STATUS              RESTARTS   AGE
continuous-image-puller-hr527     1/1     Running             0          67s
hub-5965fb6c76-jpq68              0/1     ContainerCreating   0          67s
proxy-6b58654f8f-xmnjm            1/1     Running             0          67s
user-scheduler-65f4cbb9b7-8cmpg   1/1     Running             0          67s
user-scheduler-65f4cbb9b7-f8ps8   1/1     Running             0          67s

$ kubectl get service --namespace jhub
NAME           TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
hub            ClusterIP      10.43.242.105   <none>        8081/TCP                     3m24s
proxy-api      ClusterIP      10.43.236.93    <none>        8001/TCP                     3m24s
proxy-public   LoadBalancer   10.43.171.159   <pending>     443:31674/TCP,80:31485/TCP   3m24s
```
- 삭제
```
$ helm delete jhub --purge
```

## 참고자료
- https://github.com/jupyterhub/zero-to-jupyterhub-k8s
