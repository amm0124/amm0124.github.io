import sys 

s1 = sys.stdin.readline().rstrip()
s2 = sys.stdin.readline().rstrip()

n,m=len(s1),len(s2)

dp=[[0 for _ in range(m+1)] for _ in range(n+1)]
ans=0    
for row in range(1, n+1) :
    for col in range(1,m+1) :
        if s1[row-1]==s2[col-1] : 
            dp[row][col]=dp[row-1][col-1] + 1
        else :
            dp[row][col] = max(dp[row-1][col] , dp[row][col-1])
        ans = max(ans,dp[row][col])
        
print(ans)