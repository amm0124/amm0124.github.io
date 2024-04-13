---
title: db_termproject(5) - 회원 가입
date: 2023-12-12 00:00:00 +
categories: [CS, database]
tags : CS DB
---

# python 구현

## 들어가기에 앞서..

저는 콘솔로 구현을 했습니다. 콘솔로 구현하려니, 마음에 들지 않더군요.
차라리 django를 사용해서, GUI 기반으로 만들었으면 좋았을 듯 합니다.
후회를 했습니다..
아무튼 시작해보겠습니다.

## 쇼핑몰 인사

일단 제일 먼저, database와 python을 연결하기 위해, psycopg2를 import해야 합니다.

    import psycopg2
    import time
    import getpass
    import smtplib
    from sklearn.neighbors import KNeighborsClassifier
    from email.mime.text import MIMEText
    import sys
    import pandas as pd
    from datetime import datetime
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.metrics import mean_squared_error
    
저는 이러한 모듈을 import 했습니다.

    user_con = None #로그인 한 유저별 connection 할당

    def return_owner_connect():
        con = psycopg2.connect(
            database='termproject',
            user='db2023',
            password='db!2023',
            host='::1',
            port='5432'
        )
        return con


로그인 한 user가 사용할 connection 객체를 전역 변수로 선언하였습니다.
로그인 하기 전 connection 객체는 database의 소유주로 선언하였습니다.

일단 쇼핑몰에 들어가면, 회원 가입을 할 것인지, 기존 ID로 로그인 할 것인지 선택을 해야 합니다.
따라서, main에서 제일 먼저 실행할 welcome이라는 함수를 구현했습니다.

    if __name__ == '__main__':
        welcome()

welcome 함수는 맨 처음 사용자의 입력으로 회원 가입 or 로그인을 할 것인지 결정합니다.
1이면 회원 가입, 2면 로그인, 다른 입력이면 잘못된 입력으로 간주하고 다시 질문을 던집니다.

    def welcome():
        print("************************************************************")
        print("********************쇼핑몰에 오신 것을 환영합니다****************")
        print("************************************************************")
        inp = input("신규 회원이면 1번, 기존 회원이면 2번을 입력해주세요 : ").strip()

        if inp == '1':
            print("회원 가입을 시작합니다.")
            create_account()
        elif inp == '2':
            print("반갑습니다 회원님.")
            print("로그인 페이지로 이동합니다.")
            login()
        else:
            print("[경고] 잘못된 입력입니다. ")
            count = 1
            while True:
                inp = input("신규 회원이면 1번, 기존 회원이면 2번을 입력해주세요 : ").strip()
                print(f"[경고] 남은 횟수 : {5 - count}회 남았습니다. ")
                if inp == '1':
                    print("회원 가입 페이지로 넘어갑니다!")
                    create_account()
                    break
                elif inp == '2':
                    print("반갑습니다 회원님!")
                    login()
                    break
                else:
                    count += 1
                    if count > 5:
                        print("[경고] 5회 초과된 잘못 된 입력을 감지했습니다. 프로그램을 종료합니다.")
                        sys.exit()

## 회원 가입

