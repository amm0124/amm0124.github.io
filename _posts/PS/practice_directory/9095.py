import sys
t=int(sys.stdin.readline())
dp=[0 for _ in range(12)]
dp[1]=1
dp[2]=2
dp[3]=4

for i in range(4,12) :
    dp[i]=dp[i-1]+dp[i-2]+dp[i-3] #i-1에서 1 붙이기, i-2에서 2 붙이기, i-3 에서 3 붙이기
    
for _ in range(t) : 
    number=int(sys.stdin.readline())
    print( dp[number])
