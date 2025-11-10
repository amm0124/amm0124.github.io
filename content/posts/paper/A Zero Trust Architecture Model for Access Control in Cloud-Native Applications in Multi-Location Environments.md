---
title: "A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Location Environments"
excerpt: "A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Location Environments"
type: docs
tags:
  - [Cloud Native, Cloud, Docker, k8s, Kubernetes]

toc: true
toc_sticky: true

date: 2025-09-30
last_modified_at: 2025-09-30
---

헬로


> Title : A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Location Environments<br>
> Publish : Computer Security Division Information Technology Laboratory<br>
> Published: September 13, 2023



##  Abstract

- 제로트러스트의 기본 원칙 : 사용자, 서비스, 장치에 대해 네트워크 위치, 소속, 소유권만을 근거로 부여되는 암묵적인 신뢰를 제거하는 것.
- 제로트러스트의 핵심적인 패러다임 전환 : 네트워크 매개변수(Ip, Port, 경계, 서브넷 등 네트워크 정보)를 통한 분할 및 격리에서 신원 기반으로의 보안 통제 초점 변경
    - 온프레미스, 멀티클라우드 등 환경 및 위치에 관계없이 이러한 정책을 시행할 수 있는 플랫폼이 필요함. 이는 API 게이트웨이, 사이드카 프록시, SPIFFE(secure production identity framework for everyone)과 같은 애플리케이션 신원 인프라로 구성됨.

## Executive Summary

클라우드 네이티브 애플리케이션으로 인정받는 경우는 다음과 같음
- 마이크로서비스라고 하는 느슨하게 결합된 구성 요소들로 이루어짐. 각 마이크로서비스는 다른 물리적 머신 혹은 가상 머신에 호스팅될 수 있으며, 지리적으로도 분산 가능
- 애플리케이션과 관련된 모든 트랜잭션은 네트워크를 통한 하나 이상의 서비스 간 마이크로서비스 호출을 포함할 수 있음
- 모든 애플리케이션 서비스의 통합세트를 제공하는 서비스 메시 소프트웨어 플랫폼의 존재

위와 같은 클라우드 네이티브 애플리케이션에 대한 제로트러스트 아키텍처의 구현에는 강력한 정책 프레임워크가 필요함. 제로트러스트 원칙을 따르는 프레임워크의 구성 정책은 다음을 고려해야 함
- 네트워크 위치, 소속, 소유권을 기준으로 사용자, 서비스 또는 장치에 대한 암묵적인 신뢰가 있어선 안 됨. 네트워크 매개변수를 사용한 네트워크 분할 또는 격리에 기반한 정책 정의 및 관련 보안 제어는 불충분함. 이러한 정책은 네트워크 계층 정책으로 분류됨. (일부)
- 전체 애플리케이션에 걸쳐 제로트러스트 원칙이 존재하도록 보장하기 위해, 네트워크 계층 정책은 온프레미스든 여러 클라우드든 서비스 또는 애플리케이션의 위치와 관계없이 다양한 참여 엔티티(사용자 및 서비스)의 신원에 대한 신뢰를 확립하는 정책으로 보안되어야 함.

클라우드 네이티브 애플리케이션에 대해 세밀한 애플리케이션 수준 정책을 시행할 수 있는 제로 트러스트 아키텍처를 구현하기 위한 지침을 제공.
- 네트워크 계층 및 신원 계층 정책의 조합
- 엣지, 인그레스, 사이드카 및 이그레스 게이트웨이와 같은 정책의 정의 및 배포를 가능하게 하는 클라우드 네이티브 애플리케이션의 구성 요소; 서비스 신원의 생성, 발급 및 유지 관리; 멀티클라우드 및 하이브리드 환경을 포괄하는 기업 애플리케이션 인프라에서 사용자 신원을 전달하는 인증 및 권한 부여 토큰의 발급


## 1. Introduction

클라우드로 인한 지리적으로 분산된 애플리케이션, 네트워크 내부에서의 접근 및 외부에서의 접근으로 인한 안전한 통신과 접근 정책의 검증을 통해 모든 데이터소스와 컴퓨팅 서비스에 대한 신뢰 구축 필요
지리적 분산 외에도, 클라우드 네이티브 애플리케이션의 특징은 느슨한 결합을 통한 광범위한 서비스 간 호출을 통해 비즈니스 프로세스를 종합적으로 지원하는 수많은 마이크로서비스의 존재
이들은 서비스 메시라고 불리는 모든 애플리케이션 서비스를 제공하기 위한 통합 인프라로 보강됨.

마이크로서비스 형태의 다양한 애플리케이션 구성 요소뿐만 아니라, 직접 호출이나 클라이언트를 통해 접근하는 사용자의 신원 개념 강조
이는 신원 인증, 사용자, 서비스 및 요청된 리소스의 현재 상태를 고려하는 동적 정책을 통해 세션별로 합법적인 접근을 제공해야 함