사용자의 입력에 따라서, 회원 가입 종류를 설정할 수 있습니다.
기존 ID와 중복되면 안되기에, exists_id라는 변수에 type별 ID를 저장한 후, 존재하지 않는다면 INSERT하는 형태로 구현했습니다.

    def create_account():
        con = return_owner_connect()
        cursor = con.cursor()
        exists_id = []
        type = input("일반 회원으로 가입을 원하시면 1번, 판매자로 가입을 원하시면 2번, 관리자로 가입을 원하시면 3번, 프로그램 종료를 원하시면 나머지 버튼을 눌러주세요 : ").strip()
        if type=='1' or type == '2' or type =='3' :
            type=int(type)
            if type == 1:  # customer
                cursor.execute("SELECT customer_id FROM customer_table")
                exists_id = cursor.fetchall()
            elif type == 2:  # seller
                cursor.execute("SELECT seller_id FROM seller_table")
                exists_id = cursor.fetchall()
            else:  # admin
                cursor.execute("SELECT administor_id FROM administor_table")
                exists_id = cursor.fetchall()

            print("회원가입을 위한 ID와 password를 입력해주세요.")
            print("ID는 이메일 형식으로 입력해야 합니다. 이메일 형식으로 입력하지 않을 시, 가입이 제한됩니다.")
            count = 0

            while True:
                id = input("ID : ").strip()
                if '@' not in id:
                    print("[경고] 잘못된 입력입니다. 이메일 형식으로 id를 입력해주세요")
                    print(f"[경고] 남은 횟수 : {5 - count}회 남았습니다. ")
                    count += 1
                    if count == 5:
                        print("[경고] @ 형식을 사용해주세요. 잘못 된 입력 5회 초과로 1분 후 입력 가능합니다.")
                        time.sleep(1000)
                        count = 0
                else:
                    if (id,) in exists_id:
                        print("[경고] 존재하는 id입니다. 재입력해주세요.")
                    else:
                        print("정상적으로 입력받았습니다.")
                        break

            temp_password = input("password : ").strip()
            password = input("다시 비밀번호를 입력해주세요 : ").strip()
            count = 1

            while True:
                if temp_password == password:
                    break
                else:
                    print("[경고] 초기 비밀번호와 동일하게 입력해주세요. ")
                    password = input("다시 비밀번호를 입력해주세요. ").strip()
                    count += 1
                    if count > 3:
                        print("[경고] 비정상적인 가입이 감지되었습니다. 프로그램을 강제종료합니다.")
                        sys.exit()
            print("회원 정보를 데이터베이스에 저장중 ....")

            if type == 1:  # customer
                address_want = input("주소와 키, 몸무게의 입력을 원하시면 1번, 원하지 않는다면 그 외 버튼을 눌러주세요 :  ").strip()
                if address_want == '1':
                    while True:
                        print("주소와, 키(정수), 몸무게(정수)를 입력해주세요 : ")
                        address = input("주소: ").strip()
                        height = input("키 : ").strip()
                        weight = input("몸무게 : ").strip()
                        if height.isdigit() and weight.isdigit():
                            print("정상적으로 입력되었습니다!")
                            break
                        else:
                            print("[경고] 키와 몸무게를 정수 형태로 입력해주세요!")
                    cursor.execute(f"INSERT INTO customer_table VALUES('{id}', '{password}', 0, False ,'{address}' , {height}, {weight});")
                else:
                    cursor.execute(f"INSERT INTO customer_table (customer_id, customer_pw, point, vip) VALUES('{id}', '{password}', 0, False); ")
            elif type == 2:  # seller
                cursor.execute(f"INSERT INTO seller_table (seller_id, seller_pw) VALUES('{id}', '{password}')")
            else:  # admin
                cursor.execute(f"INSERT INTO administor_table (administor_id, administor_pw) VALUES('{id}', '{password}')")

            con.commit()
            print("회원가입 완료!")
            print("시작 페이지로 돌아갑니다!")
            welcome()
        else :
            print("프로그램을 종료합니다.")


성공적으로 잘 되는 모습을 확인할 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/bf9c6625-4b55-4b7a-8eb7-4ab61685c433)


database에도 잘 저장이 되는 모습을 볼 수 있네요.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/ea937564-8fd4-4412-a32e-8015612fde2a)

## 데이터 삽입

