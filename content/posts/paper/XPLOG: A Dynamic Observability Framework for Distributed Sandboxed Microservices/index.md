---
title: "[Paper] - XPLOG: A Dynamic Observability Framework for Distributed Sandboxed Microservices"
excerpt: "XPLOG: A Dynamic Observability Framework for Distributed Sandboxed Microservices"

type: docs
tags:
  - [Cloud-native, paper]

toc: true
toc_sticky: true

date: 2025-11-11
last_modified_at: 2025-11-11
---


## Abstract

`cloud-native` 환경에서 마이크로서비스들의 이벤트 순서가 보장된 로깅은 어렵다. 왜냐하면, 각 마이크로서비스들은 비동기적으로 이벤트를 트리거하기 때문이다. 애플리케이션들의 인과 관계가 보장된 로깅을 위해 `XPLOG` 프레임워크를 제안한다. `XPLOG` 프레임워크는 `eBPF` 기능을 활용하여 호스트 내의 시스템 수준 이벤트를 가로챔과 동시에, 관련 애플리케이션 및 시스템 로그를 수집하고 통합하여 전역적으로 인과 관계가 일관된 로그 스트림을 생성한다.

## Introduction

`cloud-native` 환경이 확산됨에 따라, 마이크로서비스 아키텍처가 확산되었고, 기존의 모놀리식 아키텍처에서 마이크로서비스 기반 설계로 패러다임이 변경되고 있다. 그러나 이러한 분산 패러다임은 운영상의 어려움을 야기하고, `cloud-native`한 환경에서 `monitoring`과 `observability`가 필수가 되었다. `monitoring`이 미리 정의된 메트릭, 로그 등을 추적하는 반면, `observability`는 시스템의 동작 및 시스템끼리의 상호작용을 분석하여 근본 원인을 조사하고 식별하는 데 필요한 맥락적 이해를 제공한다. 

`Sysdig`, `SysFlow`, `eAudit`과 같은 syscall 텔레메트리 프레임워크는 시스템 수준의 가시성을 제공하지만, 분산 인과 관계를 포착하고 애플리케이션 계층과 OS 계층의 컨텍스트를 연결하는 데 부족하다.

`observability` 프레임워크를 개발하기 위한 주요 요구 사항은 실행 중인 마이크로서비스와 기본 호스트 OS의 로그 메시지를 의미 있는 방식으로 수집해야 한다. 인과적 순서 또는 실행 순서를 보존해야 한다. 인과 관계가 일관된 로그 스트림은 근본 원인을 더 잘 분석할 수 있다. 

로그 스트림에 이벤트 시퀀스 기반 필터를 적용할 수 있으며, 이는 전체 로그를 파싱할 필요 없이 필요한 정보를 더 빠르게 추출할 수 있게 해준다. 또한 인과 관계가 일관된 로그 메시지는 `provenance graph`를 동적으로 생성하는 데 도움이 되며, 이는 시스템 취약점 탐지, 근본 원인 분석 등에 추가로 활용될 수 있다.

## related work
