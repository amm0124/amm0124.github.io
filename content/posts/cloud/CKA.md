---
title: "[CKA] - K8s Architecture"
excerpt: "CKA"

type: docs

categories:
  - K8s
tags:
  - [Cloud Native, Cloud, K8s]

toc: true
toc_sticky: true

date: 2025-09-29
last_modified_at: 2025-09-29
---


# K8s Architecture

- Worker Node
- Master Node
- etcd
- Kube-scheduler
- Controller-manager : Node-Controller, Replication-Controller

- kube-api server 
  - 쿠버네티스의 기본 관리 구성 요소, 모든 작업에 대한 오케스트레이터
  - 구성 : controller manager, kube-scheduler, etcd

- 컨테이너 런타임 엔진 
  - Docker, containerd
- kubelet : 각 노드에 설치되는 agent
- worker node 사이 통신 : kube-proxy를 통해 연결

# 정리

- Master Node : etcd, Controller-Manager, kube-scheduler, kube-apiserver
- Worker Node : kubelet, kube-proxy, container runtime (docker, containerd..)


# Docker and containerd

둘 다 컨테이너 하이레벨 런타임

- CRI (Container Rumtime Interface) : K8s와 컨테이너 런타임 사이의 인터페이스
- OCI (Open Container Initiative) : 이미지 사양 및 런타임 사양
  - 런타임 : 컨테이너 개발에 대한 표준화 spec

Docker는 CRI spec 만족 x -> Docker shim 도입을 통해 Docker 사용
Docker는 이미지빌드에 도움이 되는 빌드 도구인 Docker CLI, Docker API runc, runc daemon 등의 도구로 구성

## containerd

docker 없이 containerd 사용하는 방법에 대해
containerd 기본 CLI : ctr -> 불편함 (사용자 친화 x)
nerdctl
crictl: 컨테이너 디버깅을 위한 CLI
 containerd -> crictl을 통해 CRI - K8s

kubelet : 노드에서 특정 수의 컨테이너 또는 Pod 있는지 확인


## etcd

저장하는 목록
- nodes
- pods
- configs
- secrets
- accounts
- roles
- bindings
- others

kubectl 명령어를 사용할 때 가져오는 정보들은 모두 etcd에서 가져 옴
etcd 옵션에서 다수는 인증서와 관련
kubeadam 사용하는 경우에 kube-suystem 네임스페이스에 etcd master pod가 존재함

조회

```bash
kubectl get pods -n kube-system
```

etcd 내부 모든 key

```
kubectl exec etcd-master -n kube-system etcdctl get / --prefix -keys-only
```

고가용성 -> 여러 마스터 노드를 사용하는데 각 마스터 노드마다 etcd 인스턴스가 분산됨
이 때, etcd.service에 
--initial-cluster 옵션으로 여러 Etcd의 주소를 넣음으로 고가용성을 위한 분산 클러스터 구성 가능

```bash

$ etcd.service

ExecStart = ....
--initial-clster controller-0=https://${IP}:2380, controller-1=https://${IP}:2380 \\
...

```

RAFT protocol

# kube apiserver
쿠버네티스의 기본 관리 컴포넌트
kubectl을 통해 kube apiserver에 요청
인증 필요
스케줄러는 API 서버를 지속적으로 모니터링하여 노드가 할당되지 않은 새로운 pod 인식 -> 노드 선택 
다시 kube-apiserver에 전달 후 정보를 etcd에 저장
선택된 worker node의 kubelet에 전달 -> application 배포

```kube apiserver는 etcd 데이터 저장소와 직접 상호 작용하는 유일한 구성 요소```
kube api server의 옵션에서 k8s 구성 요소들의 인증서 설정 가능, etcd 서버 설정 가능

```bash
kube-apiserver.service
```
kube-admin 사용하는 경우 master node의 kube-system 네임스페이스에 kube-apiserver를 pod로 배포


## kube controller manager

쿠버네티스의 다양한 컨트롤러를 관리. 지속적으로 구성 요소를 모니터링하고, 문제가 생기면 해결을 하는 역할 -> 원하는 상태로 유지
- Node Controller : kube-apiserver를 통해 워커 노드들의 상태 확인. 5초 polling, 40초의 grace period (40초동안 대기 후, health check fail -> 문제 생김 판단 -> 5분 타임아웃 후, 문제 생기면 다른 노드에 pod를 프로비저닝)
- Deployment, namespace, endpoint, pv-protection, replication, pv-binder, service-account, node, job controller 등 존재
- cronjob, Stateful-set, replicaset 등도 controller manager에 관리

