n=int(input())
beads = [int(input()) for _ in range(n)]
dp=[[ [1 for _ in range(n+1)] for _ in range(n+1)] for _ in range(sum(beads)+1)]

for i in range(3,sum(beads)+1) :
    for j in range(1,n+1) :
        for k in range(1,n+1) :
            if j!=k :
                for l in range(1,n+1) :
                    if l!=i:
                        dp[i][j][k]=dp[i-1][k][l]
print(dp)
            