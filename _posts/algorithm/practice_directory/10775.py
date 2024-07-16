from collections import deque

g=int(input())
p=int(input())
stack = deque()

for _ in range(g) :
    gi = int(input())
    if not stack : #stack.empty()
        stack.append((gi, 1)) #gi까지 1개 가능함
    else :
        range = stack[-1][0]
        count = stack[-1][1]
        if gi > range :
            pass
        elif gi == range :
            stack.pop()
            stack.append((gi, count+1))
        else : #gi < range
            pass