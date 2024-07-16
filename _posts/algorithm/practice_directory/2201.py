"""
k=int(input())

answer="1"
dp=[[1,1] for _ in range(100)]
sum_table=[1 for _ in range(100)]
for i in range(2,100) :
    dp[i][0]=dp[i-1][0]+dp[i-1][1]
    dp[i][1]=dp[i-1][0]
    sum_table[i]=sum_table[i-1]+dp[i][0]+dp[i][1]
    
if k!=1 :
    stop=0
    for i in range(2,100) :
        if k<=sum_table[i] :
          stop=k
    k-=(sum_table[stop-1]+1)      
    stop-=1
    while stop>0 :
        if k>sum_table[stop-1] :
            answer+="1"
            k-=(sum_table[stop-1]+1)
        else :
            answer+="0"
        stop-=1
        
print(answer)
"""


L_MAX = 100

k = int(input())

dp = [[0, 0] for _ in range(L_MAX + 1)]
sum_dp = [0] * (L_MAX + 1)

dp[1][1] = 1
sum_dp[1] = 1

for i in range(2, L_MAX + 1):
    dp[i][0] = dp[i - 1][0] + dp[i - 1][1]
    dp[i][1] = dp[i - 1][0]
    sum_dp[i] = dp[i][0] + dp[i][1] + sum_dp[i - 1]

if k == 1:
    print(1)
else:
    print(1, end='')
    n = 0
    for i in range(2, L_MAX + 1):
        if k <= sum_dp[i]:
            n = i
            break
    k -= (sum_dp[n - 1] + 1)
    n -= 1
    while n > 0:
        if k > sum_dp[n - 1]:
            print(1, end='')
            k -= (sum_dp[n - 1] + 1)
        else:
            print(0, end='')
        n -= 1
    print()
