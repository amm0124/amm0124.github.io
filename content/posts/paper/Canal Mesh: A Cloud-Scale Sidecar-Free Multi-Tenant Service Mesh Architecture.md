---
title: "Canal Mesh: A Cloud-Scale Sidecar-Free Multi-Tenant Service
Mesh Architecture"
excerpt: "ACM Computing Surveys"

type: docs

categories:
  - 논문리뷰
tags:
  - [Cloud Native, Cloud, Docker, k8s, Kubernetes]

toc: true
toc_sticky: true

date: 2025-09-17
last_modified_at: 2025-09-17
---


# Abstract

서비스메시 프레임워크는 sidecar를 통해 pod 사이의 트래픽을 처리했지만, 이는 많은 문제를 유발한다. 모든 트래픽이 sidecar를 통하기 때문에, 유저의 pod로 침입, 리소스 초과, 많은 사이드카를 관리하기 위한 오버헤드, 성능 감소등의 문제를 발생시킴.

이 문제의 해결책으로 cloud scale의 sidecar에서 자유로운 멀티테넌트 서비스메시 아키텍처인 Canal Mesh를 소개. Canal은 유저 클러스터와 service mesh function을 분리하고, public 클라우드에 이러한 기능을 다루기 위해 중앙화된 메시게이트를 배포한다. 따라서 유저 침입이나 오케스트레이션 오버헤드를 줄임. 서비스 통합 및 멀티테넌시를 통해 서비스메시의 인프라 가격 또한 감소됨. 

클라우드 기반의 deployment 때문에 일어나는 서비스 가용성, 테닌트 격리, 시끄러운 이웃, 서비스 유연성, 추가 요금 등의 떠오르는 문제를 해결하기 위해 계층적 실패 복구, 셔플 샤딩, 빠른 개입, 정밀한 스케일링, 클라우드 인프라 재사용, 리소스 집계 등의 기술을 사용한다. 평가에 따르면 Canal Mesh의 성능, 리소스 소비량, 컨트롤 플레인 오버헤드는 Istio와 Ambient보다 뛰어남을 입증

# Introduction

서비스메시는 네트워크 상의 서비스간의 통신을 가능하게 해주는 인프라 구조로 나타남. 메이저 클라우드 제공업체들은 service mesh를 쉽게 빌드하고, 마이크로서비스 기반의 애플리케이션을 매니징하는 서비스메시 기반의 상품을 출시함. Istio, Linkerd와 같은 많은 서비스메시 프레임워크의 컴포넌트의 주요 요소들은 sidecar라고 불리는 proxy임. 이러한 sidecar는 pod의 네트워크 트래픽을 관리하며, 정책 기반 라우팅, 백분율 기반 트래픽 분할, 속도 제한 등의 작업을 처리함. 네트워크 기능을 사이드카로 분리하면 유연한하게 트래픽을 관리할 수 있다. 4년동안 Alibaba 클라우드에 Istio을 배포한 후, 우리의 production data가 pod당 하나의 사이드가 배포가 아래 문제를 보여줌.

- 침입 : 유저 pod 안에 사이드카를 두고, 사용자 앱과 함께 실행된다. 이처럼 사이드카가 사용자 파드 내에 존재한다는 것은 잠재적인 보안 및 안정성 문제를 야기할 수 있다. 예를 들어 사이드카에서 메모리 누수가 발생하면 동일한 파드 내의 사용자 앱이 중단될 수 있다.
- Throughput and latency : 사이드카를 사용하면 네트워크 쓰루풋은 3x~7x까지 감소되고, latency는 3x~7x까지 증가함. 왜냐하면 각 리퀘스트들은 sidecar로 리다이렉트 되어야 함. 추가 단계를 생성하고 이게 주된 오버헤드임.
- Resource occupation (자원 점유) : 복잡한 네트워크 및 보안 구성이 적용될 경우, 사이드카는 상당한 양의 CPU와 메모리를 사용하는데, 이는 원래 사용자가 앱을 사용할 때 쓰는 자원임. 게다가, 유저 서비스의 최적의 상태를 유지하려면 사이드카의 CPU 사용량이 45% 미만이 되도록 관리해야 함.
- Orchestration : 각 pod마다 하나의 사이드카가 있고, 하나의 클라우드 서비스는 수십만개의 pod를 가질 수 있으므로, 이 모든 사이드카의 구성을 조정하는 데 따르는 오버헤드는 매우 크다.

