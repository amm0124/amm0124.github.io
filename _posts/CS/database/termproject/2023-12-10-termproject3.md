---
title: db_termproject(3) - 여러가지 기능들
date: 2023-12-10 00:30:00 +
categories: [CS, database]
tags : CS DB
---

# 장바구니, QnA, 주문, 리뷰, 이벤트, 사이즈 구현

product에 비해 간략합니다.

## 이벤트(event_table)

이벤트 구현은 간단합니다. 
그냥 customer_table에 존재하는 customer_id를 foreign key로 갖는, event_table을 만들면 됩니다.
이름을 event_candidate_customer_id로 명명하였습니다.
administor은 그냥 event_table에 존재하는 event_candidate_user_id중 랜덤하게 몇 개 뽑아서, 메일을 보내면 되기 때문입니다.
customer_id가 삭제되면 event_table에 있는 event_candidate_user_id row도 삭제되어야 하기 때문에 on delete cascade 옵션을 생성 시 주었습니다. 변경 시엔 UPDATE합니다.

### query code

[event_table] 생성 쿼리

    CREATE TABLE event_table (
        event_candidate_customer_id varchar PRIMARY KEY,
        participation_start_time timestamp,
        FOREIGN KEY (event_candidate_customer_id) REFERENCES customer_table(customer_id) ON DELETE CASCADE ON UPDATE CASCADE
    );


## 장바구니(wishlist)

장바구니 구현도 쉽습니다.
product_table에 있는 subcode를 foreign key로 가져야 합니다. 
또한, customer_table에 있는 customer_id를 foreign key로 가져야 합니다.<br>

customer_id가 변경되거나, 삭제가 되면 장바구니에 있는 customer_id도 변경, 삭제 되어야 하기 때문에 ON DELETE CASCADE, ON UPDATE CASCADE 옵션을 생성 시 주었습니다. <br>

subcode가 변경되면, 자연스럽게 UPDATE가 되어야 하기 때문에, ON UPDATE CASCADE 옵션을 설정하였고,
만약 subcode가 삭제가 된 다면, (즉, seller가 탈퇴를 해서 mapping되는 모든 product가 삭제가 되거나, 
seller가 더 이상 그 품목을 팔지 않을 때) 장바구니에서 바로 삭제합니다.

또한, 장바구니에 있는 물품을 사면 장바구니에 있었던 물품을 삭제합니다.

### query code

[wishlist] 생성 쿼리

    create table wishlist(
        customer_id varchar,
        product_subcode int,
        count int,
        foreign key (customer_id) references customer_table(customer_id) on delete cascade on update cascade,
        foreign key (product_subcode) references sub_product (subcode) on delete cascade on update cascade
    );


## QnA(QnA_table)

QnA도 장바구니와 비슷합니다.
product_table에 있는 subcode를 foreign key로 가져야 합니다. 
또한, customer_table에 있는 customer_id를 foreign key로 가져야 합니다. <br>

customer_id가 변경되면, QnA 게시판에 있는 customer_id도 변경되게 ON UPDATE CASCADE 설정을 하였습니다. 
만약 삭제가 된다면, 삭제 되어야 하기 보단 ON DELDET SET NULL옵션을 주어, 다른 customer들도 볼 수 있도록 설정을 하였습니다. 
subcode가 변경 된다면, 당연히 update가 되어야 할 것입니다.
subcode가 삭제 된다면, 딱히 QnA는 없어도 되기에, ON DELETE CASCADE를 사용하여 삭제할 수 있도록 하였습니다.

### query code

    create TABLE QnA(
        customer_id VARCHAR,
        product_subcode int, 
        question varchar DEFAULT NULL,
        seller_id varchar,
        answer varchar DEFAULT NULL,
        qna_num INT,
        foreign key (customer_id) references customer_table(customer_id) on delete SET NULL on update cascade,
        foreign key (product_subcode) references sub_product (subcode) on delete cascade on update cascade 
    );


## 주문 및 리뷰(order_table)

