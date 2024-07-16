import sys
n=int(input())
arr=list(map(int,sys.stdin.readline().split()))
dp=[1 for _ in range(n)]
for row in range(1,n) :
    now_value=arr[row]
    for col in range(row) :
        if now_value>arr[col] :
            dp[row]=max(dp[row],dp[col]+1 )
max_index = arr.index(max(dp))

print(max(dp))