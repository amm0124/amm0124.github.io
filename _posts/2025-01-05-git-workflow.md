---
title: "효과적인 Git 워크플로우"
excerpt: "팀 협업을 위한 Git 브랜치 전략과 워크플로우"

categories:
  - Git
tags:
  - [Git, GitHub, Workflow, Team]

toc: true
toc_sticky: true

date: 2025-01-05
last_modified_at: 2025-01-05
---

## Git 워크플로우 종류

팀 규모와 프로젝트 특성에 따라 적절한 워크플로우를 선택해야 합니다.

### Git Flow

{% highlight bash %}
# 피처 브랜치 생성
git checkout -b feature/user-authentication develop

# 개발 완료 후 develop에 병합
git checkout develop
git merge feature/user-authentication

# 릴리즈 준비
git checkout -b release/1.0.0 develop
{% endhighlight %}

### GitHub Flow

{% highlight bash %}
# 피처 브랜치 생성
git checkout -b feature/add-search-function

# 작업 후 푸시
git push origin feature/add-search-function

# Pull Request 생성 후 main에 병합
{% endhighlight %}

## 커밋 메시지 컨벤션

### Conventional Commits

{% highlight bash %}
feat: 사용자 인증 기능 추가
fix: 로그인 버그 수정
docs: README 업데이트
style: 코드 포맷팅 수정
refactor: 사용자 서비스 리팩토링
test: 로그인 테스트 케이스 추가
chore: 의존성 업데이트
{% endhighlight %}

### 좋은 커밋 메시지

{% highlight bash %}
# Bad
git commit -m "fix bug"

# Good
git commit -m "fix: 사용자 로그인 시 세션 만료 오류 수정

- 세션 타임아웃 설정을 30분으로 연장
- 만료된 세션에 대한 적절한 에러 메시지 추가
- 관련 테스트 케이스 업데이트

Fixes #123"
{% endhighlight %}

## 브랜치 관리

### 브랜치 명명 규칙

{% highlight bash %}
feature/기능명
bugfix/버그명
hotfix/긴급수정명
release/버전명
{% endhighlight %}

### 브랜치 정리

{% highlight bash %}
# 병합된 브랜치 삭제
git branch --merged | grep -v "\*\|main\|develop" | xargs -n 1 git branch -d

# 원격 브랜치 정리
git remote prune origin
{% endhighlight %}

## 충돌 해결

{% highlight bash %}
# 충돌 발생 시
git status
git diff

# 충돌 해결 후
git add .
git commit -m "resolve merge conflict"
{% endhighlight %}

일관된 Git 워크플로우는 팀의 생산성을 크게 향상시킵니다.