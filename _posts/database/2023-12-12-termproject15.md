---
title: db_termproject(15) - seller 기능 구현
date: 2023-12-12 16:00:00 +
categories: [Database, termproject]
---

# python 구현

## 품목 수정

판매자가 품목을 수정할 수 있어야 합니다.
설명이나 수량 등 그런 것들 말이죠.
맨 처음 product_view를 만들었습니다. 이를 통해서 수정을 하도록 하겠습니다.

    def fix_product_info(seller_id):
        user_input = input("품목 정보 수정을 원하시면 1번, 원하지 않고 메인 페이지로 돌아가기를 원하시면 나머지 버튼을 눌러주세요 : ")
        if user_input == '1':
            print("내가 등록한 품목을 불러옵니다.")
            cursor = user_con.cursor()

            select_query=f"select * from product_view WHERE product_seller='{seller_id}';"
            cursor.execute(select_query)
            my_product_info = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(my_product_info, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

            try :
                seller_input = input("제품 상위 코드 수정을 원하시면 1번, 바로 하위 제품을 수정하고 싶으시면 다른 버튼을 눌러주세요 : ").strip()
                if seller_input != "1":
                    print("하위 제품 수정 페이지로 이동합니다!")
                else:
                    print("상위 제품군 수정을 시작합니다.")
                    topcode = int(input("수정하고 싶은 상위 제품군 코드번호를 입력해주세요 : ").strip())
                    print(f"수정을 원하는 상위 제품군 코드번호는 {topcode}입니다.")

                    print("수정 시작합니다.")

                    top_category = input("상위 카테고리 : ").strip()
                    sub_category = input("하위 카테고리 : ").strip()
                    product_name = input("상품 이름 : ").strip()
                    product_explain = input("상품 설면 : ").strip()

                    update_query = f"UPDATE top_product SET top_category='{top_category}' , sub_category ='{sub_category}', product_name='{product_name}', product_explain='{product_explain}' WHERE topcode={topcode};"
                    cursor.execute(update_query)
                    user_con.commit()
                    print("상위 제품군 수정을 완료하였습니다!")

                    want_fix_sub_product_flag = input("하위 제품 수정을 원하시면 1번을 눌러주세요 : ")

                    if want_fix_sub_product_flag != '1':
                        print("수정을 완료했습니다. 메인 페이지로 돌아갑니다.")
                        return

                print("하위 제품 수정을 시작합니다!")
                print("내가 등록한 하위 제품을 불러옵니다.")

                fix_want_sub_product = input("수정하고 싶은 하위 제품 코드를 입력해주세요 : ")
                print(f"수정을 원하는 하위 제품 코드번호는 {fix_want_sub_product}입니다.")

                print("수정 시작합니다.")

                size = input("사이즈 (S,M,L,XL)중 입력하세요: ").strip()
                color = input("색상 : ").strip()
                price = int(input("가격 : ").strip())
                amount = int(input("재고량 : ").strip())

                print("수정 시작합니다..")
                update_query = f"UPDATE sub_product SET product_size='{size}', product_color='{color}', product_price={price}, product_count={amount} WHERE subcode={fix_want_sub_product}"
                cursor.execute(update_query)
                user_con.commit()
                print("하위 제품 수정 완료됐습니다!")
                print("메인으로 돌아갑니다.")
            except Exception as e:
                print(f"에러 발생 : {e}, 양식에 맞추어 입력해주세요.")
                print("메인으로 돌아갑니다.")
                return




일단 잘 됩니다.
topcode가 차례로 2,3입니다. 짤려 있네요.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/7acce194-2611-49f9-be4d-84b08815992d)

상위 제품군을 수정해보겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/1f3d54c4-eb37-4264-b163-9e907114e0e5)

오리털 롱패딩이라는 제품 명이, 오리털 완충 롱패딩으로 잘 변경됨을 볼 수 있습니다. 그와중에 20년이나 입다니 대단하네요..

하위 제품 바뀌기 전 DBeaver입니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/07bb6a7a-4733-494e-90c7-a4b6d4a80e98)

잘 실행이 되는 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/d9309a75-0ddc-4df4-a1eb-73d8e742fc0f)

바뀌기 전 DBeaver 모습입니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/c5f29b62-bc8e-4422-b8c2-c3490594c2ee)

실행 완료 후, DBeaver 모습입니다. 100만원짜리 맨투맨이라.. 명품인가 봅니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/d5599d62-7aca-452f-8a12-8b1067ca3fdf)



## 판매자 총 판매 집계 금액

판매자가 얼만큼 팔았는지, 어떤 품목을 팔았는지 당연히 볼 수 있어야 합니다.
따라서 order_review_table에서 간단한 집계를 통해서 얼만큼 팔았는지 볼 수 있습니다.

    def check_my_product(seller_id):
        user_input = input("내가 등록했던 품목 정보 열람을 원하시면 1번, 원하지 않고 메인 페이지로 돌아가기를 원하시면 1을 제외한 버튼을 눌러주세요 : ")
        cursor = user_con.cursor()
        print("정보 조회를 시작합니다")
        print("판매했던 정보를 불러옵니다 ...")
        select_query = f"select * FROM order_review_table WHERE seller_id ='{seller_id}';"
        cursor.execute(select_query)
        my_sell_product = cursor.fetchall()
        print("주문번호, 판매자 이름, 재고번호, 수량, 1개당 가격, 구매한 사람 , 고객 결제 날짜, 리뷰 포인트, 사용자 키, 사용자 몸무게 순으로 보여집니다.")
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(my_sell_product, columns=columns)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))


        print("총 판매 금액 집계중입니다 ... ")
        select_query = f"select seller_id, sum(count*price_per_1) FROM order_review_table WHERE seller_id='{seller_id}' GROUP BY seller_id; "
        cursor.execute(select_query)
        my_aggregation = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(my_aggregation, columns=columns)
        print("총 판매 금액")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        print("메인 페이지로 돌아갑니다.")

딱히 data들을 수정하지 않고 조회만 하면 되기에 간단합니다.

아까 입력했던 데이터에 대해서 집계가 잘 되는 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/ac43719b-4caa-42ec-a656-6b759922692f)

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/0a77e2a8-6e45-4354-b0c1-940d71fb3895)

### 마무리하며

판매자 QnA 질문 답변을 마지막으로, 판매자의 기능도 마무리하도록 하겠습니다.