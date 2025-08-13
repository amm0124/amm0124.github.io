---
title: "Spring Boot 시작하기"
excerpt: "Spring Boot 프로젝트 생성부터 기본 설정까지 Spring Boot 프로젝트 생성부터 기본 설정까지 Spring Boot 프로젝트 생성부터 기본 설정까지 Spring Boot 프로젝트 생성부터 기본 설정까지 Spring Boot 프로젝트 생성부터 기본 설정까지"

categories:
  - Spring
tags:
  - [Spring Boot, Java, Backend]

toc: true
toc_sticky: true

date: 2025-01-01
last_modified_at: 2025-01-01
---

## Spring Boot 소개

Spring Boot는 Spring 프레임워크를 더 쉽게 사용할 수 있도록 도와주는 도구입니다.

### 주요 특징

- 자동 설정 (Auto Configuration)
- 내장 서버 (Embedded Server)
- 스타터 의존성 (Starter Dependencies)

## 프로젝트 생성

Spring Initializr를 사용하여 프로젝트를 생성할 수 있습니다.

{% highlight bash %}
curl https://start.spring.io/starter.zip \
  -d dependencies=web,jpa,h2 \
  -d name=demo \
  -o demo.zip
{% endhighlight %}

### 기본 구조

```
src/
├── main/
│   ├── java/
│   └── resources/
└── test/
    └── java/
```

Spring Boot를 사용하면 빠르게 웹 애플리케이션을 구축할 수 있습니다.