import sys

n,k=map(int, sys.stdin.readline().split())
dp=[[0 for _ in range(k+1)] for _ in range(n)]
"""
for row in range(n) :
    walking_time, walking_raised, bicycle_time , bicycle_raised =list(map(int, sys.stdin.readline().split()))
    if row==0 :
        dp[row][walking_time]=walking_raised
        dp[row][bicycle_time]=bicycle_raised
    else :
        for col in range(k+1) :
            if dp[row-1][col]!= 0:
                if walking_time+col<=k :
                    dp[row][walking_time+col] = max(dp[row][walking_time+col], dp[row-1][col] + walking_raised) 
                if bicycle_time+col<=k :
                    dp[row][bicycle_time+col] = max(dp[row][bicycle_time+col], dp[row-1][col] + bicycle_raised)
"""


dp=[0 for _ in range(k+1)]
for row in range(n) :
    walking_time, walking_raised, bicycle_time , bicycle_raised =list(map(int, sys.stdin.readline().split()))
    tmp=[]
    for col in range(k+1) :
        if dp[col]!=0 :
            if walking_time+col<=k :
                tmp.append((walking_time+col , ))
                    #dp[row][walking_time+col] = max(dp[row][walking_time+col], dp[row-1][col] + walking_raised) 
            if bicycle_time+col<=k :
                pass
            tmp.append((col))
    dp=[0 for _ in range(k+1)]

          
print(max(dp))