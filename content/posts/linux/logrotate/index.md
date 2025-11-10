---
title: "Log rotate의 두 종류"
excerpt: "Log rotate의 두 종류"

type: docs

categories:
  - Linux
tags:
  - [Cloud Native, Cloud, K8s]

toc: true
toc_sticky: true

date: 2025-09-29
last_modified_at: 2025-09-29
---

## logrotate

`logrotate`는 linux system에서 지속적으로 쌓이는 로그 파일의 크기를 관리하고, 오래된 로그를 자동으로 처리(회전, 압축, 삭제)해주는 utility이다.
`logrotate`는 단독으로 실행되는 daemon이 아니며, `cron` 스케줄러에 의해 주기적으로 실행된다.

## logrotate mechanism

{{< figure src="logrotation-components.png" caption="logrotate의 주요 컴포넌트" >}}

- appender : 로그 파일에 계속해서 내용을 작성하는 `writer`이다. 이는 application일 수도, `kubelet`, `docker log driver`, `syslog` 등 시스템 데몬일 수 있다.
- tailer : 로그 라인이 추가될 때마다 이를 읽는 `reader`이다. 예를 들어, `promtail`, `alloy`와 같은 로그 에이전트가 있다.
- Log rotator : 주기 혹은 크기 임계점에 따라 로그 파일을 rotate하는 프로세스이다.

`fd`는 `파일 디스크립터`를 의미한다. 일단 Linux에서 파일이 읽기 또는 쓰기 모드로 열리면, OS는 프로세스별 고유한 파일 디스크립터를 반환하며, 읽기 및 쓰기와 같은 모든 작업은 해당 파일 디스크립터를 통해 이루어진다. 즉 파일이 열리면, 파일 이름보다 파일 디스크립터가 더 중요해진다. 

`Log rotator`는 두 가지 방식으로 구현될 수 있다. `copy and truncate` 방식과, `rename and create` 방식이다.

### copy and truncate

| `copy and truncate` : 로그 파일을 error.log.1과 같이 다른 이름을 copy한 다음, 원본 로그 파일 (error.log)의 내용을 비우는(truncate) 방식이다.

{{< figure src="logrotation-copy-and-truncate.png" caption="Copy and Truncate 방식의 logrotate" >}}

`copy and truncate` 방식은 계속해서 로그에 값을 쓰는 `appender`에게 유리하다. 왜냐하면 원본 로그 파일에 대한 파일 디스크립터가 변경되지 않기 때문이다. 즉, `appender`는 다시 파일을 열 필요가 없다. 그러나 계속해서 로그를 감시하는 `tailer`에게는 불리하다. 왜냐하면 파일이 잘리는 시점과 해당 로그 파일 읽기를 마치는 시점에서 `경합 상태(race condition)`가 발생할 수 있기 때문이다. `tailer`이 로그를 다 읽지 않았음에도, rotate 임계치에 도달해서 truncate 된다면 로그가 유실될 수 있다. 따라서 `appender`에는 유리하고, `tailer`에게는 불리하다.

### rename and create

| `rename and create` : 로그 파일의 이름을 error.log.1과 같이 변경(rename)한 다음, 원본과 이름이 같은 로그 파일을 생성(create)하는 방식이다.

{{< figure src="logrotation-rename-and-create.png" caption="Rename and Create 방식의 logrotate" >}}

`rename and create` 방식은 `copy and truncate` 방식에서의 `race condition` 방지에 도움을 줄 수 있다. 로그 파일 이름이 변경되더라도, `파일 디스크립터(fd)`는 유지가 되기 때문이다. 따라서 `tailer`는 작업이 완료될 때까지 로그 파일을 계속해서 읽을 수 있다. 하지만, `rename and truncate` 방식에도 문제점이 존재하는데, `appender`에게 새로운 파일을 열도록 신호를 보내야 한다는 것이다. 로그 파일 이름은 같지만, 파일 자체는 다르기 때문에 `파일 디스크립터` 또한 다를 것이다. 따라서 `appender`은 새로 파일을 열어야 한다. 열지 않으면, 이름이 변경된 `error.log.1`에 로그를 계속 쓰게 되는 문제점이 발생할 것이다.

## 참고 자료

- https://grafana.com/docs/loki/latest/send-data/promtail/logrotation/