kube-conroller-manager 단일 프로세스에서 여러 controller 관리함

컨트롤러에 문제가 있다면 -> kube-controller-manager.service를 확인
kube-controller-manager또한 pod로 kube-system namespace 사용

```bash
kubectl get pods -n kube-system
```

```bash
cat /etc/kubernetes/manifests/kube-controller-manager.yaml
```
읉 통해 확인 가능

## kube scheduler

어느 노드에 어떤 pod를 배치할지 결정함. 실제로 Node에 pod를 배치하지 않음. kubelet이 생성함.
각 pod를 살펴보고 이에 가장 적합한 node를 찾으려 함. 

과정

1. pod의 프로필에 맞지 않는 노드 필터링 (CPU 소모량 등 컴퓨팅 자원을 기준으로 맞지 않는 node 필터링)
2. node에 순위 배정


resource requirements and limits, taints and tolerations, node selectors/affinitiy
(리소스 요구 사항 및 한계, 오염 및 허용 오차, 노드 선택자/친화성)


## kubelet

node에 배치되는 Agent <-> 마스터 노드와의 통신
- register node
- create pods
- monitor node and pods

## kube-proxy

## k8s 네트워킹 컨셉 

pod는 pod끼리 통신 가능. 클러스터에 pod 네트워킹 솔루션 배포를 통한 수행.
pod 네트워크를 통해 통신 가능. 다른 Pod의 IP가 동일하게 유지된다는 보장 x -> `K8s Service`
Kube-proxy를 통한 문제 해결. 새로운 service가 생성될 때마다 각 노드에 적절한 규칙을 생성하여 해당 서비스로의 트래픽 전송. iptables 규칙 사용 (forwarding)


## Pods

pod를 통해 컨테이너를 캡슐화
1 pod당 1 컨테이너 권장. 그러나 sidecar와 같은 helper 컨테이너 패턴을 통해 여러 개도 가능.
동일 pod 내의 컨테이너는 localhost 통신 및 볼륨 공유, 생명 주기 공유

## Pods - YAML
|kind|Version|

| Kind       | Version  |
|------------|----------|
| Pod        | v1       |
| Service    | v1       |
| ReplicaSet | apps/v1  |
| Deployment | apps/v1  |


```pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name : myapp-pod
  labels : # 넣고 싶은 만큼 넣으면 됨
    app : myapp
    type : front-end
spec: 
  containers: # List
    - name: nginx-container
      image: nginx 
```

pod 생성

```bash
kubectl create -f nod-definition.yam
```

```bash
kubectl apply -f nod-definition.yaml
```

pod 상태

```bash
kubectl get pods
```
이름은 <pod name>

```bash
kubectl describe pod myapp-pod
```

하나의 pod 내 두 개의 컨테이너 생성 yaml

```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: my-pod1
  labels:
    app: my-pod
    type: frontend
spec:
  containers:
    - name: my-nginx-container
      image: nginx
    - name: my-busybox-container 
      image: busybox:latest
```


## ReplicaSet Controller

높은 고가용성을 위해 ReplicaSet 사용. 100개 복제품 선언하면 100개 보장.
ReplicaSet Controller는 하나의 노드에 적용되는 것이 아닌 여러 노드에 대해 적용


ReplicaController 대신 ReplicaSet 사용 권장 (controller : 구 버전)


```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: myapp-rc
  labels:
    app: myapp
    type: front-end
spec:
  template: # 추가 요소
    containers:
      - name: rc-container
        image: nginx:latest
  replicas: 3
```

Replica Controller 상태 보는 방법

```bash
kubectl get replicationcontroller
```



## ReplicaSet


```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-rc
  labels:
    app: myapp
    type: front-end
spec:
  template: # 추가 요소
    containers:
      - name: rc-container
        image: nginx:latest
  replicas: 3
  selector: 
    matchLabels:
      type: front-end
```

labes and selectors

replicaset(모니터링 프로세스)의 역할은 복제품들을 모니터링하고, 만약 문제가 생긴다면 새롭게 배포하는 역할. 파드에 붙인 label을 통해 감시.

