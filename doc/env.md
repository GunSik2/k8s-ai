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
## GPU 설치 확인
```
$ lspci | grep -i nvidia
00:06.0 3D controller: NVIDIA Corporation Device 1e78 (rev a1)
00:07.0 3D controller: NVIDIA Corporation Device 1e78 (rev a1)

$ nvidia-smi -L
GPU 0: Quadro RTX 6000 (UUID: GPU-3d476e5e-07ab-7cdd-2352-69c179f6b34a)
GPU 1: Quadro RTX 6000 (UUID: GPU-5f91ef31-178c-6a8e-f0c3-2ffbbadfc0b7)

$ nvidia-smi -q -d memory
==============NVSMI LOG==============
Timestamp                           : Tue Mar 23 18:48:56 2021
Driver Version                      : 440.64
CUDA Version                        : 10.2

Attached GPUs                       : 2
GPU 00000000:00:06.0
    FB Memory Usage
        Total                       : 22698 MiB
        Used                        : 0 MiB
        Free                        : 22698 MiB
    BAR1 Memory Usage
        Total                       : 32768 MiB
        Used                        : 2 MiB
        Free                        : 32766 MiB

GPU 00000000:00:07.0
    FB Memory Usage
        Total                       : 22698 MiB
        Used                        : 0 MiB
        Free                        : 22698 MiB
    BAR1 Memory Usage
        Total                       : 32768 MiB
        Used                        : 2 MiB
        Free                        : 32766 MiB
        
$ docker run --runtime=nvidia nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04 nvidia-smi
Wed Mar 24 09:54:26 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.64       Driver Version: 440.64       CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Quadro RTX 6000     On   | 00000000:00:06.0 Off |                    0 |
| N/A   26C    P8    12W / 250W |      0MiB / 22698MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  Quadro RTX 6000     On   | 00000000:00:07.0 Off |                    0 |
| N/A   27C    P8    12W / 250W |      0MiB / 22698MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
        
```

## 참고자료
- Rancher 초기화 https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cleaning-cluster-nodes/
