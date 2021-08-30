# APK8S experimet

## JupyterLab
Data Science 시험을 위한 JupyterLab 환경을 구성한다. 
Docker 이미지를 만들고 Kubernetes에 배포하여 환경을 구성한다. 

- Image build
```
git clone https://github.com/apk8s/book-source
cd chapter-04/ds/notebook-apk8s/Dockerfile
docker build -t cgshome2/jupyterlab-apk8s .
```
- Image push
```
docker push
```
- K8S push
```
kubectl run -i -t jupyterlab_v0.1 \
  --restart=Never --rm=true \
  --env="JUPYTER_ENABLE_LAB=yes" \
  --image=cgshome2/jupyterlab-apk8s
  
kubectl port-forward jupyterlab_v0.1 8888:8888 
```

