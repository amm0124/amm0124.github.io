from collections import deque
import sys
from itertools import permutations

n=int(input())
scv=list(map(int, sys.stdin.readline().split()))+[0 for _ in range(3-n)]
dp=[[[float("INF") for _ in range(61)] for _ in range(61)] for _ in range(61)]
dp[scv[0]][scv[1]][scv[2]]=0

queue=deque()
queue.append(scv+[0]) #[scv1, scv2, scv3, answer]
attack=list(permutations([9,3,1]))

while queue :
    s1,s2,s3,cnt=queue.popleft()
    for i in range(6) :
        new_s1=max(0,s1-attack[i][0])    
        new_s2=max(0,s2-attack[i][1])    
        new_s3=max(0,s3-attack[i][2])    
        if new_s1==0 and new_s2==0 and new_s3==0 :
            print(cnt+1)
            sys.exit()
        else :
            if dp[new_s1][new_s2][new_s3]>cnt+1 :
                dp[new_s1][new_s2][new_s3]=cnt+1
                queue.append([new_s1,new_s2,new_s3,cnt+1])
            