---
title: db_termproject(11) - customer QnA 및 review
date: 2023-12-12 15:00:00 +
categories: [Database, termproject]
---

# python 구현

지금까지 물건 구매와 품목 조회, 환불에 대해 살펴봤습니다.
이번 글에선 QnA 게시판에 질문 올리기, 리뷰 남기는 방법을 살펴보겠습니다.

## QnA 게시판

맨날 보던 customer_main에서 5번을 입력해서 QnA 게시판으로 갑니다.

    elif user_input == '5':  # QNA게시판
        QnA(customer_id)


QnA(customer_id) 내부를 살펴보겠습니다.

    def QnA(customer_id):
        global user_con
        cursor = user_con.cursor()

        q_input = input("QnA 질문을 보고 싶으시면 1번, 질문을 남기고 싶으시면 2번, 메인 페이지로 돌아가고 싶으시면 그 외 다른 버튼을 눌러주세요 : ").strip()
        if q_input=='1' :
            print("QnA 게시판을 불러옵니다 ..")
            select_query = f"select qna_num, product_subcode, question, answer from qna;"
            cursor.execute(select_query)
            product_list = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(product_list, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

        elif q_input=='2':
            print("살 수 있는 품목 리스트를 불러옵니다 .. .")
            print("순서대로 재고번호, 상위 카테고리, 하위 카테고리, 상품 이름, 상품 설명, 사이즈, 색상, 1개당 가격, 남아있는 재고량, 판매자 연락처입니다")

            select_query = f"select * from product_view "
            cursor.execute(select_query)
            product_list = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(product_list, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
            try :
                product_subcode = input("품목 재고번호를 입력해주세요 : ").strip()
                question = input("남기고 싶은 질문을 입력해주세요 : ").strip()
                select_query = f"SELECT product_seller FROM product_view WHERE subcode = {product_subcode}"
                cursor.execute(select_query)
                seller_id = cursor.fetchall()
                seller_id = seller_id[0][0]

                select_query = f"select qna_num from qna; "
                cursor.execute(select_query)
                qna_num_list = cursor.fetchall()
                qna_num = 0
                if qna_num_list == []:
                    qna_num = 1
                else:
                    qna_num= qna_num_list[-1][0] + 1

                insert_query = f"INSERT INTO qna VALUES ('{customer_id}' , {product_subcode} , '{question}' ,'{seller_id}' ,'', {qna_num});"
                cursor.execute(insert_query)
                user_con.commit()
                print("QnA 질문 등록이 완료됐습니다.")

            except Exception as e:
                print(f"error : {e}")
                print("잘못 입력했습니다.")
            else :
                pass
        print("메인 페이지로 돌아갑니다.")


QnA 게시판 보기를 살펴보겠습니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/b000ac2f-d137-44c4-8854-529ca8a10506)
answer가 빈 모습을 보니, 아직 답변을 하지 않았습니다.

질문을 해보도록 하겠습니다. tabulate로 재고를 출력하고, 테이블에 insert하는 작업입니다.





![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/923c5d06-80dd-436d-8c79-b5306e3f9bb6)

DBeaver에서 질문 남기기 전 data입니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/b03e432f-174b-4c4d-b54c-65694d6df40f)


작동 후, 

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/c60bcc69-3bd4-4bac-a447-a9dcd2b57bb7)

잘 등록이 되는 모습을 볼 수 있습니다.




## 리뷰 남기기 및 조회

