---
title: "[CS/Database] 데이터베이스 - Relation Algebra(1)"
tags:
    - CS
    - Datebase
    - relation algebra
    - 관계 대수
    - DB 
    - sql
date: 2024-10-13 21:30:00 +
thumbnail: "https://github.com/user-attachments/assets/d0bcf7d0-6d02-4d43-a0e2-8e7bab8009f5"
categories : database
description: Database - 관계 대수를 알아보자.
---

# 서론

Database의 관계 대수 - `selection, projection`를 알아보자. 


## 대수

대수(Algebra)라는 것은 다들 많이 들어보셨을 것입니다. 선형`대수`학이나 등등..에서 말이죠.
근데 `대수`의 정의를 물어보면 뭔가 대답하기 애매합니다. 일단 관계 대수를 알아보기 전에 대수에 대해서 알아봅시다.

`대수`라는 것은 수학적 구조와 그 위에서 정의된 연산에 대한 규칙을 연구하는 학문입니다. 예를 들어 절대 바뀌지 않는 공리와 같은 것을 연구하는 학문입니다. 즉, 내가 하고자 하는 연산의 기초를 연구한다는 것입니다.

이제 `대수`를 이해했으니, 데이터베이스의 관계 대수에 대해 알아봅시다.

## 관계 대수 

참고로, relation은 데이터들을 저장하는 table과 같다고 생각해도 됩니다.

데이터베이스는 말 그대로 데이터들의 base입니다. 즉 많은 데이터가 존재합니다. 이러한 데이터들끼리 관계가 있습니다.
이러한 데이터들 사이의 관계를 수학적으로 나타내기 위한(즉, 연산 등의 기초) 대수가 `관계 대수(Relation Algebra, RA)`입니다. 이는 관계에 대한 연산이자, 테이블(데이터들의 모음)에 대한 연산이라고 생각할 수 있을 것 같습니다.

SQL engine은 user가 작성한 sql(query)을 RA(Relation Algebra)로 변경한 다음, 이를 최적화하고 실행합니다. 이는 뭔가 코딩을 한 다음, 어셈블리어로 변경된 후, 최적화 과정을 거쳐서 결국 binary code가 되는 것과 유사합니다. 어떤 RA가 있는지 알아봅시다.

관계 대수에는 두 종류가 존재합니다. 하나의 relation을 사용해서 새로운 relation을 만드는 `Unary Operation`와, 두 개의 relation을 사용해서 새로운 relation을 만드는 `Binary Operation`이 있습니다.

보통 수학에서 좌변이라는 input을 토대로, 우변이라는 output을 만들어냅니다. 전자는 하나의 input에 어떤 연산을 해서, 새로운 1개의 output으로 나타내는 것입니다. 반대로 후자는, 2개의 input에 어떤 연산을 수행하고, 새로운 1개의 output을 나타내는 것입니다.

전자의 대표적인 예시는 select, rename..등이 있을 것이고, 후자의 대표적인 예시는 Cartesian Product(join 이라고 생각하시면 편합니다.), difference(빼기)가 있습니다.

## 관계 대수의 operators(연산자)

관계 대수에는 5개의 core operator(기본 연산자)가 존재합니다. 이러한 기본 연산자를 활용하여 추가적인 operator를 만들 수 있습니다. 아래는 5개의 core operator입니다.
- selection(𝜎)
- projection(π)
- union(∪)
- set difference(-)
- cartesian product(×)

즉, 이러한 5가지 연산을 토대로 우리가 작성하는 sql은 구성되어 있다는 의미입니다.

## selection 

말 그대로 고르는 행위입니다. 우리는 어떤 조건에 대해서 data를 고릅니다. 관계 대수에서 조건을 나타내는 방법은, 연산자 아래 작은 첨자로 조건(수학적 부등호)을 표시합니다. 

![예시 테이블](https://github.com/user-attachments/assets/f931ef3b-7a47-4268-afde-6f215a9b8bd6)

테이블에서, salary>90000인 data(row)를 고르고 싶다면 아래와 같이 작성할 수 있습니다.

![salary>90000 조건](https://github.com/user-attachments/assets/f931ef3b-7a47-4268-afde-6f215a9b8bd6)

## projection

projection도 selection과 유사합니다. 하지만 다른 점은, selection은 row를 고르는 반면, projection은 column을 고릅니다. 

![image](https://github.com/user-attachments/assets/2c15d3d8-a9e3-4389-b434-a796e9ce6248)

테이블에서, 1년 salary가 아닌, 1달의 salary를 보고 싶으면, 기존 salary에 12를 나누면 됩니다.
이를 projection을 사용해서 표현할 수 있습니다.

![image](https://github.com/user-attachments/assets/7b58b976-3812-4bcb-b3af-ff15b451027f)

## selection과 projection의 속성

`이 두 가지 연산은 중복을 제거합니다.` 그러면 이 두 가지 연산에서 중복을 제거하기 위해 database는 집합으로 이루어져 있을까요?
`정답은 아닙니다.` 왜냐하면 일단 수 많은 데이터에서 매번 중복을 제거하는 연산은 굉장히 비효율적일 뿐 아니라, 상황에 따라서는 중복을 허용해야 합니다. 이러한 구조를 set이 아닌 bag이라고 합니다. 또한 중복을 허용하거나 허용하지 않음에 따라서 평균 및 합계 .. 등등의 연산의 결과는 달라질 수 있기 때문입니다. 

결과론적으로, selection과 projection은 중복을 제거하지만, db가 set으로 이루어져 있지는 않다는 것입니다.(bag이라고 합니다.)

또한, selection 연산은 각 data들이 table에 매칭되게 출력이 되어야 하고(schema가 일치한다고 합니다),
projection 연산은 projection을 선택한 column만 포함해야 합니다.

## 교환 법칙 (Commutative property)

selection과 projection에 대해 알아보았는데, 이 두 연산은 과연 교환법칙이 성립될까요?
정답은 `x`입니다. 

![image](https://github.com/user-attachments/assets/cc273629-0975-445d-ab69-763b3aa923e9)

예시를 살펴봅시다. 아래 연산의 경우에는 먼저 firstName column을 projection했기에, birth column은 존재하지 않습니다. 따라서 오류를 낼 것입니다. 교환 법칙이 성립하지 않는 예시를 살펴보았습니다.

그러면 column과 projection을 사용해서 어떤 결과를 내고 싶은데, 어떤 연산을 먼저 수행해야 할까요?
이는 table의 구조에 따라서 다릅니다.

만약 row oriented table이라면 selection 후 projection을 하는 것이 좋고, 
column oriented table이라면 바로 projection을 하는 것이 좋습니다.

왜냐하면 row oriented는 조금이나마 data를 줄인 다음 projection을 하는 것이 연산이 빠릅니다.
반대의 경우는 projection을 바로 하면 내가 필요로 하는 데이터를 바로 받아올 수 있기 때문입니다.

자세한 내용이 궁금하시다면 아래 블로그를 참조해주시면 좋을 것 같습니다.
[link : https://haeunyah.tistory.com/69](https://haeunyah.tistory.com/69)

## 마무리하며

관계 대수의 기본 연산 `selection, projection`에 대해 알아보았습니다.