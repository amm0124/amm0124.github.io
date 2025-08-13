---
title: "데이터베이스 인덱싱 최적화"
excerpt: "데이터베이스 성능 향상을 위한 인덱스 설계와 최적화 전략"

categories:
  - Database
tags:
  - [MySQL, PostgreSQL, Index, Performance]

toc: true
toc_sticky: true

date: 2025-01-04
last_modified_at: 2025-01-04
---

## 인덱스란?

인덱스는 데이터베이스에서 검색 속도를 향상시키기 위한 자료구조입니다.

### 인덱스의 종류

- 클러스터드 인덱스 (Clustered Index)
- 논클러스터드 인덱스 (Non-Clustered Index)
- 복합 인덱스 (Composite Index)

## 인덱스 생성

### MySQL

{% highlight sql %}
-- 단일 컬럼 인덱스
CREATE INDEX idx_user_email ON users(email);

-- 복합 인덱스
CREATE INDEX idx_order_date_status ON orders(order_date, status);

-- 유니크 인덱스
CREATE UNIQUE INDEX idx_user_username ON users(username);
{% endhighlight %}

### PostgreSQL

{% highlight sql %}
-- 부분 인덱스
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- 함수 기반 인덱스
CREATE INDEX idx_lower_email ON users(LOWER(email));
{% endhighlight %}

## 성능 최적화 팁

### 인덱스 선택도

{% highlight sql %}
-- 선택도 확인
SELECT 
  COUNT(DISTINCT email) / COUNT(*) as selectivity
FROM users;
{% endhighlight %}

### 실행 계획 확인

{% highlight sql %}
-- MySQL
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
{% endhighlight %}

## 주의사항

- 너무 많은 인덱스는 INSERT/UPDATE 성능을 저하시킵니다
- 사용하지 않는 인덱스는 정기적으로 제거해야 합니다
- 카디널리티가 낮은 컬럼에는 인덱스 효과가 제한적입니다

적절한 인덱스 설계로 데이터베이스 성능을 크게 향상시킬 수 있습니다.