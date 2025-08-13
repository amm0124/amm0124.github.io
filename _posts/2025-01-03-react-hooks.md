---
title: "React Hooks 완벽 가이드"
excerpt: "useState, useEffect를 중심으로 한 React Hooks 사용법"

categories:
  - Frontend
tags:
  - [React, JavaScript, Hooks]

toc: true
toc_sticky: true

date: 2025-01-03
last_modified_at: 2025-01-03
---

## React Hooks란?

React 16.8에서 도입된 Hooks는 함수형 컴포넌트에서 상태와 생명주기를 다룰 수 있게 해줍니다.

### 주요 Hooks

- useState: 상태 관리
- useEffect: 부수 효과 처리
- useContext: 컨텍스트 사용
- useReducer: 복잡한 상태 관리

## useState 사용법

{% highlight jsx %}
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        증가
      </button>
    </div>
  );
}
{% endhighlight %}

## useEffect 사용법

{% highlight jsx %}
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  return (
    <div>
      {user ? <h1>{user.name}</h1> : <p>로딩 중...</p>}
    </div>
  );
}
{% endhighlight %}

### 정리 함수

{% highlight jsx %}
useEffect(() => {
  const timer = setInterval(() => {
    console.log('Timer tick');
  }, 1000);

  return () => {
    clearInterval(timer);
  };
}, []);
{% endhighlight %}

Hooks를 사용하면 더 간결하고 재사용 가능한 컴포넌트를 만들 수 있습니다.