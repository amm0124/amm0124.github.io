---
title: db_termproject(13) - 장바구니 사용(2)
date: 2023-12-12 19:00:00 +
categories: [CS, database]
tags : CS DB
---

# python 구현

이전 글을 참조하세요!

이번 글에선 장바구니에 담았던 품목들을 사는 방법에 대해 알아보겠습니다.

## 장바구니 구매

우선 기존의 buying_item() 함수는 사용자의 입력에 따라서, 바로 품목을 구매 할 것인지, 메인 페이지로 넘어갈 것인지 결정했습니다. 2개의 분기가 아닌, 장바구니에 있는 품목을 입력에 따라서 바로 살 수 있는 기능을 구현하겠습니다. 

    user_input = input("바로 구매를 원하시면 1번, 장바구니에 있는 물건 구매를 원하시면 2번, 뒤로 가기를 그 외 다른 버튼을 눌러주세요 : ") 
    
    """
    code
    ...
    ...

    """
    elif user_input==2 :
        #implement ....

본격적으로 구현을 시작해보겠습니다.

    elif user_input=='2' :
        print("장바구니에 있는 품목 구매를 시작하겠습니다.")
        print("장바구니에 있는 품목을 불러옵니다 .. .")
        select_query = f"SELECT * FROM wishlist WHERE customer_id='{customer_id}' ;"
        cursor.execute(select_query)
        wishlists = cursor.fetchall() #(customer_id, subcode, count)
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(wishlists, columns=columns)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

        print("장바구니에 있는 품목을 구매하겠습니다..")
        point_query = f"select point from customer_table where customer_id = '{customer_id}';"
        cursor.execute(point_query)
        remain_point = cursor.fetchall()
        remain_point = remain_point[0][0]
        print(f"현재 고객님의 남아있는 잔고는 {remain_point}입니다.")
        wishlist_total_price = 0

        for item in wishlists :
            subcode = item[1]
            select_query = f"select product_price FROM product_view WHERE subcode = {subcode} "
            cursor.execute(select_query)
            price_per_1 = cursor.fetchall()
            price_per_1 = price_per_1[0][0]
            wishlist_total_price += price_per_1*item[2]
        after_remain_point = remain_point - wishlist_total_price

        if after_remain_point < 0 :
            print("포인트가 부족합니다. 장바구니의 수량을 조절하거나, 포인트를 충전해주세요 .")
            print("메인으로 돌아갑니다.")
            return

        print("결제를 시작합니다...")
        try:
            # 등업 및 결제
            cursor.execute("BEGIN;")
            use_money_query = f"select acc_use_money from customer_table where customer_id = '{customer_id}';"
            cursor.execute(use_money_query)
            acc_use_money = cursor.fetchall()
            acc_use_money = acc_use_money[0][0]

            if acc_use_money + wishlist_total_price >= 1000000:
                print("축하합니다! VIP 회원으로 등급업 됐습니다.")
                update_query = f"UPDATE customer_table SET point = {after_remain_point + 3000}, acc_use_money = acc_use_money + {wishlist_total_price}, vip = true;"
            else:  # 적립금
                update_query = f"UPDATE customer_table SET point = {after_remain_point + 1000}, acc_use_money = acc_use_money + {wishlist_total_price};"
            cursor.execute(update_query)
            print("포인트 출금 완료 .. ")

            # order_review_table에 정보 남기기 -> order code 발급하기
            # wishlist에 있는 품목에 한해서 ..

            for item in wishlists :
                subcode = item[1]
                count = item[2]
                select_query = f"select product_price FROM product_view WHERE subcode = {subcode} "
                cursor.execute(select_query)
                price_per_1 = cursor.fetchall()
                price_per_1 = price_per_1[0][0]

                print("주문번호 발급중입니다 ..")
                select_query = f"select order_code from order_review_table "
                cursor.execute(select_query)
                exists_order_code = cursor.fetchall()
                order_code = 0
                if exists_order_code == []:
                    order_code = 1000000001
                else:
                    order_code = exists_order_code[-1][0] + 1
                current_time = datetime.now()

                select_query = f"select product_seller FROM product_view Where subcode={subcode}"
                cursor.execute(select_query)
                seller_id = cursor.fetchall()
                seller_id = seller_id[0][0]
                insert_query = f"insert into order_review_table VALUES({order_code},'{seller_id}', {subcode} ,{count}, {price_per_1}, '{customer_id}', '{current_time}') ; "
                cursor.execute(insert_query)

                update_query = f"UPDATE sub_product SET product_count = product_count - {count} Where subcode ={subcode}"
                cursor.execute(update_query)

            print("구매 완료!")
            user_con.commit()
        except Exception as e:
            # 예외 발생 시 롤백
            cursor.execute("ROLLBACK;")
            print(f"트랜잭션 롤백: {e}")


엄청난 스파게티 코드가 된 것 같습니다.. 일단 장바구니에 있는 품목을 들고온 후, 총 장바구니에 있는 품목들의 가격을 계산합니다. 만약 현재 보유하고 있는 포인트보다 더 많이 있다면, 구매를 종료하도록 구현하였습니다.
만약 금액이 많거나, 같다면 결제가 가능합니다. 이 때, 장바구니에 있는 품목들을 for문으로 돌면서, order_review_table에 기록을 하였습니다. 또한, 결제 후 당연히 품목의 수량은 줄어들어야 합니다.
지금 와서 후회하는 것은, wishlist table에 seller_id를 같이 기록했으면 품목의 subcode로 select query를 작성하지 않았어도 됐을 텐데 말입니다.

아무쪼록 결과를 보겠습니다.
실행하자마자 성공해서 기분이 좋았습니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/0ae660a6-8e90-44e2-aed6-fdc97d47e980)

DBeaver에서도
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/bc6d6819-d29b-4f6a-9320-81ac907c7c91)
였었던 구매 기록이,

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/1aca69f5-0f5f-4698-9655-14632c9ccfc5)
잘 갱신된 것을 확인할 수 있었습니다!


### 마무리하며

길고 긴 customer의 기능이 드디어 끝납니다.
이번 글에선 장바구니 결제에 대해서 알아보았고, 다음은 사용자 리뷰 별점을 토대로, 품목의 추천 사이즈를 알아보는 시간을 갖도록 하겠습니다.
