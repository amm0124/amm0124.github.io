---
title: db_termproject(8) - seller 로그인 및 품목 등록
date: 2023-12-12 11:00:00 +
categories: [Database, termproject]
---

# python 구현

## seller 품목 등록

customer가 품목을 구매 하려면, seller가 품목을 등록해야지 살 수 있습니다.
따라서, seller로 로그인 후, 품목을 등록하는 과정을 살펴보겠습니다.
일단 seller로 로그인을 했으므로, seller connection을 만들어 줍니다.

    def print_seller_main_page():
        print("--------판매자 메인 페이지입니다!---------")
        print("1번을 누르면 품목을 추가할 수 있습니다.")
        print("2번을 누르면 품목을 수정할 수 있습니다.")
        print("3번을 누르면 QnA 게시판으로 이동할 수 있습니다.")
        print("4번을 누르면 물품 판매에 대한 정보 조회 및 집계 가능합니다.")
        print("5번을 누르면 정보 수정을 할 수 있습니다.")
        print("그 외를 누르면 프로그램을 종료합니다.")

    def seller_main(seller_id):

        global user_con
        user_con = psycopg2.connect(
            database='termproject',
            user='seller',
            password='seller1',
            host='::1',
            port='5432'
        )
        print(f"{seller_id}님 반갑습니다.")
        print_seller_main_page()

        user_input = (input("입력 : "))
        if user_input == '1':  # 품목 추가
            add_product(seller_id)
        elif user_input == '2': # 품목 수정
            fix_product_info(seller_id)
        elif user_input == '3': # QnA 답변
            qna_answer(seller_id)
        elif user_input == '4': # 등록 상품 조회 및 집계
            check_my_product(seller_id)
        elif user_input == '5': # 개인 정보 수정
            fix_my_account(seller_id, 2)
        else: #종료
            print("프로그램을 종료합니다.")
            sys.exit()
        seller_main(seller_id)


품목을 등록해야 하니, 1번을 눌러 품목을 등록하러 가보겠습니다.

    def add_product(seller_id):
        cursor = user_con.cursor()
        choice = (input("품목 입고 페이지입니다. 정보 입력을 원하시면 1번, 원하지 않고 메인 페이지로 돌아가기를 원하시면 1을 제외한 버튼을 눌러주세요 : "))
        if choice == "1":
            print("상위 카테고리, 하위 카테고리, 상품 이름, 상품 설명을 입력해주세요 :")
            top_category = input("상위 카테고리 : ").strip()
            sub_category = input("하위 카테고리 : ").strip()
            product_name = input("상품 이름 : ").strip()
            product_explain = input("상품 설명 : ").strip()
            try:
                print("top_category_code를 발급중입니다 . .. ")
                cursor.execute("BEGIN;")
                cursor.execute("SELECT topcode FROM top_product")
                top_product_code = cursor.fetchall()
                """#if top_product_code == [] :
                #    top_product_code =1
                #else :"""
                top_product_code = int(top_product_code[-1][0]) + 1  # 제일 마지막 정수 형태 반환

                insert_query = f"INSERT INTO top_product VALUES ( {(top_product_code)}, '{top_category}' ,'{sub_category}' , '{product_name}' ,'{product_explain}' , '{seller_id}');"
                cursor.execute(insert_query)
                print("1차 데이터 삽입 완료. ")

                print("sub_category_code를 발급중입니다 . .. ")
                cursor.execute("SELECT subcode FROM code_mapping_table")
                subcode = cursor.fetchall()
                subcode_int = int(subcode[-1][0]) + 1
                insert_query = f"INSERT INTO code_mapping_table VALUES ( {subcode_int}, {top_product_code} );"
                cursor.execute(insert_query)
                print("code mapping 완료. ")

                print("제품 사이즈, 컬러, 가격, 수량을 입력해주세요. : ")

                product_size = input("제품 사이즈 (S,M,L,XL로 구분해서 입력해주세요) : ").strip()
                product_color = input("제품 색상 : ").strip()
                product_price = int(input("제품 가격 : ").strip())
                product_count = int(input("제품 수량 : ").strip())

                insert_query = f"INSERT INTO sub_product VALUES ({subcode_int} , '{product_size}' , '{product_color}' , {product_price}, {product_count} );"
                print(insert_query)
                cursor.execute(insert_query)
                print("2차 데이터 삽입 완료.")

                cursor.execute("COMMIT;")
                print("데이터 삽입 완료!")
            except Exception as e:
                # 예외 발생 시 롤백
                print(f"에러 : {e}")
                cursor.execute("ROLLBACK;")
        else:
            print("판매자 메인 페이지로 돌아갑니다.")

    ![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/8d912d5b-17a2-4c57-9dc6-2683cb9aaec0)

    indexerror가 나는데 이유는, 지금 아무런 상품이 등록되어 있지 않기 때문입니다.
    제일 마지막 row의 code +1을 발급해주는데 현재, 아무런 row가 없는 상태기 때문입니다.
    따라서, 이 부분을

        """#if top_product_code == [] :
        #    top_product_code =1
        #else :"""
        top_product_code = int(top_product_code[-1][0]) + 1  # 제일 마지막 정수 형태 반환

