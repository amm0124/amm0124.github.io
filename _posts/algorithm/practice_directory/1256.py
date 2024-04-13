import sys #from math import comb
n,m,k= map(int,sys.stdin.readline().split())
dp=[[ 1 for _ in range(m+1)] for _ in range(n+1)]
dp[0][0]=0
#preprocessing
for row in range(1,n+1) : 
    for col in range(1,m+1) :
        dp[row][col]=dp[row-1][col]+dp[row][col-1]
#print(dp) #(m+n)! / m!*n! 을  O(mn)의 시간으로 구할 수 있게 됨.

if k>dp[n][m] : 
    print(-1)
else :
    answer="" #m+n번 반복해서 정답을 만든다.
    row=n
    col=m
    start=1 
    end=dp[n][m]
    for count in range(n+m) :
        if row==0 :
            answer+="z"*col
            break
        elif col==0 :
            answer+="a"*row
            break
        if k<=start+dp[row-1][col]-1 :
            end=dp[row-1][col]+start-1
            answer+="a"
            row=row-1
        else : #K>= start+dp[row-1][col]
            answer+="z"
            start=dp[row-1][col]+start
            col-=1
    print(answer)
            