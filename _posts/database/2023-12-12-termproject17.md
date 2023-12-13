---
title: db_termproject(17) - administor 
date: 2023-12-13 16:00:00 +
categories: [Database, termproject]
---

# python 구현

관리자는 별 기능이 없습니다.
seller까진 기능이 존재했더라면, 관리자는 이벤트 당첨 메일 발송 및, 정보 열람정도 있다고 할 수 있습니다.

## 관리자

처음에 입력을 통해서 각 기능을 수행할 수 있습니다. connection 객체는, adminsitor role에 대해서 설정하였습니다.
또한 프로그램 종료를 누르기 전 까지, 재귀적으로 기능을 수행할 수 있도록 구현하였습니다.

    def print_administor_main_page():
        print("--------관리자 메인 페이지입니다!---------")
        print("1번을 누르면 판매 집계 정보를 열람할 수 있습니다.")
        print("2번을 누르면 당첨자 메일 발송을 할 수 있습니다.")
        print("3번을 누르면 개인 정보를 수정할 수 있습니다.")
        print("그 외를 누르면 프로그램을 종료합니다.")

    def administor_main(administor_id):
        global user_con

        user_con = psycopg2.connect(
            database='termproject',
            user='administor',
            password='administor1',
            host='::1',
            port='5432'
        )

        print(f"안녕하세요. {administor_id} 관리자님")
        print_administor_main_page()

        type= input("입력 : ").strip()
        if type=="1":
            aggregation_product(administor_id)
        elif type=='2' :
            candidate_send_mail(administor_id)
        elif type=='3' :
            fix_my_account(administor_id, '3')
        else :
            print("프로그램 종료")
            sys.exit()
        administor_main(administor_id)


## 모든 판매 정보 열람

seller 판매기록 열람 함수와 매우 비슷합니다.
seller 판매기록 열람 함수에서, select query의 where 조건을 삭제한다면, 모든 데이터를 불러올 수 있습니다.


    def aggregation_product(administor_id):
        global user_con
        print("총 품목 집계를 시작합니다 . .")
        cursor = user_con.cursor()
        print("정보 조회를 시작합니다")
        print("판매했던 정보를 불러옵니다 ...")
        select_query = f"select * FROM order_review_table;"
        cursor.execute(select_query)
        my_sell_product = cursor.fetchall()
        print("주문번호, 판매자 이름, 재고번호, 수량, 1개당 가격, 구매한 사람 , 고객 결제 날짜, 리뷰 포인트, 사용자 키, 사용자 몸무게 순으로 보여집니다.")
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(my_sell_product, columns=columns)
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

        print("총 판매 금액 집계중입니다 ... ")
        select_query = f"select seller_id, sum(count*price_per_1) FROM order_review_table GROUP BY seller_id; "
        cursor.execute(select_query)
        my_aggregation = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(my_aggregation, columns=columns)
        print("총 판매 금액")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        print("메인 페이지로 돌아갑니다.")

현재 seller3@naver.com의 판매 기록만 존재합니다.
seller4@naver.com의 판매 기록을 하나 추가하겠습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/e8aa343a-35ee-4e65-992f-1854008bd9a2)

2023000004(안경)은 아직 리뷰가 존재하지 않네요.
열람이 잘 되는 모습을 볼 수가 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/9658fcf5-707b-4000-9204-00490f8ec24d)


## 메일 보내기

