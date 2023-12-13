---
title: db_termproject(16) - seller 기능 구현(2) QnA 답변
date: 2023-12-12 22:00:00 +
categories: [Database, termproject]
---

# python 구현

이번 글에선 QnA 답변 및 SMTP protocol을 사용해서 간략하게 user에게 메일을 보내도록 하는 방법을 알아보겠습니다.
일단 실제로 존재하는 메일 주소로 회원 가입을 진행해주겠습니다.
customer는 제 naver 메일 계정으로, seller는 제 구글 계정으로 진행했습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/8755ee60-b548-4abe-b881-aae0d7b764cc)

빠르게 회원 가입을 했습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/364460e9-6a7a-496e-b507-f70d21b5164c)

seller로도 빠르게 가입했습니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/915fcf94-9c88-4fd0-9f6c-6021f1740e46)

빠르게 customer로 로그인 후, QnA 게시판에 질문을 남겼습니다.

## QnA 답변

일단 seller로 로그인 후, 자신의 product_subcode를 조회 후, 선택합니다.
이후 그에 해당하는 질문에 대답을 남기면 됩니다.

    def qna_answer(seller_id):
        print("QnA 게시판입니다.")
        cursor = user_con.cursor()
        try :
            print("내가 등록한 품목을 불러옵니다.")
            select_query = f"select * from product_view WHERE product_seller='{seller_id}';"
            cursor.execute(select_query)
            my_product_info = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(my_product_info, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

            print("QnA 게시판 불러옵니다..")
            select_query= f"select * FROM qna WHERE seller_id='{seller_id}';"
            cursor.execute(select_query)
            qna_list= cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(qna_list, columns=columns)
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

            qna_num = int(input("답변하고 싶은 QnA num을 입력해주세요 : ").strip())
            answer = input("답변하고 싶은 대답을 입력해주세요 : ").strip()

            update_query =f"UPDATE qna SET answer='{answer}' WHERE qna_num ={qna_num};"
            cursor.execute(update_query)
            user_con.commit()
            print("답변 달았습니다. ")
            mail = input("메일 보내시기 원하시면 1번, 아니면 2번을 눌러주세요 : ").strip()
            if mail=='1':
                send_mail()

        except Exception as e:
            print(f"{e}: 입력 양식을 맞춰주세요")
        print("메인 페이지로 이동합니다.")

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/d790694b-2bad-4e13-8ee9-701170bb71bd)

질문 목록이 잘 불러와집니다.
메일을 보내는 함수를 봐야겠습니다.

## 메일 보내기

    def send_mail():
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

        #sender = input("보내는 사람의 구글 계정을 입력해주세요.")
        #receiver = input("받는 사람의 구글 계정을 입력해주세요.")
        #app_password = input("16자리 앱 비밀번호를 입력해주세요 : ")

        with smtplib.SMTP('smtp.gmail.com', 587) as s:  # TLS 암호화
            s.starttls()
            s.login(sender, app_password)
            s.sendmail(sender, receiver, msg.as_string())
        print("메일 발송이 완료되었습니다.")

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/cf2a9745-ef6b-45a3-843c-9e014a7ec1c7)

메일을 보내기 위해서 귀찮지만 앱 비밀번호를 발급받아야 합니다.
제가 상세하게 하는 방법을 써 놨으니 한 번 해보실 분은 해보시길 바랍니다.


![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/b6a76670-7bc4-4a29-add5-19a9e6b7dcca)

제가 분명 메일을 받았는데 '받는이없음' 이라고 나오네요..
구글 계정을 사용하지 않고 naver 계정을 사용해서 그런가봅니다.
아무튼 메일이 잘 발송됨을 확인할 수 있습니다.


### 마무리하며

customer에 이어서, seller의 기능까지 알아보았습니다.
이제 다음 글에서는 administor에 대해 알아보겠습니다.





