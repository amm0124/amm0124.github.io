---
title: db_termproject(12) - 이벤트 참여 및 장바구니 사용(1)
date: 2023-12-12 17:00:00 +
categories: [CS, database]
tags : CS DB
---


# python 구현

이번 글에선 이벤트 참여와 장바구니 사용에 대해 알아보도록 하겠습니다.

## 이벤트 참여

사실 이벤트라고 해서 거창한 것은 없습니다. 
customer가 이벤트 참여를 하면 24시간 뒤, administor가 메일을 발송하는 형태로 구현을 했습니다.
맨날 보던 customer_main()에서, 6을 입력한 후, 이벤트 참여 페이지로 이동하겠습니다.

    def event_join(customer_id):
        global user_con
        print("이벤트 참여 페이지입니다!")
        cursor = con.cursor()
        try:
            current_time = datetime.now()
            insert_query = f"INSERT INTO event_table VALUES('{customer_id}', '{current_time}');"
            cursor.execute(insert_query)
            con.commit()
            print("이벤트 참여가 완료됐습니다! ")
        except Exception as e:
            # print(f"Error: {e}")
            print("이미 참여한 회원입니다.")
        print("메인 페이지로 돌아갑니다.")

코드도 너무 간단합니다. event_table은 customer_id를 primary key로 갖고 있기 때문에,
insert에서 오류가 나는 경우는 primary key 중복밖에 없다고 판단했습니다.
따라서 Exception으로, 이벤트 참여 여부를 판단했습니다.

DBeaver에서도 정상적으로 INSERT된 모습을 볼 수 있습니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/18e61434-46a0-415e-a937-38fb194da943)

## 장바구니 사용

문제가 항상 많은 장바구니입니다. 쇼핑몰에서 바로 물건을 사는 방법과, 장바구니에 담은 후, 사는 방법 두 가지가 있습니다.
이전 글에서 보여줬던 품목 구매는 전자에 해당합니다.
wishlist table에 품목들을 담습니다. 이후, 품목 수량 조절 후, 일괄적으로 구매하는 방향으로 구현했습니다.
wishlist 함수 내부에서 while문을 사용해, 장바구니에 계속 담을 수 있게 구현하였습니다.
물품을 담을 때 wishlist 내부에 없다면, Insert query, 이미 담은 물품을 더 담을 땐, UPDATE query를 사용했습니다. 

    def wishlist(customer_id):
        global user_con
        cursor = user_con.cursor()

        print("장바구니에 담기 전, 살 수 있는 품목 리스트를 불러옵니다 .. .")
        print("순서대로 재고번호, 상위 카테고리, 하위 카테고리, 상품 이름, 상품 설명, 사이즈, 색상, 1개당 가격, 남아있는 재고량, 판매자 연락처입니다")
        select_query = f"select * from product_view "
        cursor.execute(select_query)
        product_list = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(product_list, columns=columns)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

        while True :
            type = input("장바구니에 품목을 담고 싶으시면 1번, 장바구니 기능을 그만 사용하고 싶으시면 2번을 눌러주세요 : ").strip()
            if type =='1' :
                try :
                    wish_code = int(input("장바구니에 담고 싶은 재고번호를 입력해주세요 : ").strip())
                    select_query = f"SELECT product_subcode FROM wishlist where customer_id='{customer_id}';"
                    cursor.execute(select_query)
                    my_wishlist_subcodes = cursor.fetchall()
                    if (wish_code, ) in my_wishlist_subcodes :
                        print("장바구니에 품목이 있으므로 수량을 조절합니다.")
                        wish_count = int(input("조절하고 싶은 수량을 입력해주세요 : "))
                        select_query = f"SELECT count FROM wishlist where customer_id='{customer_id}' and product_subcode={wish_code};"
                        cursor.execute(select_query)
                        wishlist_in_count = cursor.fetchall()
                        wishlist_in_count = wishlist_in_count[0][0]
                        
                        if wishlist_in_count + wish_count < 0:
                            print("담은 품목은 0보다 크거나 같아야 합니다.")
                        elif wishlist_in_count + wish_count == 0:
                            print("0이 되었으므로 장바구니에서 삭제합니다")
                            delete_query = f"DELETE FROM wishlist WHERE product_subcode={wish_code} and customer_id ='{customer_id}';"
                            cursor.execute(delete_query)
                        else :
                            update_query= f"UPDATE wishlist SET count = count + {wish_count} WHERE customer_id ='{customer_id}' and product_subcode={wish_code}"
                            cursor.execute(update_query)
                    else :
                        print("장바구니에 품목을 추가합니다")
                        wish_count = int(input("수량을 입력해주세요 : "))
                        if wish_count <= 0 :
                            print("0보다 큰 수를 입력해주세요.")
                        else :
                            select_query = f"INSERT INTO wishlist VALUES('{customer_id}', '{wish_code}', {wish_count});"
                            cursor.execute(select_query)
                    user_con.commit()
                    print("장바구니 수정을 완료했습니다.")
                except Exception as e :
                    print(f"양식에 맞추어 입력해주세요 : {e}")
                    wishlist_continue=input("계속 하기를 원하시면 1번, 장바구니 사용을 종료하길 원하시면 다른 버튼을 눌려주세요 : ").strip()
                    if wishlist_continue!='1':
                        break
                    else :
                        print("다시 장바구니 사용을 시작합니다.")
            else :
                print("장바구니 사용을 종료합니다.")
                print("메인 페이지로 돌아갑니다.")
                return
        print("메인 페이지로 돌아갑니다.")

코드를 실행할 때, 만약 장바구니에 품목이 존재하는 경우, 품목의 수량을 조절했습니다.
장바구니에 있는 품목의 수량이 0이 되면 삭제하는 형태로 구현했습니다.
반대로 말하자면, 장바구니에 품목이 존재하지 않는다면 추가하는 방향으로 구현했습니다.

장바구니에 잘 담기는 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/ebc7031c-dd33-4af5-beed-d5fe1e4fd3f3)

DBeaver에서도 확인해보면

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/c6be5a84-62cd-4acc-bfed-9e4e83c47323)

이랬던 장바구니가, 

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/37d54c2c-708e-4a5e-ba8d-d4dc30ab5502)

잘 담긴 모습을 확인할 수 있었습니다!

이제 장바구니 수량을 조절해보겠습니다.

잘 되는 모습을 확인할 수 있습니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/573f3afd-9907-4508-ad7e-cab63944a4be)

수량도 조절이 잘 되는 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/a838016c-8746-42e1-ba3b-2aa59b0cae45)

장바구니에 있는 품목의 수량을 0으로 만들어보겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/b99d5a43-ca84-4e50-b642-9fd3ea0e9a01)

잘 작동이 되네요.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/a13721b1-9550-433f-bf6f-4d9fb1d847f1)

DBeaver에서도 삭제된 모습을 볼 수 있습니다.


### 마무리하며

이제 장바구니에 품목을 잘 담았습니다.
다음 글에선 장바구니에 잘 담은 품목들을 사는 방법에 대해 알아보겠습니다.