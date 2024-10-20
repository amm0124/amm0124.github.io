---
title: "[CS/Network Security] 네트워크보안 - Data Collection(3)"
tags:
    - CS
    - Network Security
    - Data Collection
    - Network
    - Security
    - SNMP
date: 2024-10-17 13:30:00 +
thumbnail: "https://github.com/user-attachments/assets/c9107ed4-ad2e-4d67-be25-cf41b5e37df8"
categories : Network Security
description: Network Security - SNMP의 취약점에 대해 알아보자.
---

## 서론

`SNMP(Simple Network Management Protocol)`는 중앙화 네트워크 관리 프로토콜이다. 이는 편리하지만, 많은 취약점을 노출시킨다. 이를 통해 악성 유저는 `Scan`을 할 수 있다. 이에 대해서 알아보자.

## SNMP (Simple Network Management Protocol)

`TCP/IP suite` 기반의 `Application Layer`에서 작동하는 프로토콜이다. 
`IP 네트워크`를 구성하는 기기들의 정보를 모으는데 사용되는데, 이를 통해 간단하게 네트워크를 관리할 수 있다.
이를 사용하면, 네트워크 장치에서 발생할 수 있는 문제를 예방 및 감지할 수 있을 뿐 아니라, 수정할 수도 있다.
또한, 거의 대부분의 네트워크 장비 제조업체에서 지원하는 프로토콜이기에, 호환성이 좋다. 따라서 전 세계에서 널리 사용된다.
또한, UDP를 사용하여 packet을 전달하기에 빠르고 효율적이다. (오버헤드가 별로 없다.)

## TCP/IP suite

`TCP/IP suite`인데 왜 `TCP`가 아닌 `UDP`를 사용하여 전송하는지 궁금할 수 있다.
이 궁금증을 해결하기 위해 `TCP/IP suite`에 알아야 할 필요가 있다.
결론부터 말하자면, `TCP/IP suite`에서 꼭 TCP만 사용되는 것은 아니다. 
`IP(Internet Protocol)`에서 `TCP`를 사용해서 많이 통신하기 때문에, 이름을 저렇게 했을 뿐이다. 다시 말해서, `IP`가 주체이다.  
`TCP/IP suite`는 다양한 프로토콜로 구성된 프로토콜의 집합이다. (이름이 헷갈릴 수 있지만, `IP base`의 프로토콜 집합이다.)
기본 베이스는 `IP`이고, 그 위에서 작동하는 전송 계층은 `TCP와 UDP` 중 선택이 될 수 있다는 뜻이다.
따라서, 자주 상태가 변하는 네트워크 환경에서 SNMP는 좀 더 효율적인 `UDP` 전송 방식을 선택하였다. 

## SMNP configurations

`SNMP`의 주체는 `management system(manager)`과 `agent`로 나뉜다. 

## SNMP - agent

agent는 `MIB`와 `SMI`로 구성되어 있다.

`agent`는 네트워크를 구성하는 장비들(`MIB - Management Information Base`라고 한다)로 구성되어 있다. 
`agent`는 자신의 로컬 환경에 대해 정보를 관리하고 수집하는 역할을 한다. 
자신의 로컬 환경에 대해 수집한 정보를 `management system`에게 제공한다. 
`SNMP`는 `agent`가 수집한 정보를 `management system`에게 전송하는 `protocol`이다.

### MIB - Management Information Base

`manager`가 관리하고 질의할 수 있는 객체들의 집합이다. `manager`가 이 객체를 쿼리(질의)하거나 설정할 수 있는 데이터베이스 역할을 한다.

### SMI - Structure of Management Information 

`SNMP`는 범용적인 프로토콜이다. 이를 사용해서 정보를 전송하기 위해, `MIB` (객체)들을 표준에 맞도록 생성하고, 관리하는 기준을 `SMI`라고 한다. 
네트워크는 `protocol` 기반의, 즉 `약속`을 기반으로 작동하기에, `SMI`가 필요하다.


### SNMP - management system(manager)

`agent`가 SNMP를 통해 전달한 정보를 관리하는 객체를 `management system`이라고 한다. 하나 이상의 네트워크 관리 시스템을 작동시키는 컴퓨터이다.
`agent`에게 질의를 하고, 응답을 받을 수 있다. 이를 통해, 네트워크 장치를 모니터링하고 관리할 수 있다.


## Understanding SNMP 

`agent`와 `management system`의 SNMP 버전은 동일해야 한다. 그렇지 않으면, `management system`은 `agent`가 보내는 데이터를 잘못 해석할 수 있기 때문이다.
또한, 인증 방법으로 `Community 문자열`을 사용한다. 이 부분에서 `네트워크 취약점`이 생긴다.

## SNMP Community String

이는 `management system`이 `agent`로 정보 요청을 할 때, 사용되는 비밀번호 문자열이다.
현재 SNMP는 버전 3까지 출시가 되었는데, `SNMPv3` 이 전 버전에서는 대부분 Community String의 기본값으로 `public, private`등의 간단한 평문 문자열을 사용하였다.(암호화 x)
바로 이 점에서 `네트워크 취약점`이 생긴다. 비밀번호로 간단한 문자열이 사용되었기에, 악성 공격자들은 agent에게 공격을 쉽게 할 수 있었다.

`agent가 받는 Read-Only request` 즉, `REST API의 GET 요청`의 비밀번호가 기본 값으로 public으로 설정이 되어 있었다는 것이다.
또한 `POST, PUT 요청`은 private로 설정이 되어 있었다. 널리 알려진 문자열이기에, `네트워크 취약점`이 발생하였다.

