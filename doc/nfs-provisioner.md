# NFS CSI Driver 

## Driver 설치
```
$ curl -skSL https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/install-driver.sh | bash -s master --
$ kubectl -n kube-system get pod -o wide -l app=csi-nfs-controller
NAME                                       READY   STATUS    RESTARTS   AGE     IP             NODE
csi-nfs-controller-56bfddd689-dh5tk       4/4     Running   0          35s     10.240.0.19    k8s-agentpool-22533604-0
csi-nfs-controller-56bfddd689-8pgr4       4/4     Running   0          35s     10.240.0.35    k8s-agentpool-22533604-1
$ kubectl -n kube-system get pod -o wide -l app=csi-nfs-node
NAME                                       READY   STATUS    RESTARTS   AGE     IP             NODE
csi-nfs-node-cvgbs                        3/3     Running   0          35s     10.240.0.35    k8s-agentpool-22533604-1
csi-nfs-node-dr4s4                        3/3     Running   0          35s     10.240.0.4     k8s-agentpool-22533604-0
```

## NFS Server 설치
```
$ wget https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/example/nfs-provisioner/nfs-server.yaml
$ vi nfs-server.yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: nfs-server
  template:
    spec:
      volumes:
            path: /home/nfs-data  # /nfs-vol
$ sudo mkdir -p /home/nfs-data
$ kubectl create -f nfs-server.yaml
```

## Storage Classs 설치
```
$ kubectl create -f https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/example/storageclass-nfs.yaml

$ cat storageclass-nfs.yaml
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-csi
provisioner: nfs.csi.k8s.io
parameters:
  server: nfs-server.default.svc.cluster.local    # NFS Server endpoint
  share: /                                        # NFS share path  
reclaimPolicy: Retain  # only retain is supported
volumeBindingMode: Immediate
mountOptions:
  - hard
  - nfsvers=4.1
```

## Driver 테스트
```
$ wget https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/example/nfs-provisioner/nginx-pod.yaml
$ cat nginx-pod.yaml
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvc-nginx
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  #volumeName: pv-nginx         # 제거    
  storageClassName: "nfs-csi"   # 변경 
  
$ kubectl create -f nginx-pod.yaml
$ kubectl exec nginx-nfs-example -- bash -c "findmnt /var/www -o TARGET,SOURCE,FSTYPE"
TARGET   SOURCE                                 FSTYPE
/var/www nfs-server.default.svc.cluster.local:/ nfs4
```

## 삭제
```
curl -skSL https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/uninstall-driver.sh | bash -s master --
kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/example/nfs-provisioner/nfs-server.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/deploy/example/nfs-provisioner/nginx-pod.yaml
```

## PVC 강제 삭제
```
kubectl  delete pvc redis-data-gitlab-redis-master-0 --grace-period=0 --force
kubectl  patch pvc gitlab-prometheus-server -p '{"metadata":{"finalizers":null}}'
kubectl  delete pvc gitlab-prometheus-server --grace-period=0 --force
```

## 참고자료
- https://github.com/kubernetes-csi/csi-driver-nfs/tree/master/deploy/example
- https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/docs/install-csi-driver.md
- https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/deploy/example/nfs-provisioner/README.md
- https://woohhan.tistory.com/18
