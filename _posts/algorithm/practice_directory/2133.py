
n=int(input())
if n%2!=0 :
    print(0)
else :
    dp=[0 for _ in range(n+1)]
    dp[0]=1
    dp[2]=3
    for i in range(4,n+1,2) :
        dp[i]=3*dp[i-2]
        tmp=i-4
        while tmp>=0 :
            dp[i]+=dp[tmp]*2
            tmp-=2
    print(dp[n])