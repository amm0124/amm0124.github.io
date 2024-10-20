---
title: "[CS/Network Security] 네트워크보안 - Data Collection(2)"
tags:
    - CS
    - Network Security
    - Data Collection
    - Network
    - Security
    - FootPrinting
    - Scanning
    - FireWall
    - Cybersecurity
    - Banner grabbing
    - firewalk
date: 2024-10-17 12:30:00 +
thumbnail: "https://github.com/user-attachments/assets/c9107ed4-ad2e-4d67-be25-cf41b5e37df8"
categories : Network Security
description: Network Security - Scanning과 FootPrinting에 대해 알아보자.
---

## 서론

해킹을 하기 위해선 보통 아래와 같은 순서를 따른다.
![image](https://github.com/user-attachments/assets/3939b565-8944-459d-a60e-35417b4a0d92)
해킹을 하기 위한 정보 수집 단계를 알아보자.

## FootPrint

발자취라고 한다. 이는 해킹의 초기 단계로 공격 대상을 조사하여, 정보를 수집하는 방법이다. 해킹을 하기 위해선, 내가 공격하고자 하는 타겟을 분석하는 것이 기본이기 때문이다. 얻은 정보를 기반으로 시스템의 약점을 파악할 수 있다. 또한, 사회공학적으로 정보를 알아내는데, 이는 악성 유저가 악의적인 의도를 가지고 일반 유저에게 개인 정보를 얻어내는 것 또한 속한다. 

## Scan

Scan은 정보를 기술적으로 수집하는 것을 의미한다. 현재 실행되고 있는 machine이 어떤 것인지, 열려 있는 포트가 몇 번인지, OS를 어떤 것을 쓰는지 .. 등등 실제로 요청을 보내 분석하는 것을 `Scan`이라고 한다.
`Ping`을 보내서 스캐닝을 하거나, network 계층 위에서 작동하는 `ICMP`를 사용한 Scan, `TCP/UDP`를 활용하여 Scan을 할 수 있다.

## Ping Scan

`Ping`은 network가 어떻게 작동하고 있는지 간단한 요청을 보내는 `utility`다. ICMP 기반으로 ping을 보낼 수도 있고, `TCP/UDP` 기반으로 ping을 보낼 수도 있다. 아래는 `ICMP` 기반 +  127.0.0.1(jekyll blog - local server)로 ping을 보내는 예제다. `ICMP는 network layer` 위에서 작동하는 프로토콜이므로 port 번호는 필요 없다.

![image](https://github.com/user-attachments/assets/463c0179-89bd-4018-b77a-b72fe615e2f2)

## TCP Scan

TCP 기반으로 Scanning하는 방법에 대해 알아보자. TCP는 `3-handshaking`기반으로 연결을 만든다. 정상적으로 열려있는 port에 대해서는 SYN / SYN+ACK / ACK 방식으로 연결을 만든다. 하지만 열려있지 않은 포트에 대해선, RST packet을 응답한다. 아래는 이를 그림으로 나타낸 것이다.

![image](https://github.com/user-attachments/assets/b50c3425-ea9d-44f3-aefd-82af9c2a9830)
    
## TCP - Stealth Scan

Scanning을 할 때 로그를 남기지 않아야 한다. 즉 비밀스럽게 Scanning을 해야 한다. 근데 만약 Scanning하는 port가 열려 있다면, 부득이하게 log가 남을 것이다. 이를 방지하기 위해 3-handshaking에서 2번째 응답까지만 받고, 마지막 `ACK packet`을 날리지 않는다. 이러면 server 입장에선, 3-handshaking이 완료되지 않았다고 판단하고, log를 남기지 않는다. 이를 `TCP Half Open scan`이라고 한다. 아래는 상황을 나타낸 그림이다.
 
![image](https://github.com/user-attachments/assets/ad91f39f-696e-4a98-875c-aa9a26559980)

또한, packet header를 조작해서 비밀스럽게 scan하는 방식도 존재한다. 

- FIN (Finish) Scan : FIN flag를 설정한다. 
- NULL Scan : flag를 아무것도 설정하지 않고 packet을 보낸다. 
- XMAS Scan : ACK, FIN, RST, SYN, URG flag를 setting하고 packet을 보낸다.

위 방식은 모두 열려있는 포트에 대해선 응답이 없고, 닫힌 포트에 대해선 RST packet을 받는다.

![image](https://github.com/user-attachments/assets/7e055be1-67b4-4577-99b6-21ef86bdfdce)

`RST packet`에도 정보가 담겨있다. 이제 이를 분석해야 한다. 포트가 열려 있다면, 남은 TTL의 값이 `1 ~ (OS 기본 TTL-1)` 사이일 것이다. 만약 hop = TTL인 상황이라면, 도착 시 TTL이 0인 상황은 TTL=0이므로 버려버린다. 따라서 남은 TTL은 무조건 1보다 켜야 한다. 만약 포트가 닫혀 있다면, `window size=0`인 응답을 받을 수 있다. 이는 암묵적으로 port가 닫혀 있어서 보낼 data가 없음을 의미한다. 위 방법들은 단순하지만 꽤나 효과적이다. 서버는 이를 정상적인 상황인지, Scanning 상황인지 감지할 방법이 없기 때문이다. 3번째 ACK가 오지 않는 이유는(즉, SYN packet으로 scanning하는 경우) 우리 입장에선 log를 남기지 않기 위해서지만, 서버 입장에선 `네트워크 통신 장애가 생겼다 .. 등`으로 생각을 할 수 있다.

## TCP - 방화벽 우회

또한, TCP header는 기본 20 byte고, flag에 따라 최대 60 byte까지 설정될 수 있다. 20 byte가 넘는다면, `TCP fragmentation`이 진행된다. 
분할된 첫 번째 패킷에선 IP src/dst만 저장한다고 가정하자. 두 번째 패킷에선 port 번호만 존재한다. 즉 아래와 같은 상황이다.

![image](https://github.com/user-attachments/assets/6a89a8be-8cdf-416a-a67c-61bfb8a995f9)
출처 : [https://moaimoai.tistory.com/145](https://moaimoai.tistory.com/145)

그리고 포트 번호 기반으로 방화벽은 filtering하는 상항이다. 첫 번째 패킷, 즉 우측 아래 패킷은 tcp port 번호가 존재하지 않으므로 방화벽이 통과시킨다. 두 번째 패킷은 첫 번째 패킷이 통과되었기에, 방화벽의 옵션에 따라서, 통과시킬 수도 있다. 이러한 `TCP fragmentation` 방법으로 방화벽을 우회시키고, Scanning을 할 수 있다. 방화벽은 한 번에 많은 양의 요청이 들어오면 이를 차단시킨다. 이러한 점을 이용하여 시간차를 두어 packet을 보냄으로 방화벽을 우회시킬 수 있다. 아래는 일반적은 스캐닝을 위한 타이밍 옵션이다.

- **Paranoid**: 패킷을 5분 또는 10분 간격으로 하나씩 전송한다. 이 방법은 매우 느리지만 탐지될 가능성이 거의 없다.
- **Sneaky**: WAN(광역 네트워크)에서는 15초마다, LAN(근거리 네트워크)에서는 5초마다 패킷을 전송한다. 이는 속도와 은밀함 사이의 균형을 맞춘다.
- **Polite**: 0.4초 간격으로 패킷을 전송한다. 이는 네트워크를 과부하시키지 않으면서도 적당한 속도를 유지한다.
- **Normal**: 기본 타이밍 설정. 이 설정은 더 빠르지만 보안 시스템에 의해 탐지될 가능성이 높다.

이러한 타이밍 옵션을 통해 대상 네트워크의 특정 요구 사항과 보안 상태에 따라 스캐닝 접근 방식을 조정할 수 있다.

## TCP - 취약한 FTP 서버 활용 (FTP bounce scan)

`FTP`는 파일 전송 프로토콜이다. `FTP 서버`의 취약점을 활용하여 비밀스럽게 Scanning 할 수도 있다. Attacker는 21번 포트를 사용하여 FTP 서버와 연결을 만든다. 이후 `PORT command`를 사용하여 `target host`의 포트가 열려 있는지 확인을 할 수 있다.

    port 210.121.128.9 17

같은 명령어를 사용하면, ftp server는 210.121.128.9 주소의 17 포트를 scanning 할 수 있다. 이를 통해 모든 포든 포트를 스캐닝 할 수 있다. 아래는 FTP bounce scan을 그림으로 나타낸 것이다.

![image](https://github.com/user-attachments/assets/11a21dea-1bbe-4fce-b193-533065cf82d0)

## UDP scanning

`UDP`는 본래 응답이 없다. 신뢰성을 철학으로 두지 않는 전송 프로토콜인데, 목적지에 도달하지 못한다면 `ICMP unreachable message`가 나에게 전달된다. 만약 포트가 열려있다면 아무런 메시지가 전달되지 않는다. 이를 통해 Scanning 할 수 있다.

## scanning tool

`linux` 기준, `fping`이나 `Nmap`을 사용하여 port scanning을 할 수 있다. 전자는 `ICMP` 기반 scanning이고, 후자는 `TCP/UCP` 기반 scanning이다.

## fping 

ICMP 기반이므로 port 번호는 필요하지 않다.

    fping -q -a -s 192.168.0.0/24 

이는 하위 8비트 (192.168.0.1~ 192.168.0.254) (0번은 서브넷의 네트워크 주소, 255는 브로드캐스팅 서버이므로 제외한다.)에 대해 scan을 한다는 의미이다.
-q는 icmp message를 숨기는 것이고, -a는 현재 열려있는 system, -s는 scan후 결과를 보여주는 옵션이다.


## Nmap

`TCP/UDP` 기반으로 작동한다. 즉 port 번호가 필요하다.

    nmap -sF -p 80,139 192.168.0.1

-sF는 Fin flag를 설정하여 80번 포트를 스캔한다는 의미이다. 즉 Stealth Scan을 한다는 의미다.

## Banner Grabbing

어떤 server에 접속했을 때, OS나 소프트웨어 버전을 확인 할 수 있는 `banner`를 확인함으로, 시스템에 대한 정보를 수집할 수 있다. 이를 통해 OS의 버전을 추측할 수 있고, 시스템의 취약점이나 공격 가능한 지점을 찾을 수 있다. `NetCraft`를 사용해서 attack target의 OS 정보를 획득할 수 있다.

## firewalk

`traceroute`를 사용하여 방화벽을 탐지하는 방법은 아래 포스팅을 참고하면 될 듯 하다.
[https://amm0124.github.io/CS/Network%20Security/2024-10-17-datacolleciton(1).html](https://amm0124.github.io/CS/Network%20Security/2024-10-17-datacolleciton(1).html)
요약하자면, 방화벽이 있는 곳에선 *(asterisk)를 표시한다는 것이다. 이는 방화벽에서 패킷을 filtering한다는 것을 의미한다. `firewalk`는 이 점과 유사하다. 이는 방화벽의 `Access Control List`를 찾는 프로그램이다. 방화벽이 감지되면, 즉 *(asterisk)를 받으면 이보다 하나 더 큰 TTL 값을 가진 packet을 계속 전송한다. 방화벽이 packet을 차단하면, 즉 응답이 돌아오지 않으면 해당 포트는 닫혀 있다고 판단할 수 있다. 반면 `ICMP Time Exceeded` 응답을 받으면 포트가 열려있다고 생각할 수 있다.



## 마무리하며

`정보 수집 과정- FootPrinting과 Scanning`에 대해 알아보았다. 
Scanning은 `ICMP/TCP/UDP` 기반으로 이루어질 수 있다. 또한, 방화벽의 open port를 알 수 있는 `firewalk`와, server의 정보를 기반으로 scanning하는 `Banner grabbing`에 대해서도 알아보았다. 

