---
title: db_termproject(1) - 사용자 구현
date: 2023-12-9 23:00:00 +
categories: [CS, database]
tags : CS DB
---

# database termproject 주제

Git repository link : https://github.com/amm0124/2023_db_termproject/tree/main  입니다! 

데이터베이스 텀프로젝트 주제로 쇼핑몰을 선정했습니다.<br>
주제 선정을 쇼핑몰로 한 이유에 대해 간략하게 말씀드리자면. .. <br>

올해도 50일 채 남지 않았다. 계절이 바뀜을 하루하루 느낀다. 계절이 바뀌면서 사람들의 옷가지도 바뀐다. 현대인들은 각자의 사정으로 바쁘다. 학생들은 수업을 듣고, 직장인들은 출근을 한다. 계절은 바뀌는데, 사람들의 일상은 바뀌지 않는다. 
인터넷이 발달함에 따라, 인터넷 쇼핑은 점점 발전하고 있다. 하지만 인터넷으로 쇼핑을 했을 때, 사이즈가 맞지 않아서 환불하는 경우가 많다. 이러한 삶의 불편함을 해소하고자, “상품별로 고객의 추천 사이즈를 알려주는 인터넷 쇼핑 플랫폼”을 프로젝트 주제로 선정하였다.

데이터베이스 제안서에 제출한 주제 선정 동기입니다. 지금 읽으니 살짝 부끄럽네요.
아무튼 이러한 이유로 쇼핑몰 데이터베이스 구현으로 주제를 선정하였습니다.


## DATABASE USER

쇼핑몰을 사용하는 사람은 3가지 타입으로 분류될 수 있습니다.<br>
첫 번째로 고객, 즉 사는 사람입니다. <br>
두 번째로 판매자, 즉 파는 사람입니다.<br>
세 번째로 관리자, 즉 쇼핑몰 관리자라고 볼 수 있겠네요. <br>

## USER별 스키마 및 기능

### customer 

고객은 포인트를 선불로 충전하여 물건을 구매할 수 있습니다. 
물건을 살 때마다, 일정 비율로 포인트 환급이 됩니다. (적립의 개념) 
vip 등급은 3000원씩, 일반 회원은 1000원씩 환급이 됩니다.
회원 등급업은, 누적 사용 금액이 일정 수준을 넘어가면 VIP 회원으로 등급업이 됩니다.<br>
고객은 물건을 살 수 있을 뿐 아니라, 키와 몸무게에 따라서 옷들의 추천 사이즈를 받을 수 있습니다.<br>
또한, 내가 샀던 물건 조회, 고객 정보 수정, QnA 게시판 이용, 장바구니, 이벤트 참여를 할 수 있습니다. <br>

#### customer schema

[customer_table] 생성 쿼리

    create table customer_table(
        customer_id varchar primary key,
        customer_pw varchar,
        point INT, 
        vip BOOL,
        address varchar,
        height int,
        weight int,
        acc_use_money int DEFAULT 0
    );  


### seller

판매자는 물건을 팔 수 있을 뿐 아니라, 등록 물품 정보 수정을 할 수 있습니다.<br> 
또한, QnA 답변 달기, 판매액 집계, 자기 정보 수정을 할 수 있습니다.

#### seller schema 

[seller_table] 생성 쿼리

    create table seller_table(
		seller_id varchar primary key,
		seller_pw varchar
	);



### administor 

관리자는 물품의 누적 합계 금액 열람 및 당첨 메일 발송을 할 수 있습니다.<br> 
또한, 고객과 판매자의 정보 열람 및 기타 집계 정보를 볼 수 있습니다.

#### administor schema

[administor_table] 생성 쿼리

    create table administor_table(
		administor_id varchar primary key,
		administor_pw varchar
	); 


### 마무리하며

아무래도 각 타입별 사용자들의 기능과 table 생성이라 아직까진 별 내용이 없습니다. <br>
끝까지 봐주셨으면 합니다. <br>
다음 글에선 상품에 대해서 알아보겠습니다. <br>