위 요구사항들은 포괄적인 정책 프레임워크를 통해 충족 가능. 클라우드 네이티브 애플리케이션을 위한 제로트러스트 원칙 통합 및 제로트러스트 아키텍처 구현하기 위한 정책 프레임워크 개발 지침 제공.
네트워크, 네트워크 장치, 사용자 및 서비스를 포함하여 애플리케이션 스택의 모든 중요한 엔티티와 리소스에 걸친 포괄적인 정책 집합으로 구성되어야 함.

### 1.1 Background

- zero trust (zt) : `정적인 네트워크 기반 경계`에서 벗어나 사용자와 리소스에 초점을 맞추도록 방어를 전환하는 패러다임. 이는 보안 기본 요소의 집합. 단지 물리적 또는 네트워크 위치에 근거하여 암묵적인 신뢰를 부여하지 않으며, 소유권에 근거하여 엔드포인트(장치)에 신뢰를 부여하지 않음 가정. 네트워크 위치가 리소스 보안의 구성 요소로 간주되지 않으므로, 네트워크 세그먼트가 아닌 리소스(장치, 서비스, 워크플로우, 네트워크 계정) 보호에 중점을 둠
- zero trust architecture (zta) : zt 원칙을 사용하여 인프라 및 워크플로우를 구축. 

### 1.2 Relationship to Other NIST Guidance Documents

- 온프레미스 및 다중 클라우드(여러 위치)에서 호스팅되는 클라우드 네이티브 애플리케이션을 위한 zta 구현 지침 제공
- 서비스 메시를 사용하는 마이크로서비스 기반 애플리케이션 아키텍처에 대한 배경 정보와 특정 보안 서비스를 구성하기 위한 지침 제공

SP 800-204A : 서비스 메시 아키텍처를 사용한 안전한 마이크로서비스 기반 애플리케이션 구축

SP 800-204B : 서비스 메시를 사용하는 마이크로서비스 기반 애플리케이션을 위한 속성 기반 접근 제어는 보안 요구 사항을 충족하는 서비스 메시 내 인증 및 권한 부여 프레임워크 구축에 대한 배포 지침 제공.
모든 서비스 쌍 간의 통신에서 상호 인증 활성화하여 zt 구축, 광범위한 정책을 표현하는 데 사용할 수 있고, 사용자 기반, 객체 및 배포 환경 측면에서 확장 가능한 접근 제어 모델에 기반한 강력한 접근 제어 메커니즘 구축 포함


### 1.3 Scope

- 서비스 메시 인프라를 포함하는 마이크로서비스 기반 애플리케이션 플랫폼에서 세분화된 접근 제어를 위한 ZTA를 구현하기 위한 요구 사항 식별.
- ZT 원칙을 구성하고 구현하기 위해 플랫폼의 일부가 되어야 하는 인프라 요소 식별.
- 위 플랫폼에 ZTA를 배포하기 위한 지침 및 해당 배포가 제공할 수 있는 보안 보증의 개요 설명.
- ZT 원칙을 시행하기 위해 네트워크 수준(세분화된 정책과 전체적인 정책 모두)과 ID 계층 정책을 결합한 다중 계층 정책 권장.

### 1.4. Target Audience

ㅇㅇ

### 1.5. Organization of This Document



## 2. The Enterprise Cloud-Native Platform and its Components

기업 클라우드 네이티브 -> 마이크로서비스 + service mesh를 통한 네트워크 연결, 네트워크 resilience, 관찰성, 보안
- next generation access control (NGAC)
- Attributed-based access control (ABAC)

현대 엔터프라이즈는 온프레미스 데이터센터 + 멀티 클라우드 서비스 로케이션
플랫폼을 구성하고 있는 단일 클러스터를 관리하기 위해 서비스메시 인스턴스 배포 가정 -> 많은 온프레미스 사이트와 다양한 가용영역에 퍼져 있는 여러 클러스터 관리를 위해 서비스 메시 인스턴스가 여러 개가 됨

각 메시 인스턴스(클러스터 별 하나의 메시 인스턴스)는 두 개의 구성 요소로 나뉨

1) control plane : API(다양한 설정을 정의하고 있음), 정책(다양한 마이크서비스 클러스터 사이의 정책)으로 구현됨
2) data plane : 정책을 수행하는 런타임

그러나, 마이크로서비스, 서비스 위치, 메시 인스턴스에 관계없이 모든 마이크로서비스 또는 서비스 쌍 간의 접근 관리를 위한 통일된 정책 세트가 필요함. 이를 위해 기업에서 운영되는 전체 서비스 집합에 적용 가능한 통일된 정책을 정의하고, 이를 개별 서비스 메시 인스턴스의 제어 플레인들에 배포할 수 있는 글로벌 제어 플레인이 필요함.

단일 메시를 통해 전체 클러스터 관리가 가능하지만, 이는 단일 장애 지점을 만들어서 가용성을 저하시킬 뿐 아니라, 모든 워크로드가 하나의 제어 플레인과 통신해야 하는 네트워크 복잡성, 특히 정부 시스템과 같은 격리된 환경에서는 불가능함.


### 2.1 Enterprise Infrastructure Layer

