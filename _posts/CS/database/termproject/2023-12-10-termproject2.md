---
title: db_termproject(2) - product
date: 2023-12-10 00:10:00 +
categories: [CS, database]
tags : CS DB
---


# 판매 상품 구현    

## 항상 시행착오가 생기는 법입니다.

제일 많은 시간이 걸린 상품 테이블입니다. 

맨 처음엔 각 상품을 구분하는데 product_code, product_size, product_color, product_seller 즉 4개의 column을 기반으로 구현하려고 했습니다.

#### 왜?
'같은 제품군이라면 같은 product_code를 갖는다' 라는 아이디어 기반으로 사이즈 추천 시스템을 생각을 했습니다. <br>
예를 들자면 어떤 A라는 회사에서 나온 후드티가 있다고 가정해보겠습니다. 이 제품은 색상, 사이즈, 판매자에 관계없이 모두 같은 product_code를 갖는다고 가정합니다. <br>
이 후드티의 product_code는 0123456789 라고 가정해보겠습니다. 색은 회색, 사이즈는 XL ,  A 판매자여도 이 후드티의 product_code는 0123456789를 가질 것이고, 검은색, S 사이즈, B 판매자여도 후드티의 product_code는 0123456789를 가질 것입니다.  <br>
customer는 product를 살 때, 이러한 4개의 column을 (feature, attribute도 똑같은 표현입니다) 다 고려해야 한다고 생각했습니다. 따라서 4개의 column을 primary key로 설정하고. 이 4개의 column을 다른 table에서도 foreign key로 사용하게 구현했습니다.  (foreign key constraint를 만족해야 하니까요.)
 

