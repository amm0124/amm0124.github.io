---
title: db_termproject(7) - customer 메인 페이지 및 포인트 충전 및 계정 수정
date: 2023-12-12 03:03:00 +
categories: [CS, database]
tags : CS DB
---

# python 구현


## 로그인 후 메인 페이지

customer로 로그인을 했습니다.
customer를 제일 먼저 반기는, customer_main 함수를 살펴보겠습니다.
로그인 했으므로, user_con 객체에 새로운 connection을 부여합니다.
코드가 실행되고 나면, customer의 메인 페이지에서 어떤 작업을 할 수 있는지 안내문을 출력해주는
print_customer_main_page() 함수가 작동합니다.

    def print_customer_main_page():
        print("--------회원 메인 페이지입니다!---------")
        print("1번을 누르면 포인트를 충전할 수 있습니다.")
        print("2번을 누르면 주문 조회 및 환불 및 리뷰 등록을 할 수 있습니다.")
        print("3번을 누르면 개인 정보를 수정할 수 있습니다.")
        print("4번을 누르면 품목 구매를 할 수 있습니다.")  # 장바구니 , 여기서 추천 시스템, 리뷰 조회 가능
        print("5번을 누르면 QnA 게시판으로 이동합니다.")
        print("6번을 누르면 이벤트 참여를 할 수 있습니다.")
        print("7번을 누르면 리뷰 등록을 할 수 있습니다.")
        print("그 외를 누르면 프로그램을 종료합니다.")

    def customer_main(customer_info):  
        # ('test1@naver.com', 'test1', 102000, False, '경상북도 의성군 단촌면 구계1길 18-4 37320 한국', 185, 75,0)
        global user_con

        user_con = psycopg2.connect(
                database='termproject',
                user='customer',
                password='customer1',
                host='::1',
                port='5432'
            )
        cursor= user_con.cursor()
        customer_id = customer_info[0]
        vip = customer_info[3]
        cursor.execute(f"select point from customer_table where customer_id = '{customer_id}';")
        point = cursor.fetchall()
        point = point[0][0]
        print_customer_main_page()

        cursor.execute("select * from administor_table");
        aa = cursor.fetchall()
        print(aa)

        if vip:
            print(f"안녕하십니까. {customer_id} 회원님. 현재 회원님은 VIP 회원입니다. ")
        else:
            print(f"안녕하십니까. {customer_id} 회원님. 현재 회원님은 일반 회원입니다. ")
        print(f"고객님의 현재 포인트는 {point}입니다.")



![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/735d0855-bdf4-468a-bfa9-d4898bc70ee4)

성공적으로 연결이 잘 되는 모습을 볼 수 있네요.

    cursor.execute("select * from administor_table");
    aa = cursor.fetchall()
    print(aa)

아까 권한을 주지 않았던 administor_table에 대한 접근을 시도해보려고 합니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/ea44e1f0-cdf0-49a2-b8a0-e29dd8c8c063)

접근이 되지 않는 모습을 볼 수 있습니다! 좋네요 

다시 customer_main으로 돌아가서,
각 입력에 대해서, 기능을 연결해주는 함수로 연결해줍니다.
다시 메인 페이지로 돌아오도록 재귀적으로 구현하였습니다.

    #customer_main 아랫 부분

    user_input = input("입력 : ").strip()

    if user_input == '1':  # 포인트 충전
        charging_point(customer_id)  # id 넘겨줌
    elif user_input == '2':  # 주문 조회 및 환불 및 리뷰
        buying_item_lookup(customer_id)
    elif user_input == '3':  # 개인 정보 수정 및 탈퇴
        fix_my_account(customer_id, 1)  # id를 매개변수로 넘겨줌, type == 1 -> 고객으로 encoding
    elif user_input == '4':  # 품목 구매 (장바구니 ,추천 시스템)
        buying_item(customer_id)
    elif user_input == '5':  # QNA게시판
        QnA(customer_id)
    elif user_input == '6':  # 이벤트 참여
        event_join(customer_id)
    elif user_input == '7':  # 리뷰 등록
        evaluation_item(customer_id)
    else:
        print("프로그램을 종료합니다.")
        sys.exit()
    customer_main(customer_info)


## 포인트 충전

일단 먼저, 결제를 하기 위한 포인트를 충전해야 합니다.
제가 뭐 다른 결제 API를 받아와서 해볼까도 생각도 했지만 그렇게 되면 너무 복잡해지더라고요..
약간 아쉬움이 남습니다. 다른 프로젝트 할 때, 결제 API도 사용해 보도록 하겠습니다.
아무튼 포인트를 충전하는 함수 charging_point(customer_id)에 대해 살펴보도록 하겠습니다.

    def charging_point(customer_id):
        global user_con
        print("포인트 충전 페이지입니다!")

        while True:
            want_charging_point = input("충전하고 싶은 포인트를 입력하세요 : ")
            if want_charging_point.isdigit():
                break
            else:
                print("잘못된 입력입니다. 정수형으로 입력하세요. ")

        want_charging_point = int(want_charging_point)

        cursor = user_con.cursor()
        update_query = f"UPDATE customer_table SET point = point + {want_charging_point} WHERE customer_id = '{customer_id}';"
        cursor.execute(update_query)
        user_con.commit()
        print("포인트 충전 완료! 메인 페이지로 이동합니다.")

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/76de9750-9097-4b7b-8464-9f213042f76f)

포인트 충전이 잘 되는 모습을 볼 수 있습니다.

## 회원 정보 수정