글로벌 제어 플레인 내에 여러 관리 플레인이 호스팅됨. 글로벌 제어 플레인은 클러스터 수준이 아닌 기업 수준에서 (전체적으로) 개별 제어 플레인 기능 수행하는 데 활용. 또한 특정 제어 플레인 하에 모든 클러스터 노드가 침해된 경우 제어 플레인 종료하는 데에도 가능. 관리 플레인은 하위 계층의 도구 사용과 관련된 조직 프로세스를 인코딩하여 기업 수준 시스템이 작동할 수 있도록 하는 인터페이스를 제공함. 기업 전체 모든 서비스에 대해 일관되고 통일된 정책의 정의 및 배포를 가능하게 한다.
서비스 메시 인스턴스와 연관된 로컬 제어 플레인과 각각의 데이터 플레인의 일부를 형성하는 다양한 유형의 프록시 세트로 구성됨. 프록시는 PEP로 작동하며 3가지 유형으로 구분

- 인그레스 프록시 : 클러스터 외부에서 시작되는 클라이언트 애플리케이션으로부터 클러스터 내 모든 서비스로 들어오는 사용자 또는 서비스 요청에 대한 정책 시행
- 사이드카 프록시 : 클러스터 내부 서비스 간의 정책 시행
- 이그레스 프록시 : 클러스터 내 모든 서비스에서 클러스터 외부의 외부 애플리케이션으로 발생하는 요청에 대한 정책 시행

{{< figure caption="[Figure 1]" src="/images/posts/paper/A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Location Environments/Fig1.png" >}}

## 3. Designing a Policy Framework for ZTA for Cloud-Native Application Environments

Fig1에서 제공된 제로 트러스트 원칙 세트와 일부 초안 ZTA를 기반으로, 엔터프라이즈 클라우드 네이티브 애플리케이션 환경(즉, 서비스 메시로 관리되는 각 클러스터의 다양한 마이크로서비스 세트와 글로벌 제어 플레인 및 관리 플레인으로 구성된 기업 수준 인프라로 보강됨)을 위한 ZTA를 실현하기 위해 다음과 같은 핵심 가정들이 수립되었다:

- 네트워크 경계는 항상 침해될 수 있기 때문에 신뢰는 더 이상 네트워크 경계를 기반으로 할 수 없다.
- 정책은 공격자가 이미 기업 네트워크 내부에 있다는 가정 하에 정의되어야 한다.
- 모든 접근 결정은 최소 권한, 요청별, 컨텍스트 기반 원칙과 사용자, 서비스 및 디바이스와 연관된 신원에 의존해야 한다. 이는 애플리케이션에 대한 런타임 격리의 한 형태로 이어지며, 본 문서에서는 이를 "신원 기반 세그먼테이션"이라고 지칭한다.
- API가 클라우드 네이티브 애플리케이션에서 중요한 역할을 하므로, 적절한 버전 관리(하위 호환성 제공), 적절한 입력 검증 기술(SQL 인젝션 및 크로스 사이트 스크립팅과 같은 공격 방지), 출력 인코딩이 적절한 문서화(예: 사용 지침)와 같은 일반 요구사항 외에도 정책 프레임워크의 일부가 되어야 한다.

위의 핵심 가정들은 다음과 같은 ZTA 설계 요구사항을 제공한다:

- 단일 컴포넌트나 기능만으로는 ZTA를 구현하기에 충분하지 않다. 오히려 인프라의 모든 애플리케이션에 걸쳐 제로 트러스트 원칙을 집단적으로 시행해야 한다.
- ZTA 컴포넌트 기능은 상호 관계 및 워크플로를 포함하여 명확하게 명시되어야 한다.
- 보안 제어를 구현하는 시행 인프라(주로 PEP로 구성)는 보안 커널의 속성을 만족해야 한다: 항상 호출됨(우회 불가), 검증 가능, 애플리케이션 코드로부터 독립적.
- 런타임 시 ZTA의 핵심 원칙 또는 주요 기능은 시행 인프라를 활용하는 애플리케이션의 신원 기반 세그먼테이션을 구현하는 것이다.

### 3.1. Requirements for Identity-Based Segmentation Policies for ZTA


### 3.2. Limitations of Identity-Based Segmentation Policies for Enterprise ZTA


### 3.3. Multi-Tier Policies for Enterprise ZTA


## 4. Implementing Multi-Tier Policies for ZTA for Cloud-Native Application Environments


### 4.1. Reference Application Infrastructure Scenario


### 4.2. Role of the Service Mesh in Policy Deployment, Enforcement, and Updates 


### 4.3. Policy Deployment for Reference Application Infrastructure


### 4.4. Another Application Infrastructure Scenario


### 4.5. Functional Roles of Application Infrastructure Elements in Enforcing Policies


### 4.6. Comparison of Identity-Tier and Network-Tier Policies


#### 4.6.1. Approaches for Deployment and the Limitations of Network-Tier Policies


#### 4.6.2. Prerequisites for the Deployment of Identity-Tier Policies


#### 4.6.3. Advantages of Identity-Tier Policies


## 5. Support for Multi-tier Policies Through a Monitoring Framework


## 6. Summary and Conclusions