![termproject2](https://github.com/amm0124/amm0124.github.io/assets/108533909/f5ee4be0-4b2c-4a25-b5d9-5fdfe976db86)


또한 하나의 product_code는 같은 상위(top_category), 하위(bottom_category.. 이는 나중에 sub_category로 이름이 바뀝니다.) 카테고리, 상품 이름 (product_name)을 가질테니, product_details라는 table을 만들어서, product_code를 primary key로 갖고, product_info table이 foreign key로 사용하도록 구현했습니다.  product_details에 product_count는 무시해주세요.
 
#### 여기서 생기는 문제
하지만 상품을 구분하는데 4개의 column을 사용한다면, 상품을 참조하는 다른 table에서 너무 많은 공간을 소모합니다. 상단의 사진을 보면 충분할 것 같습니다.
order_table, qna_table은 사실 4개의 column을 foreign key로 사용할 필요가 전혀 없습니다.<br>
왤까요? customer_review table이나 shopping_cart table (나중에 wishlist라는 이름으로 바뀝니다. 아무래도 wishlist가 더 맞는 표현인 듯 합니다)이야 뭐 판매자, 옷 색상, 사이즈 다 고려할 필요가 있지만 order_table이나, qna_table은 딱히 알 필요가 없지 않나요? 알면 좋겠지만 저는 굳이라는 생각을 했습니다.<br>
또 다른 문제가 있습니다. seller 상품을 추가할 때, product_code를 검사해야 합니다. 
이유는 3가지가 있습니다.
1. 내가 등록하고자 하는 상품이 있는 것인가? 판매자는 그냥 등록을 하는 것이 아닌, 이미 있는 상품인가? 찾아봐야 합니다. 이게 저장하고 있는 data row가 많아지면 판매자는 귀찮아지는거죠. 검색하면 되잖아! 라고 대답할 수가 있는데, 요즘 쇼핑몰을 예시로 들어봅시다. <br>똑같은 상품인데, 판매자에 따라 이름이 너무 다릅니다. 당장 쿠팡에 "나이키 맨투맨"만 검색해도 똑같은 맨투맨이 판매자만 다르게 수십가지씩 나옵니다.  판매자는 일일이 다 찾아보고.. 오 이거 겹치니까 똑같은 product_code를 사용해야 하네.. 그럼 또 product_code 찾아보고 똑같이 입력하고.. 이는 문제가 있는거죠.
2. "아니 이름을 같게 하면 되잖아!!" 라고 반문 가능한데, 이게 두 번째 이유입니다. 모든 판매자들이 상품 이름을 다 외울 수가 없으니까요. 상품 판매자들은 직접 만들어서 팔 수도 있고, 다른 브랜드에서 납품받아서 팔 수도 있습니다. 자기 브랜드야 뭐 그러려니 하겠다만, 다른 브랜드에서 받아오는 상품들은 다 알지 못하기 때문이지요.
3.  그렇다면 "브랜드에서 나오는 재고번호를 찾아서, 그거 기준으로 등록하면 안될까?" 대답은 안됩니다. 만약 유명 브랜드가 아닌 개인이 파는 상품을 납품받아 판다면 어떻게 할까요? 이러한 상품들은 보통 개별 재고번호가 부여되지 않는다고 합니다. 그럼 "납품받는 사람이 product_code를 등록하면 안될까?" 질문이 생기는데 이 질문은 1번으로 다시 가게 되는 것이죠. 또 판매자는 찾아봐야 합니다. <br>탈출 조건이 없는 재귀함수에 빠지는 케이스가 생겼네요. 따라서 이렇게 column을 4개 사용하면 용량이 커질 뿐 아니라, 특정한 edge case에서 문제가 생깁니다. 이 이유 덕에, 새로 다 고쳤습니다.. 자동화 잘 되어있는 시대에 이러한 쇼핑몰을 열면 폐업은 시간문제지 않을까요?

## 해결은 어떻게 할래?

그래서 생각한 해결책이 같은 제품군이면 같은 product_code를 갖는다는 생각을 갖다 버리자는 것입니다. 같은 제품에서 색상이 다르다면, 원래는 같은 product_code를 갖지만, 이제 다르다고 생각을 해보자는 것입니다. 판매자들도 다르다면 그냥 다른 product_code를 갖는다고 생각해보자는 것입니다.  
즉,  사이즈, 색상 등 다 관계없이 그냥 개별 물품에 대해 독보적인 product_code를 가져보자. 그리고 이러한 product_code에 대해 상위 product_code를 가져서 묶자. 
상위 product_code가 같으면 상품의 details(top_category, sub_category, 제품 이름 등등)들은 다 같을 테니까요. "4개의 column이 아닌, product_code라는 하나의 column을 가지고 다른 table도 다 참조하도록 구현을 다시 해보자!"라는 것이 주된 아이디어입니다.

**즉, 다시 말하자면 각 개별 물품에 대해서 하위 product_code를 부여하고, 이를 primary key로 사용하자. 그리고 상위 product_code로 묶자. 그러면 공간도 덜 소모할 것이고 깔끔할 것이다.** 

라는 것이 개선된 아이디어입니다. 
1개의 column을 primary key로 사용한다면 foreign key constraint도 훨씬 보기 좋게 만족할 뿐 아니라, 공간도 덜 소모하게 될 것이니까요. 

## 구현은 어떻게 할 것인데?

위 조건에 맞춰서 table들을 새로 구현했습니다.
아래 코드는 product와 관련된 table들에 대한 query입니다.
당연 postgresql 기준 작성되었습니다.
일단 table을 만드는 query를 보고, 부가적인 설명을 더 하겠습니다.

### query code

[product_top] 생성 쿼리

    create TABLE top_product(
        topcode int primary key,
        top_category VARCHAR,
        sub_category VARCHAR,
        product_name VARCHAR,
        product_explain VARCHAR,
        product_seller VARCHAR, 
        FOREIGN KEY (product_seller) REFERENCES seller_table (seller_id) ON DELETE CASCADE ON UPDATE CASCADE
    );

seller_table에서 seller_id가 UPDATE되면 자동으로 UPDATE가 되어야 합니다.
seller_table에서 seller_id가 삭제된다면, 그와 연결된 row들도 삭제되어야 합니다.
즉 top_product_code도 삭제가 되어야 합니다.

[code_product_mapping] 생성 쿼리

    CREATE TABLE code_mapping_table (
        subcode INT,
        topcode INT,
        FOREIGN KEY (topcode) REFERENCES top_product (topcode) ON DELETE CASCADE ON UPDATE CASCADE
    );

topcode는 product_details의 top_product_code를 foreign key로 갖습니다.
product_details의 top_product_code가 변경되면 자동으로 topcode도 UPDATE가 되어야 합니다.
topcode가 삭제된다면, 즉 seller가 탈퇴하는 경우나 topcode를 직접적으로 삭제하는 경우, 그와 연결된 subcode들도 자동으로 삭제되어야 합니다.
상위 코드가 없거나, 판매자 없는 물품은 존재하면 안되니까요.


[product_table] 생성 쿼리

    CREATE TABLE sub_product (
        subcode int PRIMARY KEY,
        product_size VARCHAR CHECK (product_size IN ('S', 'M', 'L', 'XL')),
        product_color VARCHAR,
        product_price INT,
        product_count INT,
        FOREIGN KEY (subcode) REFERENCES code_mapping_table (subcode) ON DELETE CASCADE ON UPDATE CASCADE
    );

code_mapping_table의 subcode가 변경되거나 삭제가 된다면 code_mapping_table에 따라서 움직여야 합니다.

### 설명

맨 처음 판매자는, product_details에 등록하고자 하는 제품군의 detail data를 먼저 insert해야 합니다.
이후, 하위 코드를 발급받습니다. 
code_mapping_table에 있는 subcode의 제일 큰 값보다 하나 더 큰 값을 발급받는다고 생각하면 될 듯 합니다. <br>
하위 코드를 발급 받을 때, transaction은 Serializable로 설정하였습니다.
어차피 품목 등록은 좀 천천히 해도 되는 작업이니까요.
발급받은 하위 코드를 기반으로 product_table에 정보를 입력합니다.

subcode, topcode, seller가 삭제 되더라도 ON DELETE CASCADE 조건으로 모두 잘 지워짐을 확인할 수 있습니다.

이만 product table에 대한 글을 마무리하겠습니다.<br>

### 마무리하며

약간의 고해성사 및 성찰을 해보겠습니다. <br>
이번 학기, 솔직히 번아웃이 심하게 왔습니다. 데이터베이스 시간은 꼬박꼬박 출석 했지만, 안 간 수업도 엄청 많습니다.
출석 F 받기 직전까지 안 간 수업도 있고요. <br>
뭐 이유야, 좌측 네비게이터 탭의 About.me를 읽어보신 분은 아시겠지만, 저는 전과생입니다.
그 덕에 다른 학생들보다 늦었다는 강박에 시달리면서 수업도 계절도 꽉꽉 채워들었습니다. <br>
학과에서 이론 위주의 수업들은 이러한 강박에 더 시달리게 저를 만들었습니다. <br>
아, 다른 학생들은 뭐 외주도 맡던데, 뭐 개발도 하던데 .. 하지만 나는 수업만 듣네 .. <br>
수업만 듣는데, 양은 왜이렇게 많은지 . . 과제는 뭐 이리 많은지 .. 뭐 이러한 생각들로 번아웃이 온 듯 합니다.<br>
중간고사도 번아웃 와서 제대로 공부 안하고 말아먹은 과목도 있거든요 ...<br>
그런 의미에서 이번 프로젝트가 저한테 꽤 의미가 있는 프로젝트입니다.
맨날 학과 수업만 듣다가 처음으로 제 스스로 해보는 프로젝트기 때문입니다. <br>
하지만 수업 제대로 안 듣고, 제 멋대로 데이터베이스 스키마 짜고, 이러다가 몇 번씩 고치고.. 시간도 없는데 바빠 죽겠습니다.<br>
대충 해서 내도 되지만, 뭔가 이번 텀프로젝트는 제대로 해보고 싶은 생각이 들어요. <br>
왜냐면 처음으로 제 스스로 해보는 "무엇"이기 때문입니다. <br>
누군가가 보면 "3학년이 이정도는 뭐 간단하게.. 별 기능도 없네"라고 할 수 있습니다. <br>
이번 텀프, 기능은 부족하지만 제 나름대로 열심히, 최대한 완성도 높게 해보려고 합니다.<br>
왜냐면 처음으로 스스로 해보는 개발이니까요.<br>
아무튼 긴 글 읽어주셔서 감사합니다.<br>
다음 글에선, 쇼핑몰에서의 주문, 고객 리뷰, QnA, 장바구니 table에 대해 글을 작성하겠습니다.<br>
