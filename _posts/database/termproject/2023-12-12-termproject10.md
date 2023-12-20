---
title: db_termproject(10) - customer 주문했던 품목 조회 및 환불
date: 2023-12-12 14:00:00 +
categories: [Database, termproject]
---

# python 구현

품목을 구매했으니, 내가 샀던 품목이 잘 order_review_table에 저장되었는지, 조회하는 방법을 알아보겠습니다.
환불은 구매 후 정확히 7일 이후가 되면, 환불하지 못하는 방식으로 구현하였습니다.

## 구매했던 품목 조회

customer_main에서, 2를 입력 후, 내가 샀던 품목 조회 및 환불하는 함수 buying_item_lookup(customer_id)를 살펴보겠습니다.

    #customer_main
    elif user_input == '2':  # 주문 조회 및 환불 
        buying_item_lookup(customer_id)

2를 입력했습니다.

    def buying_item_lookup(customer_id):
        global user_con
        print("구매 내역 조회입니다.")
        cursor = user_con.cursor()
        select_query = f"select * from order_review_view where customer_id='{customer_id}' ; "
        cursor.execute(select_query)
        my_buying_product = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(my_buying_product, columns=columns)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

tabulate library를 사용해서 dataframe 형태로 출력하였습니다.
select_query에서 where에서 condition을 넣어, 자신의 구매 목록을 조회할 수 있도록 하였습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/1bc29869-7607-4622-ab1d-37596b6bab2b)

잘 되고 있군요. 죠습니다.


## 품목 환불

이후 입력에 따라서, 환불을 할 수 있는지, 아닌지 선택합니다.
환불은 현재 시간을 datetime library에 객체를 선언 후, 
order_review_table에 있는 order_start_time 값과 비교해서 7일 이상이면 환불이 불가능, 아니면 가능한 형태로 구현하였습니다. 당연 구매했던 수량보다 많으면 환불 불가능입니다.


    customer_input = input("환불하고자 하는 품목이 있으시다면 1번, 메인 페이지로 돌아가기를 원하신다면 그 외 다른 버튼을 입력해주세요 : ").strip()
    if customer_input == "1":
        print("환불을 시작합니다.")
        want_refund_product_order_code = input("환불하고자 하는 품목의 주문 번호를 입력해주세요 : ").strip()
        want_refund_product_count = (input("환불하고자 하는 품목의 수량을 정확하게 입력해주세요 : ")).strip()

        try:
            cursor.execute("BEGIN; ")
            current_time = datetime.now(timezone.utc)
            select_query = f"SELECT order_start_time, count, price_per_1 FROM order_review_table WHERE order_code={want_refund_product_order_code} ;"
            cursor.execute(select_query)
            order_information = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(order_information, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

            order_start_time = order_information[0][0].replace(tzinfo=timezone.utc)
            order_product_count = order_information[0][1]
            one_per_price = order_information[0][2]
            remain_time = order_start_time - current_time
            enable_refund = remain_time.days < 7 #왜 True?
            want_refund_product_count = int(want_refund_product_count)

            if want_refund_product_count > order_product_count:
                print("주문했던 수량보다 더 많은 입력입니다.")
                print("메인 페이지로 돌아갑니다.")
                return
            else:
                if enable_refund:
                    print("환불을 시작합니다 ..")
                    update_query = f"UPDATE order_review_table SET count = count - {want_refund_product_count} WHERE order_code = {want_refund_product_order_code};"
                    cursor.execute(update_query)
                    print("구매 기록 변경 완료 ..")
                    update_query = f"UPDATE customer_table SET point = point + {one_per_price * want_refund_product_count} where customer_id ='{customer_id}';"
                    cursor.execute(update_query)
                    print("금액 추가 완료..")
                    update_query = f"UPDATE customer_table SET acc_use_money = acc_use_money -  {one_per_price * want_refund_product_count} where customer_id ='{customer_id}';"
                    cursor.execute(update_query)
                    print("누적 금액 차감 완료..")
                    select_query= f"SELECT acc_use_money FROM customer_table WHERE customer_id ='{customer_id}';"
                    cursor.execute(select_query)
                    acc_money = cursor.fetchall()

                    update_query = f"UPDATE sub_product SET product_count = product_count + {want_refund_product_count} Where subcode= {subcode}"
                    cursor.execute(update_query)
        

                    if acc_money[0][0]<10000000 :
                        update_query = f"UPDATE customer_table SET vip = False where customer_id ='{customer_id}';"
                        cursor.execute(update_query)

                    user_con.commit()
                    print("환불이 완료되었습니다.")
                else:
                    print("일주일 이상 시간이 지나서 환불 불가능입니다.")
                    print("메인 페이지로 돌아갑니다.")
                    return

        except Exception as e:
            cursor.execute("ROLLBACK;")
            print(f"error 발생 : {e}")
            print("잘못 입력되었습니다.")


환불 하기 전 DBeaver에 저장된 data입니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/cd0a7b0c-3193-47d9-9da2-d8cd13108769)

많이 환불하려니 불가능한 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/ccb9e430-2adc-406a-a122-37cf03567b55)

2개를 환불하니 정상적으로 환불이 된 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/f98c5c31-4324-4ed7-b2ea-15a5b8792e0e)


### 마무리하며

다음 글에선 review와 QnA 기능을 살펴보겠습니다.

