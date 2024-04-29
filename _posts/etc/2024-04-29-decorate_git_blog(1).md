---
title: git blog를 꾸며보자 (1) - 방문자 추가
date: 2024-4-29 19:00:00 +
categories: [record, etc]
tags : githubio hits today
---

## git blog를 꾸며보자

반갑습니다. 제가 예전부터 git blog에 tistory나 다른 블로그 플랫폼처럼 투데이를 넣어보고 싶었습니다. 하지만 git blog는 그런 기능을 제공해주지 않아서 항상 아쉬웠습니다.
개발자의 자유를 중시하는 git blog의 장점이자 단점입니다. 

이를 해결하기 위해서, [gjbae님의 hit counter](https://github.com/gjbae1212/hit-counter)라는 오픈소스 프로젝트를 활용하였습니다.

[gjbae님의 hit counter 후기](https://medium.com/@gjbae1212/github-repository-%EB%B0%A9%EB%AC%B8%EC%88%98%EB%A5%BC-%ED%8A%B8%EB%9E%98%ED%82%B9-%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-1df4dfc5509c)

## hits

hits를 사용해서 git blog에 today를 추가하는 방법을 알아봅시다. 저는 jekyll-theme-chirpy 테마를 사용해서 git blog를 만들었기에, 이를 기준으로 설명하겠습니다.

### today badge

[https://hits.seeyoufarm.com/](https://hits.seeyoufarm.com/)

일단 위 링크로 들어가서, 아래 사진처럼 TARGET URL에 자신의 git blog url을 입력하시고, 나머지는 자신의 취향껏 커스터마이징하면 됩니다.

![image](https://github.com/amm0124/issue_repository/assets/108533909/452b2002-f258-47b4-aae8-fcf37f55455f)

hits에서 자동으로 취향껏 만든 badge를 아래 사진처럼 제공합니다. HTML LINK를 복사합니다.

![image](https://github.com/amm0124/issue_repository/assets/108533909/6b4bd6cb-a74e-478f-8a26-808a53493358)

만들어진 badge를 이제 웹 사이트에 추가해야 합니다. F12(개발자 도구)를 눌러 badge를 넣고 싶은 곳의 정보를 확인합니다. 
저는 sidebar에 header에 넣고 싶어서, header의 class 이름이 profile-wrapper임을 확인했습니다. 

![image](https://github.com/amm0124/issue_repository/assets/108533909/2aae8d15-1318-4df0-8d37-4720b674a0b2)

class이름이 profile-wrapper임을 확인했으므로, 이제 badge를 넣을 수 있습니다. 
profile-wrapper라는 class가 어디 있는지 확인하기 위해서, 제일 상위 문서에서 편집기의 검색 기능을 활용하였습니다.

![image](https://github.com/amm0124/issue_repository/assets/108533909/82d7f63b-b851-4863-90cd-803df5172141)

_includes의 sidebar.html 파일에 있음을 확인했습니다. 저는 저의 소개 "work hard" 아래에 badge를 표현하고 싶었으므로 위치에 해당하는 곳에 위에서 복사한 HTML LINK를 넣어주었습니다. 

![image](https://github.com/amm0124/issue_repository/assets/108533909/0db92b00-94b7-4827-a4e7-aaa38c36049e)

이후 git push를 하면 될 줄 알았는데, build가 실패합니다.

![image](https://github.com/amm0124/issue_repository/assets/108533909/0db0e6e4-2e5a-4969-b7c1-ea6de2d994c7)

오류 메시지를 자세하게 읽어봅시다.

    does not have an alt attribute
 
alt attribute가 존재하지 않아서 생긴 오류였네요. 그렇다면 alt attribute를 추가해봅시다.

    <a href="https://hits.seeyoufarm.com">
      <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Famm0124.github.io&count_bg=%2343493E&title_bg=%233264C6&icon=github.svg&icon_color=%23EAEAEA&title=today&edge_flat=false" alt="today"/>
    </a>

저는 간략하게 alt="today"를 입력해주었습니다.

이러고 push를 하면 

![image](https://github.com/amm0124/issue_repository/assets/108533909/fe6d0c3e-4ce7-47e0-9c38-b3d58bd0964a)

이제 today badge가 추가됐습니다!

## 마무리하며

hits를 사용해 git blog에 today를 넣어보았습니다. 개발자 도구를 잘 활용하여, badge를 넣고 싶은 위치의 정보만 잘 확인하신다면 다들 쉽게 할 수 있을거라 생각합니다!
 