### 주문 

주문은 이벤트, 장바구니, QnA보다 살짝 더 복잡합니다.
customer_table에 있는 customer_id를 foreign key로 가져야 합니다.
product_table에 subcode를 foreign key로 가져야 합니다.
seller_table에 있는 subcode를 foreign key로 가져야 합니다.

또한 customer_table에 있는 point가 product_table의 product_price보다 작다면 주문을 할 수 없습니다.
만약 주문이 성사됐다면, order_table에 customer_id, seller_id, 주문 수량(count), 1개당 판매 가격을 기록합니다.
또한, 각 주문마다 order_code를 주어, data를 구분하였습니다. order_time_stamp라는 값을 주어, 만약 주문 후 1주일이 지났다면, 환불을 하지 못하도록 구현하였습니다.

subcode가 삭제되어도 주문 기록을 삭제할 필요는 없기에, on delete 옵션을 NO ACTION으로 설정했습니다.
customer_id가 삭제 된다면 기록은 남겨두지만, customer_id를 지워야 하기 때문에 ON DELETE 옵션을 SET NULL로 설정했습니다. 
seller_id가 삭제 되어도 주문 기록을 삭제할 필요는 없기에, on delete 옵션을 SET NULL로 설정했습니다.


#### review table 시행 착오

처음에는 customer_id, product_subcode를 foreign key로 갖는 review_table을 만들려고 했습니다.
따라서 order_table에서 customer_id, product_subcode를 primairy key로 지정했습니다.
하지만 이 경우, ON DELETE SET NULL option을 주면 primary key는 NULL이 되면 안된다는 무결성 제약 조건을 위배하게 됩니다. 따라서, 참조를 하지 않고 그냥 하나의 table로 합치자는 생각을 했습니다.  

### 리뷰 

height, weight column이 존재합니다. 이는 꼭 customer의 height와 weight를 사용하지 않아도 됩니다.
왜냐하면 선물로 사용되는 경우도 있기 때문입니다. 기본으로 customer의 height, weight를 리뷰에 사용하되,
customer의 옵션에 따라서 새롭게 height와 weight를 저장합니다.
마지막으로, review의 내용(review_content)과 별점(review_point)가 존재합니다.

### query code

[order_review_table] 생성 쿼리

    CREATE TABLE order_review_table (
        order_code int,
        seller_id varchar,
        product_subcode int,
        count INT,
        price_per_1 INT,
        customer_id varchar,
        order_start_time timestamp,
        review_point int DEFAULT NULL CHECK (review_point >= 0 AND review_point <= 10),
        review_content varchar DEFAULT NULL,
        user_height INT,
        user_weight INT,
        FOREIGN KEY (customer_id) REFERENCES customer_table(customer_id) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY (product_subcode) REFERENCES sub_product (subcode) ON DELETE NO ACTION ON UPDATE CASCADE,
        FOREIGN KEY (seller_id) REFERENCES seller_table(seller_id) ON DELETE SET NULL ON UPDATE CASCADE
    );

## User별 Diagram

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/f4e868ed-8269-4d37-ba78-c0295582b91f)

최종적으로 이렇게 완성이 되네요. <br> 
맨 처음에 4개 foreign key를 사용한 것 보다 제가 보기엔 깔끔하게 생긴 듯 합니다.


## 사이즈 추천

customer가 사이즈 추천을 원하는 subcode를 입력합니다. customer가 선물을 할 수 있기에, 옵션으로 height, weight를 입력받습니다. 옵션을 선택하지 않으면, 기본 값으로 customer의 height와 weight가 선택됩니다. review_table에서 subcode를 기준으로 10점 중 7점 이상인 row의 height와 weight만 select해서 이러한 data를 기반으로 dataframe을 만듭니다. sklearn.tree로부터 불러온 DecisionTreeRegressor를 사용해서 사이즈를 추천합니다.

### 마무리하며

다음 글에선 ROLE 설정 및 VIEW 설정에 대해 다뤄보겠습니다.
