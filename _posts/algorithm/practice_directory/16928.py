import sys
from collections import deque
n,m=map(int,sys.stdin.readline().split())
ladders, snakes= dict(), dict() # key : start , value : end
dp=[i for i in range(101)]

for i in range(1,7) :
    dp[i]=1

for i in range(n) :
    x,y=map(int,sys.stdin.readline().split())
    ladders[x]=y 
    
for i in range(m) :
    x,y=map(int,sys.stdin.readline().split())
    snakes[x]=y
    
queue=deque()
queue.append(1)

#BFS
while queue :
    now = queue.popleft()
    
    if now==100 :
        print(dp[100])
        break
    for i in range(now+1, min(now+7,101)) :
        if dp[i]==i :
            queue.append(i)
            dp[i]=min(dp[i], dp[now]+1)

    if now in ladders:
        dp[ladders[now]]=min(dp[ladders[now]], dp[now])
        queue.append(dp[ladders[now]])
    if now in snakes:
        dp[snakes[now]]=min(dp[snakes[now]], dp[now])
        queue.append(dp[snakes[now]])

# 동적 계획법으로 하면 안 되는 이유가
# 1. 내려왔을 때 최솟값이 갱신 될 수가 있음. 하지만 동계법 특성상 앞만 보고 달림. 기존은 최적일 것이라고 하기에
# 따라서, 다시 본 부분이 최적이 아닐 수가 있기에 .. 
# 동계법 + BFS로 해야함.