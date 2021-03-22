# 시험 환경 구성 Record

## Rancher 초기화
```
docker rm -f $(docker ps -qa)
docker rmi -f $(docker images -q)
docker volume rm $(docker volume ls -q)
```
```
for mount in $(mount | grep tmpfs | grep '/var/lib/kubelet' | \
awk '{ print $3 }') /var/lib/kubelet /var/lib/rancher; do umount $mount; done
```
```
ip link delete  flannel.1
```
```
iptables -L -t nat
iptables -L -t mangle
iptables -L
reboot
```
## Rancher
- docker install
```
$ docker -v
Docker version 18.09.7, build 2d0083d
```
- rancher install : v2.5+ 이상부터 Single Node 배포 시 DID 사용을 위해 [priviledged 모드 실행 필요](https://rancher.com/docs/rancher/v2.x/en/installation/other-installation-methods/single-node-docker/#privileged-access-for-rancher-v2-5)
```
docker run -d --restart=unless-stopped --privileged  -p 8443:443 rancher/rancher
```
- 웹브라우저 Rancher UI 접속 후 비밀번호 초기화
- Rancher UI > Add Cluster > From Existing Nodes
- k8s 설치
```
sudo docker run -d --privileged --restart=unless-stopped --net=host \
-v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.4.5
--server https://xxx.xxx.xxx.xxx:8443 --token 5v8fgsqd4 --ca-checksum 65a051410 \
--etcd --controlplane --worker
```

## Longhorn 설치
- Default > App > Launch App > Longhorn
- Longhorn UI >  Setting > General > Default Replica Count (1)
- Longhorn 백업 환경 구성  : Default > App > Launch App > nfs-provisioner

## Haproxy 설치
```
# apt install -y haproxy
# cat /etc/haproxy/haproxy.conf
listen tcp8888
        bind *:9080
        log global
        mode tcp
        option tcplog
        server tcpserver localhost:80
# systemctl restart haproxy
```
## kubectl
```
$ curl -LO "https://storage.googleapis.com/kubernetes-release/release/$( \
    curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
$ chmod a+x kubectl && sudo mv kubectl  /usr/bin/
$ vi .kube/config // config 복사하고 넣기
```

## [helm 설치](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub/setup-helm.html)
```
// Helm Installation
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

// Helm Initialization
kubectl --namespace kube-system create serviceaccount tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller --upgrade  // 또 다른 클라이언트에서 heml 초기화: helm init --client-only

helm version
```

## [k8s Nvidia GPU](https://rancher.com/blog/2020/introduction-to-machine-learning-pipeline)
```
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list \
  | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
$ sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
$ sudo apt-get install nvidia-container-runtime

$ cat /etc/docker/daemon.json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}

$ kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.6.0/nvidia-device-plugin.yml 

$ kubectl get nodes -o yaml | grep -i nvidia.com/gpu
            f:nvidia.com/gpu: {}
            f:nvidia.com/gpu: {}
      nvidia.com/gpu: "2"
      nvidia.com/gpu: "2"
```
## [Jupyter 설치](https://github.com/gradiant/charts)
```
$ helm repo add gradiant https://gradiant.github.io/charts/
$ helm install --name jupyter gradiant/jupyter
$ helm del --purge jupyter
```

## 참고자료
- Rancher 초기화 https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cleaning-cluster-nodes/
