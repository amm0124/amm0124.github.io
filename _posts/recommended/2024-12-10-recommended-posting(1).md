---
layout : post
title: "[추천] SYN Flooding Attack으로 알아보는 GO에서 3-way handshaking의 backlog 값 변경하기"
tag : [recommended, network, Dos, DDos, SYN Flooding]
date: 2024-12-10 09:30:00 +
categories : [추천]
description: SYN Flooding 추천 글
topping : false
sitemap: 
    changefreq : 
    priority : 
---


* content
{:toc}

## 추천 포스팅

[링크 : SYN Flooding in CLOUDFLARE](https://blog.cloudflare.com/ko-kr/syn-packet-handling-in-the-wild/)

## 후기

> `DoS(Denial of Service`의 `SYN Flooding Attack - SYN Cookie`를 공부하다 읽은 글이다. 이해하기 쉽도록 설명이 되어서 추천한다.

`backlog queue(글에선 SYN queue라고 표현하였다)`는 수신 SYN 패킷을 저장하고, 타임아웃시 재시도하는 역할을 하는 queue이다. backlog queue, Accept queue의 관점으로 바라보는 `SYN Flooding attack`에 대한 글이다. 특이한 점은 `Go Lang의 기본 TCP 서버(net/http)는` backlog 값 변경을 지원하지 않고 128로 고정했다는 점이다. 이를 변경하기 위해선 내가 찾아본 바로는 대략 3가지 방식이 존재하는 거 같다. 



**2024.12.13 추가 : Go의 기본 설정을 바꾸는 것 보다는, nginx와 같은 웹 서버를 프론트 프록시 서버로 두어, 로드밸런싱을 하는 것이 더 좋을 것 같다. 그리고 실제 요청을 처리하는 WAS(Web Application Server)는 사설 네트워크로 감싸서 안전하게 Syn Flooding 공격을 대응하는 것이 좋다고 생각이 든다.**



### 1번 방식 - OS 설정 파일 직접 변경

> 시스템에 전역적으로 적용되는 백로그 설정을 변경하는 방법이다. 이로 인한 책임은 개발자의 몫이다.

Linux OS 기준으로 `/etc/sysctl.conf` 파일의 ~~`tcp_max_syn_backlog` 값을 직접 변경하는 방법이다. 최근에는 net.core.somaxconn의 값을 수정한다고 한다.~~ 하지만 이는 시스템 전체에 적용되기에, 위험이 따르는 것 같다.

**2024.12.13 추가 :  [https://brunch.co.kr/@alden/5](tcp_syncookies는 어떻게 동작하는가?), [https://brunch.co.kr/@alden/6](syn_backlog와 somaxconn 파라미터) `리눅스 커널 이야기` 저자 `강진우`님의 brunch story에 의하면, 위 두 파라미터는 변경 즉시 애플리케이션에 영향을 끼치지 않는다고 한다. 이에 대해서는 다음 포스팅에 더 자세하게 다루도록 하겠다.**

**사담이지만, 확실히 이런 시스템쪽 내용을 다루는 것이 재밌다. 어제 Go를 다루는 회사에 어제 면접을 다녀왔는데, Go 언어가 되게 좋은 점이 많은 것 같다. 문법도 간편하고, 비동기 처리도 간편하고, 아무튼 언어에 대해 흥미가 생겼다.  `그림으로 배우는 리눅스 구조` 책이 Go 언어를 통해 리눅스 커널을 다루는 예제가 많던데, 시험 끝나고 이번 기회에 리눅스 커널 구조도 다시 공부하고, Go 언어에 대해서도 공부를 해봐야겠다.**


### 2번 방식 - 라이브러리를 통한 저수준 소켓 API 사용

`Go Lang`에서, 저수준 소켓 API를 지원하는 라이브러리가 존재한다. `syscall`이나 `golang.org/x/sys/unix` 패키지를 사용하면, application layer에서 소켓 생성 시 백로그 값을 명시적으로 설정할 수 있다고 한다. 아래는 GPT가 생성한 `syscall` 라이브러리를 사용한 Go 예시 코드이다. 이는 직접 소켓을 열어야 한다. 

```jsx
package main

import (
	"log"
	"syscall"
)

func main() {
	// 소켓 생성
	fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, syscall.IPPROTO_TCP)
	if err != nil {
		log.Fatalf("Failed to create socket: %v", err)
	}

	// 소켓 주소 바인딩
	addr := syscall.SockaddrInet4{Port: 8080}
	copy(addr.Addr[:], []byte{127, 0, 0, 1}) 
	err = syscall.Bind(fd, &addr)
	if err != nil {
		log.Fatalf("Failed to bind socket: %v", err)
	}

	// 백로그 값 설정 (예: 256)
	err = syscall.Listen(fd, 256)
	if err != nil {
		log.Fatalf("Failed to listen on socket: %v", err)
	}

	log.Println("Server is listening...")
}
```

### 3번 방식 - 다른 네트워크 라이브러리 활용

`net/http`가 backlog 값 변경을 지원하지 않는다면 다른 방식으로 tcp 서버를 구축하면 된다. 이를 테면, `fasthttp`와 같은 라이브러리를 사용하면 된다. `fasthttp`를 지원하는 Go 웹 프레임워크로는 `fiber` 등등이 존재한다.

## 마무리하며

처음으로 하는 글 추천이다. 글의 주제는 요즘 이슈가 되는 `DoS attack`중 `SYN Flooding`에 대한 글이다. `SYN Flooding`에 대해선 포스팅이 잘 작성되어 있으니 읽어보면 좋을 것 같다. 본 포스팅에선 `SYN Flooding`보다 `backlog 값 변경`에 대해 초점을 더 두었다. 

`Go Lang`을 기준으로 글을 작성하였지만, 방식은 어떤 언어를 사용하건 유사하다고 생각한다. 만약 머신에 대해 전역적으로 백로그 값을 수정하길 원한다면, OS 설정 파일을 열어 `backlog` 값을 변경할 수 있다. 만약 전역적으로 backlog 값을 변경하지 않길 원한다면 소켓을 직접 열거나, 다른 backlog를 수정할 수 있는 라이브러리(fasthttp..등)를 통해 백로그 값을 변경할 수 있다.