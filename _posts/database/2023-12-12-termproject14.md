---
title: db_termproject(14) - 고객 사이즈 추천
date: 2023-12-12 20:00:00 +
categories: [Database, termproject]
---


# python 구현

## 고객 사이즈 추천

고객의 review 기반으로 사이즈를 추천합니다.
그에 앞서 데이터셋이 있어야 하는데, 임의의 데이터를 추가하였습니다.

    INSERT INTO order_review_table VALUES
  (1000000001, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 10, '좋아요', 185, 73),
  (1000000002, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 8, '좋아요', 180, 71),
  (1000000003, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 7, '음', 178, 73),
  (1000000004, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 6, '좋아요', 172, 65),
  (1000000005, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 3, '좋아요', 164, 60),
  (1000000006, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 9, '좋아요', 188, 81),
  (1000000007, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 10, '좋아요', 186 , 73),
  (1000000008, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 10, '좋아요', 184 , 79),
  (1000000009, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 10, '좋아요', 181 , 71),
  (1000000010, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 4, '좋아요', 164 , 55),
  (1000000011, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 3, '좋아요', 160 , 42),
  (1000000012, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 1, '좋아요', 155 , 48),
  (1000000013, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 6, '좋아요', 177 , 70),
  (1000000014, 'seller3@naver.com', 2023000001, 1, 100000, 'test3@naver.com', '2023-12-12 21:06:41.242', 7, '좋아요', 176 , 59);

굉장히 작위적인 데이터셋입니다.. 아무튼 test3@naver.com이라는 사람이 물품을 하나씩 사서, 주변 사람들에게 선물했다고 가정하겠습니다. 그리고 각자 평점을 등록한 상황입니다.

이제 추천시스템 적용을 해보겠습니다.
간단하게 선형회귀 모델을 사용해서 7점이 넘는다면 추천, 아니면 추천하지 않는 방식을 사용했습니다.

def recommended_size(customer_id):
    global user_con
    print("사이즈 추천 시스템입니다. 이때까지 리뷰를 기반으로 작동합니다.")
    cursor = user_con.cursor()
    select_query = "SELECT user_height, user_weight, review_point FROM order_review_table;"
    cursor.execute(select_query)
    data = cursor.fetchall()
    try :
        columns = ['height', 'weight', 'point']
        df = pd.DataFrame(data, columns=columns)
        X = df[['height', 'weight']]
        y = df['point']
        model = LinearRegression()
        model.fit(X, y)

        user_height = int(input("키를 정수형으로 입력하세요 : ").strip())
        user_weight = int(input("키를 정수형으로 입력하세요 : ").strip())

        new_data = [(user_height,user_weight)]
        new_df = pd.DataFrame(new_data, columns=['height', 'weight'])
        predictions = model.predict(new_df)

        if predictions[0] >= 7 :
            print("괜찮을 듯 합니다!")
        else :
            print("추천하지 않습니다.")

    except Exception as e:
        print(f"{e} 발생. 양식에 맞추어 입력해주세요.")
        print("메인으로 돌아갑니다.")

결과는 이렇게 나옵니다. 학습 데이터셋을 잘 가공된 데이터로 넣어서 그런지, 예측은 잘 될 듯 합니다.

![image](https://github.com/amm0124/amm0124.github.io/assets/108533909/7668e74e-63dd-4758-a873-b0dce1dfd108)

### 마무리하며

길었던 고객의 기능이 마무리되었습니다.
다음 글에선 판매자의 기능에 대해 설명해보겠습니다.