형태로 수정하겠습니다.

    if top_product_code == [] :
        top_product_code =1
    else :
        top_product_code = int(top_product_code[-1][0]) + 1  # 제일 마지막 정수 형태 반환

subcode도 마찬가지입니다.
topcode와 겹치는건 별로니, 2023000001을 초기 코드로 설정하였습니다.
완성된 최종 코드를 첨부하겠습니다.
또한 저렇게 코드를 사용하면, 상위 product에 subcode가 묶이는 것이 아닌 그냥 1:1 mapping이 됩니다.
따라서 코드를 수정해야 합니다.

    def add_product(seller_id):
        cursor = user_con.cursor()
        choice = (input("품목 입고 페이지입니다. 정보 입력을 원하시면 1번, 원하지 않고 메인 페이지로 돌아가기를 원하시면 1을 제외한 버튼을 눌러주세요 : "))
        if choice == "1":
            flag = input("상위 제품군을 입력하고 싶으시면 1번, 바로 하위 품목을 등록하고 싶으시면 다른 버튼을 눌러주세요 : ").strip()
            if flag =='1' :
                print("상위 카테고리, 하위 카테고리, 상품 이름, 상품 설명을 입력해주세요 :")
                top_category = input("상위 카테고리 : ").strip()
                sub_category = input("하위 카테고리 : ").strip()
                product_name = input("상품 이름 : ").strip()
                product_explain = input("상품 설명 : ").strip()
                try:
                    print("top_category_code를 발급중입니다 . .. ")
                    cursor.execute("BEGIN;")
                    cursor.execute("SELECT topcode FROM top_product")
                    top_product_code = cursor.fetchall()

                    if top_product_code == [] :
                        top_product_code =1
                    else :
                        top_product_code = int(top_product_code[-1][0]) + 1  # 제일 마지막 정수 형태 반환

                    insert_query = f"INSERT INTO top_product VALUES ( {(top_product_code)}, '{top_category}' ,'{sub_category}' , '{product_name}' ,'{product_explain}' , '{seller_id}');"
                    cursor.execute(insert_query)
                    print("상위 데이터 삽입 완료. ")
                    user_con.commit()
                except Exception as e:
                    # 예외 발생 시 롤백
                    print(f"에러 : {e}")
                    cursor.execute("ROLLBACK;")
                    print("메인 페이지로 돌아갑니다.")
                    return

            print("하위 품목을 등록합니다 .. ")
            print("sub_category_code를 발급중입니다 . .. ")
            cursor.execute("SELECT subcode FROM code_mapping_table")
            subcode = cursor.fetchall()
            if subcode ==[] :
                subcode=2023000001
            else :
                subcode = int(subcode[-1][0]) + 1

            top_product_code=int(input("존재하는 제품군의 상위 코드를 입력해주세요 : ").strip())
            select_query = f"select topcode from top_product"
            cursor.execute(select_query)
            exists_topcode = cursor.fetchall()

            if (top_product_code, ) in exists_topcode :
                try :
                    cursor.execute("BEGIN;")
                    insert_query = f"INSERT INTO code_mapping_table VALUES ( {subcode}, {top_product_code} );"
                    cursor.execute(insert_query)
                    print("code mapping 완료. ")

                    print("제품 사이즈, 컬러, 가격, 수량을 입력해주세요. : ")

                    product_size = input("제품 사이즈 (S,M,L,XL로 구분해서 입력해주세요) : ").strip()
                    product_color = input("제품 색상 : ").strip()
                    product_price = int(input("제품 가격 : ").strip())
                    product_count = int(input("제품 수량 : ").strip())

                    insert_query = f"INSERT INTO sub_product VALUES ({subcode} , '{product_size}' , '{product_color}' , {product_price}, {product_count} );"
                    print(insert_query)
                    cursor.execute(insert_query)
                    print("2차 데이터 삽입 완료.")

                    cursor.execute("COMMIT;")
                    print("데이터 삽입 완료!")
                except Exception as e:
                    # 예외 발생 시 롤백
                    print(f"에러 : {e}")
                    cursor.execute("ROLLBACK;")
                    print("메인 페이지로 돌아갑니다.")
                    return
        else:
            print("판매자 메인 페이지로 돌아갑니다.")


그리고 품목 발급시, 동시에 여러 사람이 발급을 하면 code가 겹치는 상태가 발생할 수 있기에,
transaction 처리를 해주었습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/66dfd9e3-da58-4da6-b4e6-a7e4379e5926)

정상적으로 삽입되는 모습을 볼 수가 있습니다.

top product

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/9040d061-ea84-402e-b610-1a496fc371e0)

code mapping table

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/cbb237ec-b0e7-407c-89c5-654a9d4e9477)

sub product

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/ce204042-7c20-4876-92ce-f7db85d1c894)

view에도 정상적으로 삽입되는 모습을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/fb0a8532-8a8f-4507-940f-fefc9cd8e5cc)


### 마무리하며

다음 글에선 고객이 품목을 조회하고, 구매하는 방법을 살펴보겠습니다.