회원 정보 수정하는 fix_my_account(user_id, type) 함수를 살펴보겠습니다.
이 함수는 작동하는 로직이 다 비슷해서, type이 1이면 customer, 2면 seller, 3이면 administor 정보 수정하는 함수로 작성했습니다.

    def fix_my_account(user_id, type):
    global user_con
    if type == 1:  # 고객 정보 수정
        print("고객 정보 수정 페이지입니다!")
        print("1번을 누르면 ID 수정입니다.")
        print("2번을 누르면 비밀번호 수정입니다.")
        print("3번을 누르면 주소 수정입니다.")
        print("4번을 누르면 키를 수정합니다.")
        print("5번을 누르면 몸무게를 수정합니다.")
        print("6번을 누르면 회원 탈퇴를 진행합니다.")
        print("7번을 누르면 고객 메인 페이지로 이동합니다.")
        print("그 외 버튼을 누르면 프로그램을 종료합니다.")
        count = 0
        user_input = input("입력 : ").strip()
        cursor = user_con.cursor()
        if user_input == '1':  # 아이디 변경
            while True:
                cursor.execute("SELECT customer_id FROM customer_table")
                exists_customer_id = cursor.fetchall()
                update_id = input("변경을 원하는 ID를 입력하세요 : ").strip()
                if '@' not in update_id:
                    print("[경고] 잘못된 입력입니다. 이메일 형식으로 id를 입력해주세요")
                    print(f"[경고] 남은 횟수 : {5 - count}회 남았습니다. ")
                    count += 1
                    if count == 5:
                        print("[경고] 잘못 된 입력 5회 초과로 시스템을 종료합니다.")
                        sys.exit()
                else:  # @ 포함
                    if (update_id,) in exists_customer_id:
                        print("[경고] 존재하는 id입니다. 재입력해주세요.")
                    else:
                        print("정상적으로 입력받았습니다.")
                        break

            update_query = f"UPDATE customer_table SET customer_id = '{update_id}' WHERE customer_id = '{user_id}';"
            cursor.execute(update_query)
            con.commit()
            print(f"고객 ID를 {update_id}로 수정했습니다!")
            print("고객 메인 페이지로 이동합니다.")
        elif user_input == 2:  # 비밀번호 변경
            update_password = input("업데이트 하고 싶은 비밀번호를 입력하세요 : ")
            update_query = f"UPDATE customer_table SET customer_pw = '{update_password}' WHERE customer_id = '{user_id}';"
            cursor.execute(update_query)
            con.commit()
            print("비밀번호 변경 완료했습니다!")
            print("고객 메인 페이지로 이동합니다.")
        elif user_input == 3:  # 주소 변경
            update_address = input("변경하고자 하는 주소를 입력해주세요 : ")
            update_query = f"UPDATE customer_table SET customer_address = '{update_address}' WHERE customer_id = '{user_id}';"
            cursor.execute(update_query)
            con.commit()
            print("주소를 성공적으로 변경했습니다!")
            print("고객 메인 페이지로 이동합니다.")
        elif user_input == 4:  # 키 변경
            update_height = input("변경하고자 하는 키를 입력해주세요 : ")
            update_query = f"UPDATE customer_table SET customer_address = {update_height} WHERE customer_id = '{user_id}';"
            cursor.execute(update_query)
            con.commit()
            print("키를 성공적으로 변경했습니다!")
            print("고객 메인 페이지로 이동합니다.")
        elif user_input == 5:  # 몸무게 변경
            update_weight = input("변경하고자 하는 몸무게를 입력해주세요 : ")
            update_query = f"UPDATE customer_table SET customer_address = {update_weight} WHERE customer_id = '{user_id}';"
            cursor.execute(update_query)
            con.commit()
            print("몸무게를 성공적으로 변경했습니다!")
            print("고객 메인 페이지로 이동합니다.")
        elif user_input == 6:
            print("회원 탈퇴를 진행합니다. ")
            withdraw = input("정말 탈퇴를 원하시면 1번, 메인 페이지로 돌아가기를 원하시면 2번을 입력해주세요 : ").strip()

            if withdraw == "1":
                print("회원 탈퇴를 진행합니다.")
                print("고객님의 정보는 삭제되지만, 고객님의 주문과, 리뷰는 ID가 가려진 채 남습니다. ")
                try:
                    delete_query = f"DELETE FROM CUSTOMER_TABLE WHERE customer_id='{user_id}' ;"
                    cursor.execute(delete_query)
                    con.commit()
                    print("탈퇴를 완료하였습니다..... 프로그램을 종료합니다.")
                    sys.exit()
                except Exception as e:
                    print(f"error 발생 : {e}")
                    print("프로그램을 종료합니다.")
                    sys.exit()
            else:
                print("고객 메인 페이지로 돌아갑니다")
        elif user_input == 7:
            print("고객 메인 페이지로 이동합니다.")
        else:
            print("프로그램을 종료합니다.")
            sys.exit()

test2@naver.com ID를 test100@naver.com으로 수정해보도록 하겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/359a90c3-d6ab-4ecc-a5ad-6b3b46ab704f)

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/f02b42e2-f31a-4a50-86b9-05d8c2ecbe3c)

잘 반영이 됐습니다.


test4@naver.com 삭제를 한 번 해보도록 하겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/1e8047a6-d43b-4844-b744-ce77cc009868)

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/e7c6119e-e711-4b47-8244-0ef79a24b685)

회원 탈퇴가 잘 되는 모습을 볼 수 있습니다.
    
### 마무리하며

품목 구매 및 조회 기능를 하려면, 판매자의 품목 등록이 먼저입니다.
따라서 다음 글에선 seller 품목 등록도 살펴 보겠습니다.
밤이 깊어서 집에 가야할 듯 합니다..