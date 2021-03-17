# 시험 환경 구성 Record

## Rancher 초기화
```
docker rm -f $(docker ps -qa)
docker rmi -f $(docker images -q)
docker volume rm $(docker volume ls -q)
```
```
for mount in $(mount | grep tmpfs | grep '/var/lib/kubelet' | awk '{ print $3 }') /var/lib/kubelet /var/lib/rancher; do umount $mount; done
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
- rancher install
```
docker run -d --restart=unless-stopped -p 8443:443 rancher/rancher
```
- 웹브라우저 Rancher UI 접속 후 비밀번호 초기화
- Rancher UI > Add Cluster > From Existing Nodes
- k8s 설치
```
sudo docker run -d --privileged --restart=unless-stopped --net=host -v /etc/kubernetes:/etc/kubernetes -v /var/run:/var/run rancher/rancher-agent:v2.4.5
--server https://xxx.xxx.xxx.xxx:8443 --token 5v8fgsqd4 --ca-checksum 65a051410 --etcd --controlplane --worker
```


## 참고자료
- Rancher 초기화 https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cleaning-cluster-nodes/