이벤트 참여 테이블에서 시간이 24시간 지난 데이터들을 불러온 후, 그 중 랜덤하게 하나를 선택하였습니다.
이후 메일을 보냈습니다.

    def candidate_send_mail(administor_id):
        global user_con
        cursor = user_con.cursor()
        print("이벤트 참여자에게 메일을 보냅니다!")
        try :
            current_time = datetime.now(timezone.utc)
            yesterday = current_time - timedelta(days=1)
            print("어제 참여 후 24시간 지난 사람들 목록입니다.")
            select_query = f"SELECT event_candidate_customer_id FROM event_table WHERE participation_start_time < '{yesterday.isoformat()}'"
            cursor.execute(select_query)
            candidate_list = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(candidate_list, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

            print("어제 참여자 중 랜덤하게 한 명 뽑았습니다 . .")
            select_query = f"SELECT event_candidate_customer_id FROM event_table WHERE participation_start_time < '{yesterday.isoformat()}' ORDER BY RANDOM() LIMIT 1"
            cursor.execute(select_query)
            selected_candidate = cursor.fetchone()[0]
            print(f"선택된 이벤트 참여자 아이디: {selected_candidate}")

            title = input("메일 제목을 입력하세요 : ")
            content = input("메일 내용을 입력하세요 : ")
        
            msg = MIMEText(content)
            msg['Subject'] = title
            print("구글 계정으로 메일을 보냅니다. 구글 계정과 Gmail 앱 비밀번호가 없으시다면 가입 후 사용해주시길 바랍니다.")
            print("Gmail 앱 비밀번호를 발급받는 방법 1단계 : Gmail 홈에서 톱니바퀴 > 빠른 설정 > 모든 설정 보기")
            print("Gmail 앱 비밀번호를 발급받는 방법 2단계 : IMAP 사용하기 설정")
            print("Gmail 앱 비밀번호를 발급받는 방법 3단계 : Google 계정 관리 > 보안 > 2단계 인증")
            print("Gmail 앱 비밀번호를 발급받는 방법 4단계 : 인증 완료 후 OTP 추가")
            print("Gmail 앱 비밀번호를 발급받는 방법 5단계 : 2단계 인증 시작화면으로 들어와서, 앱 비밀번호 설정.")
            print("Gmail 앱 비밀번호를 발급받는 방법 6단계 : 앱 비밀번호 생성 > 기타(맞춤 이름) ")
            print("16자리 우측 상단 기기용 앱 비밀번호를 기억해주세요.")
        
            # (*)메일의 발신자 메일 주소, 수신자 메일 주소, 앱비밀번호(발신자)
            receiver = selected_candidate
            sender = input("보내는 사람의 구글 계정을 입력해주세요.")
            app_password = input("16자리 앱 비밀번호를 입력해주세요 : ")
        
            with smtplib.SMTP('smtp.gmail.com', 587) as s:  # TLS 암호화
                s.starttls()
                s.login(sender, app_password)
                s.sendmail(sender, receiver, msg.as_string())
            print("메일 발송이 완료되었습니다.")

            delete_query = f"DELETE FROM event_table WHERE participation_start_time < '{yesterday.isoformat()}'"
            cursor.execute(delete_query)
            user_con.commit()
            print("24시간 지난 참여한 사람들의 데이터가 삭제되었습니다.")


        except Exception as e :
            print(f"에러가 발생했습니다 : {e}")
            print("메인 페이지로 돌아갑니다")

데이터는 이럼. test5는 제가 설정했음.
![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/fb993b94-c4ea-45a0-b590-951484fe15af)


코드 내부에서 편의상 저는 미리 설정을 했지만,
배포판에서는 입력으로 받을 수 있도록 수정을 하였습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/d3a931d5-e64f-42bf-9af1-dec158fbe719)


잘 받은 것을 확인할 수 있습니다. 절 찾아오시면 선물을 드리도록 할게요.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/1bee8487-2f00-45db-a847-18c35860f2a1)


또한, DBeaver에서도 데이터가 삭제된 것을 볼 수 있습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/c8d188fa-8b27-402a-adff-88c84dd2fbb4)


### 마무리하며

길고 길었던 database 텀프로젝트가 끝났습니다.
급하게 하느라, 에러 처리도 미흡하게 끝난 경향이 있지만, 그래도 재밌었습니다.
GUI 구현도 좀 아쉽긴 하네요. 아무쪼록 마무리가 되어서 기분이 좋습니다!
<br>
방학 땐, java spring 공부를 해보려고 합니다.
그 때 spring framework를 사용한 좀 더 업그레이드 한 쇼핑몰 구축으로 돌아오겠습니다.

