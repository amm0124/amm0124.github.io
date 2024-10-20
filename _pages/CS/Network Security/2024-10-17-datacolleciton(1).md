---
title: "[CS/Network Security] 네트워크보안 - Data Collection(1)"
tags:
    - CS
    - Network Security
    - Network
    - Security
date: 2024-10-17 12:00:00 +
thumbnail: "https://github.com/user-attachments/assets/c9107ed4-ad2e-4d67-be25-cf41b5e37df8"
categories : Network Security
description: Network Security - 정보 수집에 대해 알아보자.
---

## 정보의 열람

일부 정보는 공개적이어야 하지만(대표적인 예시로 내가 운영하는 사이트의 정보를 알려주는 api는 공개적이어야 한다.), 일부 `도메인 정보`의 비밀 정보로 취급되어야 한다. `도메인 정보`는 인터넷 도메인 등록과 관련된 정보이다. 대표적으로 등록자 정보, 도메인 만료 날짜, 도메인 상태 등을 말한다. 
만약 `비밀 도메인 정보`가 유출된다면 보안 취약점을 야기할 수 있다. 
따라서 공개 정보는 적절히 잘 공개하고, 비공개 정보는 잘 숨겨야 한다.

현재 `Whois` 나 `nslookup(nameserver lookup)`, `Internet Assigned Numbers Authority (IANA)`, `Regional Institute Registries (RIRS)`, `traceroute` 등의 `도메인 정보`를 찾을 수 있는 많은 도구들이 존재한다. 등록자, 기술 담당자의 연락처 등은 공개되는 것이 바람직하지 않다. 하지만 도메인 이름이나, 네임서버는 공개되어야 하는 정보이다.

실제로 국제기구 `whois`에서 도메인 정보를 열람할 수 있는데, 기술 담당자 등의 정보는 도메인에 따라 선택적으로 공개한다.   
 
## Host Files

`host files`는 DNS 서비스가 존재하기 전부터 사용되던 파일이다. 이는 로컬 DNS서버의 역할을 한다. 즉, 사용자가 입력한 도메인 이름을 `host file`에 존재하는 IP 주소로 mapping해주는 파일이다. 
예를 들어, github.io blog를 local에서 키는 상황을 생각해보자. chrome 검색창에 꼭, 127.0.0.1:4000을 적지 않고, `localhost:4000`을 입력해도 로컬 블로그를 볼 수 있다. 내가 localhost라는 이름이 마음에 들지 않는다면, host file에서 127.0.0.1 (내가 원하는 도메인 이름) 으로 변경할 수 있다. 
참고로, 127.0.0.1은 OS나 등등의 요인에 따라, host file에 존재할 수도 있고, 하지 않을 수도 있다. 하지만 은 별도의 설정이 없으면 localhost는 127.0.0.1으로 resolution된다.  

`host file`의 사용 용도는 아래와 같다.

- DNS 서버가 다운될 때
- Internet이 아닌, 별도의 네트워크를 임의로 만들었을 때 : DNS 서버에 가지 않고 host file에서 resolution할 수 있다. 
- 여러 서버가 다른 IP 주소를 가지는데, 같은 도메인 이름을 가지는 경우 : 로드 밸런싱이나 가용성을 테스트하기 위해 어떤 서버(IP)로 접속할 지 정할 수 있다.

만약 악의적인 공격자가 어떤 형식으로 host file을 수정한다면, 위조 사이트로 연결될 수 있는 문제점이 발생한다. 


## DNS (Domain Name Server)

사용자는 접속하고자 하는 서비스의 IP주소를 다 알 수 없고, host file에 작성할 수 없다. `DNS`는 이러한 불편함을 해결하기 위해서 만들어진 것이다. 즉, IP 주소와 domain 이름을 mapping해주는 `네트워크 상에서 운영되는 host file`이라고 생각할 수 있다.

