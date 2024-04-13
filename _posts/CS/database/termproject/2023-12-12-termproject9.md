---
title: db_termproject(9) - customer 품목 조회 및 구매
date: 2023-12-12 13:00:00 +
categories: [CS, database]
tags : CS DB
---

# python 구현

## 품목 조회 및 구매

품목을 등록했으니, 이제 구매를 해야합니다.

    def buying_item(customer_id):
        global user_con
        print("구매 페이지로 이동합니다.")

        cursor = user_con.cursor()
        user_input = input("품목 조회를 원하시면 1번을 눌러주세요. 뒤로 가기를 그 외 다른 버튼을 눌러주세요 : ")

        if user_input != '1':
            print("메인 페이지로 이동합니다 ..")
        else:
            print("살 수 있는 품목 리스트를 불러옵니다 .. .")
            print("순서대로 재고번호, 상위 카테고리, 하위 카테고리, 상품 이름, 상품 설명, 사이즈, 색상, 1개당 가격, 남아있는 재고량, 판매자 연락처입니다")

            select_query = f"select * from product_view "
            cursor.execute(select_query)
            product_list = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(product_list, columns=columns)

            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

fetchall한 결과를 pandas library를 사용해서 dataframe형태로 변환하고, tabulate library를 사용해서 table형태로 출력하였습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/2f448528-9503-467d-acdb-54a8c285708b)

정상적으로 작동되는 모습을 볼 수가 있습니다.

이제 각 주문을 구분하기 위해서 order_code를 발급하려 합니다.
발급은, product의 subcode와 비슷하게, 만약 코드가 존재하지 않으면 1,000,000,001부터 시작하고,
존재한다면 제일 마지막 +1을 한 order_code를 발급하도록 구현하였습니다.

    select_query = f"select order_code from order_review_table "
    cursor.execute(select_query)
    exists_order_code = cursor.fetchall()
    order_code = 0
    if exists_order_code ==[] :
        order_code = 1000000001
    else:
        order_code = exists_order_code[-1][0] + 1 #제일 마지막 code 발급

구매가 잘 되는 모습을 볼 수가 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/fc5be956-f54f-4c92-a986-4b2465617e50)

이러한 주문 기록은 order_review_table에 저장이 됩니다.
아직까지 review를 남기지 않았으므로, 초기에는 NULL 값으로 저장되어 있는 모습을 알 수가 있습니다.

dbeaver에서 data가 잘 저장됐는지 확인할 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/42fcb989-91ca-4a3b-b51b-9d8a3e36f40f)


![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/111024c2-286e-4581-ba59-ee1fb1677591)

잘 저장됨을 확인할 수 있습니다.


### 마무리하며

물품을 구매했으니, 다음 글에선 내가 샀던 품목 조회에 대해 살펴보겠습니다.
