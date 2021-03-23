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
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: jupyterlab
  namespace: jlab
spec:
  rules:
  - host: wwww.jlab.14.49.44.246.xip.io
    http:
      paths:
      - backend:
          serviceName: ingress-b856e11330a007bcd8ac62182921af68
          servicePort: 8888
```

## 참고자료
- https://medium.com/analytics-vidhya/deploying-standalone-jupyterlab-on-kubernetes-for-early-stage-startups-7a1468fae289
