---
title: db_termproject(9) - customer 품목 조회 및 구매
date: 2023-12-12 11:40:00 +
categories: [Database, termproject]
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


order code 발급해야함