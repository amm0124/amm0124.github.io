import sys
from collections import deque

n,k=map(int,sys.stdin.readline().split())
queue=deque()    
queue.append((n,0))
dp=[False for _ in range(100001)]
while queue :
    position, weight = queue.popleft()
    if position==k :
        print(weight)
        sys.exit()
    if position-1>=0 and dp[position-1]==False:
        queue.append((position-1,weight+1))
        dp[position-1]=True
    if position+1<=100000 and dp[position+1]==False:
        dp[position+1]=True
        queue.append((position+1,weight+1))
    if (2*position<=100000 and 2*position>=0) and dp[position*2]==False :
        dp[2*position]=True
        queue.append((2*position,weight+1))