기존의 데이터를 다 삭제했습니다.
customer 데이터 삽입. 주소 랜덤 생성기를 사용하였습니다. 대충 데이터를 47개 만들어왔습니다.. 후..

    customer_table INSERT INTO customer_table VALUES 
        ('test1@naver.com', 'test1', 2000, false, '경상북도 의성군 단촌면 구계1길 18-4 37320 한국', 185, 75),
        ('test2@naver.com', 'test2', 2000, false, '경상남도 창원시 마산합포구 어시장7길 62-1(남성동) 51721 한국', 180, 72),
        ('test3@naver.com', 'test3', 2000, false, '충청북도 청주시 서원구 청남로2036번길 67(수곡동) 28709 한국', 170, 72),
        ('test4@naver.com', 'test4', 2000, false, '경상북도 칠곡군 왜관읍 석전로9길 19(삼진주택) 39874 한국', 171, 64),
        ('test5@naver.com', 'test5', 2000, false, '울산광역시 남구 월평로103번길 4(신정동) 44684 한국', 192, 88),
        ('test6@naver.com', 'test6', 2000, false, '경기도 양평군 서종면 무드리2길 13 12500 한국', 180, 72),
        ('test7@naver.com', 'test7', 2000, false, '광주광역시 남구 수박등로12번길 8(월산동) 61651 한국', 150, 38),
        ('test8@naver.com', 'test8', 2000, false, '경상북도 포항시 남구 송림로31번길 21-17(송도동) 37800 한국', 165, 74),
        ('test9@naver.com', 'test9', 2000, false, '부산광역시 연제구 쌍미천로 169-12(연산동) 47551 한국', 165, 54),
        ('test10@naver.com', 'test10', 2000, false, '서울특별시 영등포구 선유로 130(양평동3가) 07255 한국', 152, 39),
        ('test11@naver.com', 'test11', 2000, false, '서울특별시 송파구 백제고분로19길 26-23(잠실동) 05566 한국', 172, 49),
        ('test12@naver.com', 'test12', 2000, false, '경상남도 통영시 도산면 법송상촌길 51 53003 한국', 185, 88),
        ('test13@naver.com', 'test13', 2000, false, '서울특별시 영등포구 선유로 130(양평동3가) 07255 한국', 161, 49),
        ('test14@naver.com', 'test14', 2000, false, '충청남도 홍성군 홍성읍 문화로176번길 29-4 32222 한국', 181, 68),
        ('test15@naver.com', 'test15', 2000, false, '충청남도 천안시 동남구 버들1길 43(원성동) 31132 한국', 192, 100),
        ('test16@naver.com', 'test16', 2000, false, '울산광역시 남구 산업로91번길 23-2(상개동) 44775 한국', 184, 70),
        ('test17@naver.com', 'test17', 2000, false, '경상남도 합천군 삼가면 소오1길 71 50224 한국', 171, 50),
        ('test18@naver.com', 'test18', 1200, false, '서울특별시 강남구 역삼동 123-45 135-789 대한민국', 170, 65),
        ('test19@naver.com', 'test19', 1800, true, '인천광역시 남동구 미아동 678-90 223-456 대한민국', 175, 68),
        ('test20@naver.com', 'test20', 2200, false, '대구광역시 수성구 만촌동 543-21 402-123 대한민국', 190, 80),
        ('test21@naver.com', 'test21', 1600, true, '부산광역시 해운대구 좌동 987-65 612-345 대한민국', 175, 70),
        ('test22@naver.com', 'test22', 1900, false, '광주광역시 서구 화정동 234-56 567-890 대한민국', 180, 75),
        ('test23@naver.com', 'test23', 1400, true, '대전광역시 중구 대흥동 876-54 321-654 대한민국', 185, 78),
        ('test24@naver.com', 'test24', 2000, false, '울산광역시 남구 삼산동 789-01 987-654 대한민국', 170, 65),
        ('test25@naver.com', 'test25', 1700, true, '세종특별자치시 도담동 321-09 123-987 대한민국', 175, 70),
        ('test26@naver.com', 'test26', 1300, false, '경기도 수원시 장안구 영화동 567-89 234-567 대한민국', 190, 82),
        ('test27@naver.com', 'test27', 2100, true, '강원도 강릉시 연곡면 신림리 543-21 876-543 대한민국', 175, 68),
        ('test28@naver.com', 'test28', 1500, false, '충청북도 청주시 흥덕구 복대동 876-54 321-765 대한민국', 180, 75),
        ('test29@naver.com', 'test29', 1800, true, '충청남도 천안시 서북구 봉명동 234-56 876-543 대한민국', 185, 77),
        ('test30@naver.com', 'test30', 2000, false, '전라북도 전주시 완산구 서신동 321-09 123-876 대한민국', 170, 64),
        ('test31@naver.com', 'test31', 1600, true, '전라남도 목포시 대한누리로 789-01 234-567 대한민국', 175, 68),
        ('test32@naver.com', 'test32', 1900, false, '제주특별자치도 제주시 아라동 987-65 876-543 대한민국', 180, 72),
        ('test33@naver.com', 'test33', 1400, true, '경기도 용인시 수지구 성복동 876-54 321-654 대한민국', 185, 75),
        ('test34@naver.com', 'test34', 2200, false, '서울특별시 강동구 상일동 543-21 654-321 대한민국', 190, 80),
        ('test35@naver.com', 'test35', 1700, true, '인천광역시 서구 가좌동 234-56 432-109 대한민국', 175, 70),
        ('test36@naver.com', 'test36', 1300, false, '대구광역시 달서구 두류동 876-54 567-890 대한민국', 180, 74),
        ('test37@naver.com', 'test37', 1900, true, '부산광역시 동래구 명장동 321-09 109-876 대한민국', 185, 77),
        ('test38@naver.com', 'test38', 1600, false, '경기도 성남시 분당구 정자동 123-45 456-789 대한민국', 155, 45),
        ('test39@naver.com', 'test39', 1400, true, '서울특별시 종로구 인사동 678-90 987-654 대한민국', 170, 55),
        ('test40@naver.com', 'test40', 1800, false, '부산광역시 부산진구 부전동 543-21 321-987 대한민국', 160, 50),
        ('test41@naver.com', 'test41', 1600, true, '인천광역시 연수구 송도동 987-65 654-321 대한민국', 165, 48),
        ('test42@naver.com', 'test42', 1500, false, '대전광역시 유성구 봉명동 876-54 789-012 대한민국', 175, 60),
        ('test43@naver.com', 'test43', 1700, true, '경상북도 포항시 북구 죽도동 321-09 234-567 대한민국', 150, 42),
        ('test44@naver.com', 'test44', 1900, false, '대구광역시 수성구 만촌동 765-43 567-890 대한민국', 168, 56),
        ('test45@naver.com', 'test45', 1400, true, '전라남도 여수시 중동 890-12 432-109 대한민국', 162, 46),
        ('test46@naver.com', 'test46', 1800, false, '경기도 안양시 동안구 관양동 456-78 654-321 대한민국', 158, 44),
        ('test47@naver.com', 'test47', 1600, true, '강원도 강릉시 연곡면 신림리 543-21 876-543 대한민국', 170, 58);


seller 데이터 삽입.

    INSERT INTO seller_table (seller_id, seller_pw)
        VALUES 
        ('seller1@naver.com', 'seller1'),
        ('seller2@naver.com', 'seller2'),
        ('seller3@naver.com', 'seller3'),
        ('seller4@naver.com', 'seller4'),
        ('seller5@naver.com', 'seller5'),
        ('seller6@naver.com', 'seller6'),
        ('seller7@naver.com', 'seller7'),
        ('seller8@naver.com', 'seller8'),
        ('seller9@naver.com', 'seller9'),
        ('seller10@naver.com', 'seller10');



administor 데이터 삽입.

    INSERT INTO administor_table VALUES
        ('admin1@naver.com', 'admin1'),
        ('admin2@naver.com', 'admin2'),
        ('admin3@naver.com', 'admin3');


### 마무리하며

회원 가입이 완료된 후, 로그인을 해야 합니다.
글이 너무 길어지다 보니, 다음 글에서 로그인에 대해 설명하겠습니다.