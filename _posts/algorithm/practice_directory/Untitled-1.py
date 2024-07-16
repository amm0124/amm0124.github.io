
import sys
n,m= map(int, sys.stdin.readline().split())

mars=[[0]*(m+1) for _ in range(n+1)]
dp=[[0]*(m+1) for _ in range(n+1)]

for row in range(1,n+1) : 
    width=list(map(int, sys.stdin.readline().split()))
    for col in range(m) :
        mars[row][col+1] = width[col]
        
for col in range(1,n+1) :
    dp[1][col]=sum(mars[1][1:col+1])


for row in range(2,n+1) : 
    for col in range(1,m+1) : 
        if col==1 :
            dp[row][col] = dp[row-1][col]+mars[row][col]
        else : 
            dp[row][col] = max(dp[row-1][col], dp[row][col-1])+mars[row][col]
     

print(dp)            

"""import sys
n,m= map(int, sys.stdin.readline().split())

mars=[[0]*(m+1) for _ in range(n+1)]
dp=[[0]*(m+1) for _ in range(n+1)]

for row in range(1,n+1) : 
    width=list(map(int, sys.stdin.readline().split()))
    for col in range(m) :
        mars[row][col+1] = width[col]
        
dp[1]=mars[1]

for row in range(1,n+1) : 
    for col in range(1,m+1) : 
        if row==1 :
            dp[row+1][col]=mars[row][col]+mars[row+1][col]
        elif row!=n:
            if col==1 :
                dp[row+1][col] = max(dp[row][col]+mars[row+1][col], dp[row+1][col])
                dp[row][col+1] = max(dp[row][col]+mars[row][col+1], dp[row][col+1])
            elif col==m:
                dp[row+1][col] = max(dp[row][col]+mars[row+1][col], dp[row+1][col])
                dp[row][col-1] = max(dp[row][col]+mars[row][col-1], dp[row][col-1])
            else :
                dp[row+1][col] = max(dp[row][col]+mars[row+1][col], dp[row+1][col])
                dp[row][col+1] = max(dp[row][col]+mars[row][col+1], dp[row][col+1])
                dp[row][col-1] = max(dp[row][col]+mars[row][col-1], dp[row][col-1])
        else : #row==n <-, -> 방향만 탐색함
            if col==1 :
                dp[row][col+1] = max(dp[row][col]+mars[row][col+1], dp[row][col+1])
            elif col==m:
                dp[row][col-1] = max(dp[row][col]+mars[row][col-1], dp[row][col-1])
            else :
                dp[row][col+1] = max(dp[row][col]+mars[row][col+1], dp[row][col+1])
                dp[row][col-1] = max(dp[row][col]+mars[row][col-1], dp[row][col-1])
print(dp)            
            
print(dp[n][m])"""
        
        
       
    