---
title: "[FastAPI] - SQLAlchemy 사용 시의 유의점"
excerpt: "SQLAlchemy를 통한 유의사항"

type: docs


categories:
  - Python
tags:
  - [Cloud Native, Cloud, Docker, k8s, Kubernetes]

toc: true
toc_sticky: true

date: 2025-10-02
last_modified_at: 2025-10-02
---


Python3의 SQLAlchemy 사용 시 유의점에 대해 알아보자.

# SQLAlchemy

```SQLAlchemy```란 Python 기반의 백엔드 프레임워크에서 SQL을 직접 사용하지 않고, Python 객체와 매핑해주는 ```ORM(Object-Relational Mapping)```입니다. 편리한 기능임에도 불구하고, ORM에 대한 이해가 부족하면 ```N+1```문제 등이 발생할 수 있습니다.

# 예제

```py
hello()
```








