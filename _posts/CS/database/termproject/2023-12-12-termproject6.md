---
title: db_termproject(6) - 로그인
date: 2023-12-12 00:00:05 +
categories: [CS, database]
tags : CS DB
---

# python 구현

저번 글에서 회원 가입 구현까지 했습니다.
이제 로그인을 할 차례입니다.
    
## 로그인

로그인 하기 위해서, 입력을 받고, 그 입력이 각자 사용자의 table에 존재한다면 쇼핑몰의 기능을 사용할 수 있게 구현하였습니다. 로그인 횟수가 5회가 넘어가면 비정상적인 접근으로 간주하고 프로그램을 종료하였습니다.
이러한 디테일이 또 중요한 것 아니겠습니까..

customer_main(customer_info) 함수는 로그인 한 고객의 정보를 넘겨 받는 함수입니다.
이후 여기서 고객은 물건 사기 등등을 할 수가 있습니다. 
옆에 주석을 본다면, 어떤 형태로 매개변수를 사용 중인지 알 수 있습니다.

seller_main(seller_id) 함수는 seller를 식별하는데 seller_id만 존재하므로, seller_id를 매개변수로 받아서,
품목 등록, 수정 등등의 기능을 사용할 수 있습니다.

administor(administor_id) 함수도 seller 함수와 유사합니다.

    def login():
        type = input(("고객으로 로그인하시려면 1번, 판매자로 로그인하시려면 2번, 관리자로 로그인 하시려면 3번, 프로그램을 종료하시려면 그 외 입력을 해주세요. ")).strip()
        count = 0
        con = return_owner_connect()
        cursor = con.cursor()

        if type == '1':  # customer
            print("고객 로그인!")
            cursor.execute("select customer_id, customer_pw from customer_table")
            id_pw_pair = cursor.fetchall()
            print("[공지] 로그인을 하기 위한 ID와 password를 입력해주세요. ")
            id = input("ID: ").strip()
            password = input("password : ").strip()
            while True:
                if (id, password) in id_pw_pair:
                    print("************로그인 성공**********")
                    print("고객 메인 페이지로 넘어갑니다!")
                    break
                else:
                    if count == 5:
                        print("[경고] 비정상적인 로그인 접근입니다. 프로그램을 종료하겠습니다.")
                        sys.exit()
                    else:
                        print("[경고] 존재하지 않는 회원입니다.")
                        print(f"[경고] 남은 횟수 : {5 - count}회 남았습니다. ")
                        id = input("ID: ")
                        password = input("password : ")
                        count += 1
            cursor.execute(f"SELECT * FROM customer_table WHERE customer_id='{id}'")  # postgresql에서 query where '' 문자열
            customer_information = cursor.fetchall()  # [('test1@naver.com', 'test1', 102000, False, '경상북도 의성군 단촌면 구계1길 18-4 37320 한국', 185, 75)]
            customer_main(customer_information[0])  # ('test1@naver.com', 'test1', 102000, False, '경상북도 의성군 단촌면 구계1길 18-4 37320 한국', 185, 75)
        elif type == '2':  # seller
            print("판매자 로그인!")
            cursor.execute("select seller_id, seller_pw from seller_table")
            id_pw_pair = cursor.fetchall()
            print("[공지] 로그인을 하기 위한 ID와 password를 입력해주세요")
            id = input("ID: ")
            password = input("password : ")
            while True:
                if (id, password) in id_pw_pair:
                    print("************로그인 성공**********")
                    print("판매자 메인 페이지로 넘어갑니다!")
                    break
                else:
                    if count == 5:
                        print("[경고] 비정상적인 로그인 접근입니다. 프로그램을 종료하겠습니다.")
                        sys.exit()
                    else:
                        print("[경고] 존재하지 않는 회원입니다.")
                        print(f"[경고] 남은 횟수 : {5 - count}회 남았습니다. ")
                        id = input("ID: ")
                        password = input("password : ")
                        count += 1
            seller_main(id)
        elif type == '3':
            print("관리자 로그인!")
            cursor.execute("select administor_id, administor_pw from administor_table")
            id_pw_pair = cursor.fetchall()
            print("[공지] 로그인을 하기 위한 ID와 password를 입력해주세요")
            id = input("ID: ")
            # password = getpass.getpass("Enter your password: ")
            password = input("password : ")
            while True:
                if (id, password) in id_pw_pair:
                    print("************로그인 성공**********")
                    print("판매자 메인 페이지로 넘어갑니다!")
                    break
                else:
                    if count == 5:
                        print("[경고] 비정상적인 로그인 접근입니다. 프로그램을 종료하겠습니다.")
                        sys.exit()
                    else:
                        print("[경고] 존재하지 않는 회원입니다.")
                        print(f"[경고] 남은 횟수 : {5 - count}회 남았습니다. ")
                        id = input("ID: ")
                        password = input("password : ")
                        count += 1

            administor_main(id)
        else:
            print("프로그램을 종료하겠습니다!")
            sys.exit()

아까 customer_table에 삽입했던 데이터 test1@naver.com, test1의 ID로 로그인을 해보겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/21f78b0d-c171-445d-aa17-f268089fcd70)

잘 작동하는 모습을 볼 수 있습니다.

customer말고 seller로도 로그인 해보겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/aaf33d2e-4ad7-4e3e-85a2-017876773700)

잘 되네요~

### 마무리하며

이제 회원가입, 로그인 기능까지 끝냈습니다.
다음부턴 고객의 기능에 대해 알아보도록 하겠습니다.