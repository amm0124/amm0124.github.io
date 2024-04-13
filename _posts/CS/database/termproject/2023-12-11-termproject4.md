---
title: db_termproject(4) - view and authorization
date: 2023-12-11 00:30:00 +
categories: [CS, database]
tags : CS DB
---

# database owner

일단 먼저 termproject 내부에서 모든 권한이 다 부여된 user을 하나 생성합니다.
이름을 db2023라고 하겠습니다. password는 db!2023으로 설정하겠습니다.

    ALTER ROLE db2023 NOSUPERUSER CREATEDB CREATEROLE INHERIT LOGIN NOREPLICATION NOBYPASSRLS;

만약 안된다면, super 계정 (postgres)로 로그인 후,
    
    ALTER DATABASE termproject OWNER TO db2023;

를 해보거나, 새롭게 database를 만든 후, 슈퍼 계정으로

    CREATE DATABASE [dbname] OWNER [username] TABLESPACE [tsname] ;

쿼리를 작성해보시길 바랍니다.

## customer

고객은 자신의 개인 정보 열람 및 수정, 품목 정보 열람, wishlist 수정 및 열람 및 추가, 자신의 주문 정보 열람 및 수정 및(환불) 주문 추가, QnA 게시판 열람 및 추가 및 수정만 볼 수 있습니다.

### VIEW 만들기

product view를 만들 수 있습니다. 왜냐하면 product는 3개의 table로 구성이 되어있기 때문입니다.

    CREATE OR REPLACE VIEW public.product_view
        AS SELECT sp.subcode, 
        tp.sub_category,
        tp.top_category,
        tp.product_name,
        tp.product_explain,
        sp.product_size,
        sp.product_color,
        sp.product_price,
        sp.product_count,
        tp.product_seller,
        tp.topcode
    FROM top_product tp
        JOIN code_mapping_table cmt ON tp.topcode = cmt.topcode
        JOIN sub_product sp ON sp.subcode = cmt.subcode;


order review view를 만들 수 있습니다. 주문에 대한 모든 정보를 다 담고 있습니다. 
고객이 좀 더 쉽게 환불할 수 있도록, 사이즈가 크지만 view를 생성했습니다.

    CREATE VIEW order_review_view AS
    SELECT 
        pr.subcode,
        pr.sub_category,
        pr.top_category,
        pr.product_name,
        pr.product_explain,
        pr.product_size,
        pr.product_color,
        pr.product_price,
        pr.product_seller,
        ot.order_code,
        ot.customer_id,
        ot.order_start_time,
        ot.review_point,
        ot.review_content
    FROM product_view pr
    JOIN order_review_table ot ON pr.subcode = ot.product_subcode;

wishlist view도 만들 수 있습니다. 고객이 wishlist에 담은 품목에 대한 정보를 담는 view입니다.
view의 size가 꽤나 커지지만, 매번 4번 join을 하다 보니, 너무 복잡하다는 생각이 들어 그냥 통으로 view를 만들었습니다..

### ROLE 만들기

postgresql에서

    CREATE ROLE customer WITH LOGIN PASSWORD 'customer1';

role을 만든 후,

    GRANT ALL ON TABLE public.order_review_table TO customer;
    GRANT ALL ON TABLE public.qna TO customer;
    GRANT ALL ON TABLE public.wishlist TO customer;
    GRANT ALL ON TABLE public.customer_table TO customer;
    GRANT ALL ON TABLE product_view TO customer;
    GRANT ALL ON TABLE order_review_view TO customer;
    GRANT ALL ON TABLE public.sub_product TO customer;
    GRANT ALL ON TABLE public.top_product TO customer;
    GRANT ALL ON TABLE public.code_mapping_table TO customer;


주문, 리뷰, 장바구니, QnA, 개인 정보에 권한을 부여하였습니다.


## seller 

판매자는 나의 개인 정보와, 판매 물품, 판매 기록, QnA 게시판만 열람할 수 있습니다.
나의 개인 정보와 판매 물품 정보, QnA 게시판 수정만 판매자는 가능합니다.

### ROLE 만들기

postgresql에서

    CREATE ROLE seller WITH LOGIN PASSWORD 'seller1';

role을 만든 후,

    GRANT ALL ON TABLE public.order_review_table TO seller;
    GRANT ALL ON TABLE public.qna TO seller;
    GRANT ALL ON TABLE public.seller_table TO seller;
    GRANT ALL ON TABLE product_view TO seller;
    GRANT ALL ON TABLE order_review_view TO seller;
    GRANT ALL ON TABLE public.sub_product TO seller;
    GRANT ALL ON TABLE public.code_mapping_table TO seller;
    GRANT ALL ON TABLE public.top_product TO seller;

로 품목, 주문, QnA, 개인 정보에 권한을 부여하였습니다.

## administor 

관리자는 모든 정보를 열람하거나 수정할 수 있습니다.

### ROLE 만들기

    CREATE ROLE administor WITH LOGIN PASSWORD 'administor1';

role을 만든 후,

    GRANT ALL ON TABLE public.administor_table TO administor;
    GRANT ALL ON TABLE public.code_mapping_table TO administor;
    GRANT ALL ON TABLE public.wishlist TO administor;
    GRANT ALL ON TABLE public.top_product TO administor;
    GRANT ALL ON TABLE public.sub_product TO administor;
    GRANT ALL ON TABLE public.seller_table TO administor;
    GRANT ALL ON TABLE public.qna TO administor;
    GRANT ALL ON TABLE public.order_review_table TO administor;
    GRANT ALL ON TABLE public.event_table TO administor;
    GRANT ALL ON TABLE public.customer_table TO administor;
    GRANT ALL ON TABLE public.order_review_view TO administor;
    GRANT ALL ON TABLE public.product_view TO administor;

로 모든 권한을 부여하였습니다.

## View를 포함한 Diagram

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/b23845c0-952f-4fd6-9f77-cfa5a05a934e)

최종적으로 이렇게 마무리가 되었습니다. <br>
최대한 깔끔하게 만들어 보려고 했는데, 저보다 더 잘하시는 분들은 더 깔끔하게 구현하실 듯 합니다.

### 마무리하며

table schema를 진짜 여러 번 갈아엎었습니다.. 시험기간인데도..
근데 특히, 4개 join한 테이블을 최대한 view로 만들지 않으려고 했습니다. 공간을 너무 잡아먹다 보니 ..
그러다 보니, 어디서 에러가 나고, 어디서 참조 에러가 계속 나더라고요.
마음 편하게 4개 join한 view를 만들었습니다. <br>
여기까지가 python code를 작성하기 전 사전 단계였고, 본격적으로 다음 글부터, 기능을 python 3.12 버전을 사용해서 구현해보겠습니다.