이러한 문제를 해결하기 위해 cilium과 spright는 eBPF를 사용함 -> 패킷 프로세싱 레이턴시, CPU 소모량을 줄이기 위해. 이러한 이점에도 불구하고 eBPF 기반의 솔루션은 프로그래밍적으로 제한이 있음. -> HTTP 프로토콜과 같은 L7 레이어들의 프로세싱을 유연하게 처리하는데.. (이는 eBPF는 커널에서 작동하기 때문에 L7까지 안 감 + eBPF 프로그래밍은 제한적) 

소비자들 조사에 따르면 대략 80~95퍼센트의 서비스메시 유저들이 L7 기능을 필요로 함. 따라서 cilium과 spright는 고객 수요를 만족 못 함. 

ambient는 이러한 문제 해결의 선구자임. ambient는 복잡한 L7 기능은 사이드카에서 분리하여 선택적 프록시로 이전하고, L4 기능 처리를 위해 노드별 공유 프록시를 배포함. 또한, Cilium도 Envoy [26]를 포함하여 L7 처리를 지원할 수 있습니다 [12]. 

그러나 단일 테넌트(single-tenant)용 오픈소스 솔루션으로서, Envoy를 사용하는 Ambient와 Cilium은 모두 L4/L7 프록시가 여전히 사용자 클러스터 내에 존재하므로 침범(intrusion) 및 자원 문제를 미해결 상태로 남겨둡니다.


사용자 클러스터로부터 사이드카가 완전히 분리되지 않아 발생하는 위 문제들을 해결하기 위해, 저희는 침범은 최소화하고 성능과 비용 효율성은 높이며 오케스트레이션 오버헤드는 적은, 클라우드 기반의 사이드카 없는(sidecar-free) 멀티테넌트 서비스 메시인 Canal Mesh를 제안합니다. Canal은 서비스 메시를 사용자 클러스터 밖으로 완전히 빼내고, 퍼블릭 클라우드에 중앙화된 메시 게이트웨이를 도입하여 이러한 기능들을 원격으로 처리하는 적극적인 분리 전략을 채택합니다.

게이트웨이에서 서비스 통합과 멀티테넌시를 통해 서비스 메시 사용 비용을 크게 절감할 수 있습니다. 서비스 메시를 사용자 클러스터로부터 분리함으로써, 새로운 기능을 개발하거나 성능을 최적화할 때 K8s[31]와 같은 오픈소스 소프트웨어가 가하는 제약에서 벗어날 수 있습니다. 추가적으로, 클라우드 제공업체는 기존 클라우드 인프라를 더 효율적으로 재사용하고, 멀티테넌트 클라우드 관리 분야에서 수년간 쌓아온 경험을 활용할 수 있습니다.

논문에서 cilium을 single tenant라고 소개함 -> 이유는? 이는 클러스터에 설치하기 때문에

즉, 다른 클러스터에 설치하는 멀티테넌트 시스템을 논문에서 제안함



------------



# Abstract and Introduction

Istio, Linkerd와 같은 sidecar 기반의 service mesh를 사용하면 유저 어플리케이션과 네트워크 트래픽 관리 부분 (정책 기반 라우팅, 퍼센트 기반의 트래픽 분리, 속도 제한 등)을 분리할 수 있어 편하지만, sidecar 기반의 service mesh는 다음과 같은 문제점이 있음.

- Intrusion : 유저 어플리케이션 pod에 sidecar 컨테이너가 함께 배치 -> 보안 문제 및 장애 유발 가능
- throughput and latency : 네트워크 경로 증가로 인한 throughput 감소 및 latency 증가
- resource occupation : sidecar에 할당된 CPU 사용량이 임계점을 넘으면 효율성이 저하
- orchestration : pod 수에 비례한 sidecar의 수 -> 관리 및 orchestration 오버헤드 증가

위 Sidecar의 문제를 해결하기 위해 Cilium과 SPRIGHT은 eBPF를 통해 packet processing latency와 CPU 소모량을 줄였으나, eBPF 기반의 해결책은 HTTP와 같은 L7 layer processing을 처리하기 힘든 문제가 존재한다. 

이러한 sidecar의 문제를 해결하기 위해 K8s service mesh의 구현체 Istio에서 Sidecarless인 Ambient mesh (Istio의 sidecarless mode - Ambient)를 활성화할 수 있음. 이는 pod에 붙어있는 sidecar를 과감하게 버리고, L4 proxy와 L7 proxy를