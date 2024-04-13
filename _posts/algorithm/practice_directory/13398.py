import sys
n=int(input())
arr=list(map(int, sys.stdin.readline().split()))
dp=[0 for _ in range(n)]
dp_reverse=[0 for _ in range(n)]
dp[0]=arr[0]
dp_reverse[0]=arr[-1]

#음수 제거하지 않고
for i in range(1,n) : 
    dp[i]=max(dp[i-1]+arr[i],arr[i])
    dp_reverse[i]=max(arr[(n-1)-i] , dp_reverse[i-1] + arr[(n-1)-i])    
dp_reverse.reverse()
answer=max(dp)
for i in range(1,n-1) :
    answer=max(answer, dp[i-1] + dp_reverse[i+1])
        #answer=max(answer, dp[i-1] + dp_reverse[n-i-2])
print(answer)
