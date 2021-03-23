## 설치
- 네임스프레이스 생성
```
kubectl create namespace jlab
```
- 설치 
```
kubectl apply -f pvc.yml
kubectl apply -f deployment.yml
kubectl apply -f service.yml
kubectl apply -f ingress.yml
```

## 설정파일

- pvc.yml : longhorn storageclass 사용
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jupyterlab-pvc
  namespace: jlab
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: longhorn
```


- deployment.yml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jupyterlab
  namespace: jlab
  labels:
    name: jupyterlab
spec:
  replicas: 1
  selector:
    matchLabels:
      name: jupyterlab
  template:
    metadata:
      labels:
        name: jupyterlab
    spec:
      securityContext:
        runAsUser: 0
        fsGroup: 0
      containers:
        - name: jupyterlab
          image: jupyter/datascience-notebook:latest
          imagePullPolicy: IfNotPresent
          ports:
          - containerPort: 8888
          command:
            - /bin/bash
            - -c
            - |
              chmod -R 777 /home/jovyan; 
              start.sh jupyter lab --LabApp.token='password' --LabApp.ip='0.0.0.0' --LabApp.allow_root=True
          volumeMounts:
            - name: jupyterlab-data
              mountPath: /home/jovyan
          resources:
            requests:
              memory: 500Mi
              cpu: 250m
      restartPolicy: Always
      volumes:
      - name: jupyterlab-data
        persistentVolumeClaim:
          claimName: jupyterlab-pvc
```

- service.yml
```
apiVersion: v1
kind: Service
metadata:
  name: jupyterlab
  namespace: jlab
  labels:
    name: jupyterlab
spec:
  ports:
    - port: 8888
      targetPort: 8888
      protocol: TCP
  selector:
    name: jupyterlab
```

- ingress.yml
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: jupyterlab
  namespace: jlab
spec:
  rules:
  - host: wwww.jlab.14.49.xx.xxx.xip.io
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: jupyterlab
            port:
              number: 8888
```

## 확장플러그인 설치
- nodejs
```
conda install -c conda-forge nodejs
```
- jupyterlab-git 
```
conda install -c conda-forge jupyterlab-git
jupyter labextension update --all
jupyter labextension list
```
- jupyter-lsp (code assistance)
```
conda install -c conda-forge jupyterlab_lsp
```


## 참고자료
- https://medium.com/analytics-vidhya/deploying-standalone-jupyterlab-on-kubernetes-for-early-stage-startups-7a1468fae289
- https://github.com/jupyterlab/jupyterlab-git
- https://github.com/ml-tooling/ml-workspace
- https://kubernetes.io/ko/docs/concepts/services-networking/ingress/