## Deployment

rolling 배포 등 가능 + replicaset

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-frontend
  labels:
    apps: my-frontend-deployment
spec:
  selector:
    matchLabels:
      apps: my-httpd
  replicas: 3
  template:
    metadata:
      labels:
        apps: my-httpd
    spec:
      containers:
        - name: httpd-frontend-container
          image: httpd:2.4-alpine
```

쿠버네티스 전체 오브젝트 보는 CLI

```bash
kubectl get all
``` 


# Service

application 내부 <-> 외부 사이 통신 제어.

- ClusterIP : 클러스터 내부 가상 IP 트래픽 라우팅
- NodePort : 노드의 Port로 들어오는 트래픽을 라우팅. 유효 범위 30000~32767
- LoadBalencer : 
- DNS

## NodePort

nodeport yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  label: myapp-nodeport
spec: # type and port
  type: NodePort
  ports: # 30008번 포트로 들어오는 트래픽을 NodePort:80 -> Target IP:80으로 전달
    - targetPort: 80
      port: 80
      nodePort: 30008
  selector:
    app: myapp # pod의 label과 동일
    type: front-end # pod의 label과 동일
```

서비스 생성되면 selector과 일치하는 pod를 찾고 연결. SessionAffinity : Yes가 기본 옵션

Pod가 여러 노드에 분산되어 있을 때는 어떻게? -> 클러스터의 모든 노드의 포트에 할당함
예시

노드 1의 pod-> 192.168.1.2:30008
노드 2의 pod -> 192.168.1.3:30008
노드 3의 pod -> 192.168.1.4:30008

service 조회하는 방법

```bash
kubectl get services
```

## ClusterIP

```yaml
apiVersion: v1
kind: Service
metadata:
  name: back-end
spec: 
  type: ClusterIP
  ports:
    - targetPort: 80
      port: 80
  selector:
    app: myapp
    type: back-end
```


## Load Balancer

yaml template

```yaml
apiVersion: v1
type: service
metadata:
  name: myapp-service
spec:
  type: LoadBalancer
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008
```

# NameSpace

사용할 수 있는 리소스 객체를 구분
default namepsace : k8s가 관리
네트워킹 솔루션, DNS 서비스 등에 필요한 것을 default로 생성


kube-system, kube-public 또한 자동생성
- default : 
- kube-system : 
- kube-public : 공용 네임스페이스

db-service.dev.svc.cluster.local 도메인에서

db-service: service name
dev: namespace
svc: service
cluster.local: domain

```bash
kubectl get pods
```

명령은 기본 네임스페이스에 있는 모든 파드 나열. 만약 네임스페이스 지정하고 싶으면

```bash
kubectl get pods --namespace=kube-system
or
kubectl get pods -n=kube-system
```

네임스페이스 지정을 통한 리소스 생성. 혹은 yaml에 추가 가능 (metadata)

```bash
kubectl create -f pod-definition.yml --namespace=dev
or
kubectl apply -f pod-definition.yaml --namepsace=dev
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  namepsace: dev
  labels:
    app: myapp
    type: back-end
spec:
  containers:
    - name: backend-container
      image: nginx:latest
      port: 80
```


네임스페이스 자체를 생성
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

namespace 생성하기

```bash
kubectl create -f namespace-dev.yaml
or
kubectl create namespace dev
```
영구적으로 namespace 전환하기

```bash
kubectl config set-context $(kubectl config current-context) --namespace=dev
```
context는 관리 시스템에서 여러 클러스터와 환경 관리하는 데 사용


전체 namespace의 pod 보기

```bash
kubectl get pods -all-namespaces
or
kubectl get pods -A
```

namespace의 리소스 사용량 제한하기 -> quota 생성

```quota yaml```
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```

적용

```bash
kubectl create -f compute-quota.yaml
```

---

모든 네임스페이스 조회

```bash
kubectl get ns
```

빠르게 pod 생성

```bash
kubectl run redis --image=redis --namespace=finance
```

네임스페이스의 service 조회

```bash
kubectl get svc -n=<namespace>
```

같은 네임스페이스 안에 있으면 service 이름으로 접근 가능 (host name - full dns 안 해도 됨)
다른 네임스페이스 안에 있으면 full dns 해야 함