리뷰 남기기도 QnA와 비슷합니다.
먼저, 자신이 구매한 품목을 불러온 후, 해당하는 order_code에 리뷰를 남기면 됩니다. <br>
리뷰를 보는 방법은, 상품 별 재고번호를 입력하면, 리뷰를 불러오는 형식으로 구현할 수 있습니다.
1번을 누르면 리뷰 등록, 2번을 누르면 리뷰 조회하는 형태로 구현했습니다.


    def review(customer_id):
        global user_con
        cursor = user_con.cursor()
        type = input("리뷰 등록을 하시려면 1번, 리뷰 조회를 원하시면 2번, 메인 페이지로 돌아가기를 원하시면 3번을 눌러주세요 : ").strip()

        if type=='1':
            print("구매 내역을 조회입니다.")
            cursor = user_con.cursor()
            select_query = f"select * from order_review_table where customer_id='{customer_id}' ; "
            cursor.execute(select_query)
            my_buying_product = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(my_buying_product, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
            try :
                print("리뷰 등록을 시작합니다.")
                review_order_code = int(input("리뷰를 남기고 싶은 주문번호를 입력해주세요 : ").strip())
                review_point = input("별점입니다. 1~10 사이 정수를 입력해주세요  : ").strip()
                review_point = int(review_point)
                review_content = input("리뷰 내용을 입력해주세요 : ").strip()
                user_height = 0
                user_weight = 0
                flag = input(f"사용한 user의 키와 몸무게를 {customer_id}님의 키와 몸무게로 사용하시려면 1번, 직접 입력을 원하시면 그 외 버튼을 눌러주세요 : ")
                if flag=='1' :
                    select_query = f"SELECT height, weight FROM customer_table WHERE customer_id='{customer_id}'"
                    cursor.execute(select_query)
                    infor = cursor.fetchall()
                    user_height = infor[0][0]
                    user_weight = infor[0][1]
                    print(user_height, user_weight)
                else :
                    user_height = int(input("사용자의 키를 정수 형태로 입력해주세요 : ").strip())
                    user_weight = int(input("사용자의 몸무게를 정수 형태로 입력해주세요 : ").strip())

                update_query =f"UPDATE order_review_table SET review_point = {review_point}, review_content = '{review_content}',user_height ={user_height}, user_weight={user_weight} WHERE order_code={review_order_code}"
                cursor.execute(update_query)
                print("리뷰를 성공적으로 등록했습니다.")
                user_con.commit()
            except Exception as e:
                print(f"양식을 갖춰서 입력해주세요 : {e}")
                print("메인으로 돌아갑니다.")
                return
        elif type=='2':
            print("살 수 있는 품목 리스트를 불러옵니다 .. .")
            print("순서대로 재고번호, 상위 카테고리, 하위 카테고리, 상품 이름, 상품 설명, 사이즈, 색상, 1개당 가격, 남아있는 재고량, 판매자 연락처입니다")
            select_query = f"select * from product_view "
            cursor.execute(select_query)
            product_list = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(product_list, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
            try:
                want_review_code = input("리뷰를 보고싶은 품목의 재고번호를 입력해주세요 : ").strip()
                want_review_code = int(want_review_code)
                print("리뷰 조회를 시작합니다.")
                select_query = f"SELECT review_point, review_content FROM order_review_table WHERE product_subcode ={want_review_code} ;"
                cursor.execute(select_query)
                review_list = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                df = pd.DataFrame(review_list, columns=columns)
                print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
                user_con.commit()
            except Exception as e:
                print(f"양식을 갖춰서 입력해주세요 : {e}")
                print("메인으로 돌아갑니다.")
                return
        else :
            print("메인 페이지로 돌아갑니다.")


리뷰가 등록이 되는 것을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/21b249c9-2f56-4195-911e-43876be69ee4)

DBeaver에서도 확인을 해봅시다.<br>
DBeaver 리뷰 남기기 전
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/d343224f-6506-430c-8503-aee8c1fc56e3)

DBeaver 리뷰 남긴 후
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/e71b8546-01c9-49ee-b9b3-f48aba71bbcc)

잘 되어서 좋네요.
pycharm console이랑 살짝 다른데, 실행은 잘 되니, 걱정 안하셔도 됩니다!

리뷰 조회를 해보겠습니다.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/32836c7e-8317-4841-b32f-32a883e766be)
아까 등록했던 리뷰를 볼 수 있습니다.

### 마무리하며

길고 길었던 customer의 기능이 막바지에 이르렀습니다.
다음 글에선 장바구니 기능과, 이벤트 참여, 사이즈 추천에 대해 알아보겠습니다.




