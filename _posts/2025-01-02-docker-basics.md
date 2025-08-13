---
title: "Docker 기초 사용법"
excerpt: "Docker 컨테이너화 기술의 기본 개념과 사용법"

categories:
  - DevOps
tags:
  - [Docker, Container, DevOps]

toc: true
toc_sticky: true

date: 2025-01-02
last_modified_at: 2025-01-02
---

## Docker란?

Docker는 애플리케이션을 컨테이너로 패키징하고 실행할 수 있게 해주는 플랫폼입니다.

### 컨테이너의 장점

- 환경 일관성
- 빠른 배포
- 리소스 효율성

## 기본 명령어

### 이미지 관리

{% highlight bash %}
# 이미지 검색
docker search nginx

# 이미지 다운로드
docker pull nginx:latest

# 이미지 목록 확인
docker images
{% endhighlight %}

### 컨테이너 실행

{% highlight bash %}
# 컨테이너 실행
docker run -d -p 80:80 --name webserver nginx

# 실행 중인 컨테이너 확인
docker ps

# 컨테이너 중지
docker stop webserver
{% endhighlight %}

python

```py
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

dockerfile

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

go

```go
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```


bash

```bash
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```




## Dockerfile 작성

{% highlight dockerfile %}
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
{% endhighlight %}

Docker를 활용하면 개발 환경과 운영 환경을 동일하게 유지할 수 있습니다.