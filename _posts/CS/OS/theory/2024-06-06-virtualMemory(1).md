---
title: 운영체제(25) - virtual memory (1) 
date: 2024-6-6 19:00:00 +
categories: [CS, Operating system]
tags : CS OS
---

## virtual memory

### virtual memory를 사용하게 된 배경

- 프로그램을 실행해보니, 전체 code가 꼭 memory에 올라가지 않아도 됨
    - 사용을 잘 하지 않는 code(error 처리하는 code는 에러가 raise한 경우에만 실행됨. 에러가 없다면 굳이 메모리에 올리지 않아도 되는 것 아닌가?), 제일 마지막에 사용되는 매우 큰 data structure 등.
- 또한, 전체 코드가 꼭 같은 시간에 올라가야 할까?
    - 생각해보니 code는 순차적으로 실행되는데, 제일 나중에 사용되는 code는 나중에 올려도 되지 않을까?

이러한 점을 고려했을 때, 프로그램을 부분적으로 disk에서 loading을 해보자는 아이디어가 나왔습니다.

- 부분적으로 loading을 하면, 프로그램은 물리적 메모리의 한계에서 벗어날 수 있다.
    - 왜? memory가 4GB 가정. 만약 프로그램이 필요로 하는 메모리가 6GB다? 부분적으로 로딩을 한다면, 4GB를 가지고도, 전체 프로그램을 실행할 수 있다. 
    - 이는 물리적 한계를 뛰어 넘을 수 있다,
- 하나의 프로그램당 사용하는 메모리가 줄어든다. 이는 한 번에 많은 양의 프로그램을 메모리에 올릴 수 있다. 
    - 더 많은 프로그램을 concurrency하게 실행 가능.
    - 이는 CPU utilization 향상을 도모한다.
- 이는 memory <=> disk swap I/O를 줄인다. 
    - 왜? disk에서 memory에 부분을 loading하기 때문에, 전체 loading보다 I/O 작업량이 낮다.
    또한, 필요한 부분만 swap하면 되니까. 전체 swap하는 것 보다 I/O 작업량이 낮다.

### virtual memory?

virtual memory란 user의 logical memory를 physical memory와 분리하는 방식입니다. 
- 이를 통해, logical address space는 pyhsical address space보다 더 크게 이용 가능함.
    - 왜? logical memory address가 disk 영역을 포함할 수 있기 때문.
- 주소 공간을 공유할 수 있고, 효율적임.
- 메모리를 disk와 CPU 사이 cache처럼 사용하자.
- 속도는 좀 느리지만, 많은 process를 실행 가능하다.