즉, agent의 기기의 상탯값을 쉽게 얻고, 조작할 수 있었다는 의미다. 따라서, SNMP를 사용한다면 제일 최신 버전의 암호화를 지원하는 `SNMPv3`을 사용하거나, 
그렇지 않으면 `Community String`을 `brute force`공격에 대응할 수 있도록 복잡하게 설정해야 한다.

바로 이러한 이유에서, `SNMP`를 사용 안 해도 되는 상황이라면 사용하지 말라고 권장하는 이유다.

## SNMP PDU 

`SNMP`는 `PDU(Protocol Data Unit - 프로토콜 데이터 단위)`를 사용하여 통신의 목적을 정의한다. 아래는 `PDU type`이다.

- 0: Get request: 관리 시스템이 에이전트로부터 특정 데이터를 요청하는 메시지.
- 1: Get next request: 관리 시스템이 에이전트로부터 다음 데이터를 요청하는 메시지.
- 2: Set request: 관리 시스템이 에이전트에게 특정 데이터를 설정하거나 변경하라고 요청하는 메시지.
- 3: Get response: 에이전트가 관리 시스템의 요청에 대한 응답을 보내는 메시지.
- 4: Trap: 에이전트가 특정 이벤트가 발생했을 때 관리 시스템에게 비동기적으로 보내는 알림 메시지.

Trap은 Os에서 `interrupt handler`가 없는 `interrupt trap`과 유사하다. 
즉, 문제가 발생했을 때, OS에 문제를 위임하는 trap과 유사하다. 이러한 trap에도 `Community String`이 필요하다.
agent에서 문제가 생기면, management system에게 문제가 생겼다고 알린다. 이 때 UDP 162번 포트를 사용한다. 
다른 요청은 161번 포트를 사용하는 것과 달리, 네트워크에서 문제가 생긴다는 것은 중요한 상황이기에, management system은 162번 포트를 사용한다.
management system은 162번 포트로 들어온 메시지를 수집하고 관리한다. 
아래를 보면 Trap은 일방적으로 agent가 management system에게 보내는 것임을 알 수 있다.

![image](https://github.com/user-attachments/assets/47ac1deb-fafc-4d84-bdc9-bf00d6f2a450)


## SNMP 취약점 실습

리눅스 환경을 기반으로 먼저 SNMP을 설치하자. 따로 설정이 없으면, community string은 default value(public, private)로 설정이 된다.

    (sudo) apt-get install snmp

이후, SNMP이 실행되고 있는지, 즉 161번 포트가 실행되고 있는지 `scan`을 해야 한다.

    nmap -sU -p 161 192.168.0.1

161/udp open|filltered snmp 응답을 받았으면, 이제 community string을 알아내야 한다. 이를 알아내기 위해 일단 `무차별 공격(brute-force)`를 실행한다.

    nmap -sU -p 161 --script=snmp-brute 192.168.0.1

만약 public - valid credentials라는 응답을 받았으면, community string을 알아낸 것이다. community string을 알아냈기에, `SNMP`를 통해 우리는 아래 정보를 알아낼 수 있다. 우리는 관리자 권한을 획득한 것과 마찬가지기 때문이다.

- System MIB: 호스트 이름, OS 버전, 마지막 부팅 시간과 같은 기본 시스템 정보.
- Interfaces: 루프백 및 물리적 네트워크 인터페이스의 세부 정보.
- Shared Printers: 네트워크에 공유된 프린터의 상태와 설치 여부.
- Services: 시스템에서 실행 중인 서비스 목록과 상태.
- Accounts: 시스템에 등록된 사용자 계정 정보.
- Shares: 네트워크를 통해 공유된 파일 및 폴더 자원 식별 가능.
- TCP/IP Networks: 시스템이 연결된 네트워크 인터페이스와 IP 주소 정보.
- Routes: 시스템의 라우팅 테이블을 확인하여 네트워크 경로 정보 열람 가능.
- UDP Services: 시스템에서 제공 중인 UDP 기반 서비스들을 식별.
- TCP Connections: 시스템에서 열려 있는 TCP 포트와 현재 활성화된 TCP 연결 확인 가능.

취약점을 종합해보자.

SNMP의 문제는 관리자 권한을 너무 쉽게 획득할 수 있다는 것이다. 이는 인증 과정이 부족하기 때문이다. 
또한, 평문으로 데이터가 전송되기에 정보가 쉽게 노출될 수 있을 뿐 아니라, 공격자는 위장을 쉽게 할 수 있다.
또한 악성 공격자가 SNMP 메시지의 순서를 변경하거나, 지연시키거나, 합법적인 메시지를 복사한 후 나중에 재전송하는 방식으로 메시지의 무결성을 위협할 수 있다.


## SNMP 취약점 해결 

이러한 문제를 해결하기 위해서 제일 베스트 방법은 `SNMP`를 사용하지 않는 것이다. 하지만 이는 서비스가 제한되므로 마냥 좋다고는 볼 수 없다.
따라서, `SNMPv3(최신 버전)`을 통해 `Community String`을 암호화시키거나, 만약 최신 버전을 사용하지 못한다면 Community String을 복잡하게 변경해야 한다. 또 다른 방법으로는 `SNMP`를 전달하고 받는, 즉 management system의 IP를 사전 등록 후, 나머지 IP에 대해선 차단을 하는 방식으로 허가된 시스템만이 SNMP를 사용해서 데이터를 전송하거나 받을 수 있도록 설정할 수 있다.

## 마무리하며

`SNMP`에 대해 알아보았다. 이는 편리하지만, community string을 알아내기 쉽다. 이 점이 취약점인데, 이를 보호하기 위해서 community string을 강화하거나, `SNMPv3 - 암호화 지원되는 최신 버전`을 사용하거나, SNMP 통신을 할 `IP 주소를` 사전에 정해둠으로 취약점을 해결할 수 있다.  