DNS는 아래와 같은 계층 구조를 가진다. 즉 tree 형태이다. 
![image](https://github.com/user-attachments/assets/5f640d5d-b7bc-482a-a342-e5da53ebef34)
트리의 모든 노드가 합쳐진, 즉 최종 도메인 이름을 `Fully Qualified Domain Name (FQDN)`라고 부른다. 네이버의 경우는 `www.naver.com`이다.

내가 `www.naver.com`에 접속하고 싶은 상황이라고 가정하자.
검색창에 `www.naver.com`을 입력한다. 컴퓨터의 `local cache`에 도메인 이름에 해당하는 IP 주소가 있다면 이를 바로 사용한다. 만약 존재하지 않는다면, 나와 제일 가까이 있는 `Local DNS server`로 query (질의)한다. 만약 존재하지 않는 경우라면, Root dns -> 하위 -> 점점 하위 .. dns 서버로 이동하며 `www.naver.com`의 IP주소를 가지고 있는 서버까지 이동한다. 존재한다면, Local Dns server는 `www.naver.com`에 해당하는 `IP`주소를 받고, 이를 나의 컴퓨터로 전달한다. 이후, 받은 `IP 주소`로 다시 질의한다. 즉, 나의 컴퓨터는 처음에는 dns 이름으로, 두 번째는 IP 주소로 `2번의 질의`를 한다. 로컬 컴퓨터의 `DNS cache table`을 보고 싶으면 터미널에서 

    ipconfig/displaydns 

를 통해 확인할 수 있다.

## DNS server 종류

DNS 서버는 `primary dns server, secondary dns server, cache dns server`의 세 종류로 나뉜다. 
`primary dns server`는 내가 요청한 dns에 대해 주로 대답을 하는 서버이다. `A 레코드나, MX 레코드, AAAA 레코드, CNAME 레코드 ..`등을 관리한다. 즉, `www.naver.com` 에 해당하는 IP 주소를 답변해주는(A 레코드) 주된 name server이다.
`secondary dns server`는 말 그대로 두 번째 서버다. 이는 주로 백업용으로 사용된다. `primary server`가 고장나면 사용된다. `cache dns server`는 말 그대로 cache server다. 질의에 대한 응답을 caching하는 서버다.

## IP 주소에 대한 tracking

[https://www.ip-tracker.org/](https://www.ip-tracker.org/) 라는 웹사이트를 활용하면 대충 IP 주소에 해당하는 현실 위치를 알 수 있다. 또한, [google apps : 이메일 기반 IP 추적](https://toolbox.googleapps.com/apps/messageheader/analyzeheader)을 사용하면 `SMTP header정보 기반`으로 IP를 tracking 할 수 있다. 또한, web server를 운영중이면 이를 log로 남길 수 있다. 

`traceroute`라는 프로그램에 대해 알아보자. 이는 source -> destination으로 packet을 전송할 때, 어떤 경로로 가는 지, 추적할 수 있는 프로그램이다. 말 그대로 `route를 tracing` 할 수 있다. 또한 몇 개의 router를 뛰어 넘었는지 `TTL(=hop)`을 측정할 수 있다.

![image](https://github.com/user-attachments/assets/2b829fe1-9d7e-49cd-a69b-bc5845a51bfc)


기본 방식은 src에서 dst로 packet을 날릴 때, `TTL 값을 하나씩 늘리는 것`이다. packet이 router에 도달했을 때, TTL이 0이면 그 자리에서 packet을 폐기한다. 이를 기반으로 route를 추적할 수 있다.
기본적으로 `UDP packet`을 사용한다. 경우에 따라서 `TCP, ICMP packet`를 사용할 수 있다.

`UDP/TCP packet`을 사용하는 경우는 포트 번호가 필요하다. 왜냐하면 이는 4계층 `transport layer에서 작동하는 protocol`이기 때문이다. 만약 `ICMP packet을 사용하는 경우는 포트 번호가 필요로 하지 않다.` 왜냐하면 이는 3계층 Network layer의 IP protocol 위에서 동작하는 이를테면 `3.5계층 protocol`이기 떄문이다. 보통 TCP packet은 사용하지 않는다. 왜냐하면 응답 packet의 src만 알면 되기 때문이다. TCP는 이러한 용도에는 너무 overhead가 크다.

UDP에서 TTL이 0이 되고, port에 도달하지 못했다면, `port unreachable` message를 응답받는다. 이를 통해 route를 추적할 수 있다. ICMP를 사용하는 경우에는, 도달하지 못했다고 `echo reply`를 받을 수 있다.

먼저 TTL=1로 설정한 후, destination으로 packet을 `3`개 보낸다. 만약 목적지에 도달하지 못한 경우라면, router에서 폐기했다고 응답을 받을 것이다. 이후 TTL을 하나 더 늘려서 destination으로 packet을 3개 보낸다. 다음 router에서 응답을 할 것이고.. 최종적으로 `destination으로 갈 때 까지 router의 IP 주소를 다 획득할 수 있다`. route를 추적한다는 traceroute라는 이름을 이해할 수 있을 것이다.

`*(asterisk)` 응답을 받을 수도 있다. 이는 destination에 도달하기 전, TTL=0이 된 곳이 `방화벽`임을 알려준다. 방화벽에서 packet을 폐기했고, 따로 응답을 하지 않아서 사용자에겐 *라는 메시지로 표현이 된 것이다.

내가 `traceroute`를 사용하여 source -> destination으로 packet을 보내는 상황을 생각해보자. 네트워크 상황에 따라, route는 계속 변하는데, 만약 계속 고정이 된 상황이다. 이는 누군가가 의도적으로 어떤 destination에 대한 `route를 의도적으로 고정시킨 것`이다. 감시의 주체가 누군지는 모르겠지만, 현재 `감시/감청`을 당하는 상황을 생각해볼 수 있다.

참고로 `linux에선 traceroute고, window에서 tracer`이다. [https://visualtraceroute.net/](https://visualtraceroute.net/)을 사용하면 어떤 route를 거쳐가는지 시각적으로 확인할 수 있다.

