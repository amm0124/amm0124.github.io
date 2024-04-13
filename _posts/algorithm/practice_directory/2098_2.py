import sys,math
sys.setrecursionlimit(10**9)
n = int(input())

INF = int(1e9)
dp = [[math.inf] * (1 << n) for _ in range(n)]
def dfs(x, visited):
    if visited == (1 << n) - 1:     
        if graph[x][0]:             
            return graph[x][0]
        else:                       
            return math.inf

    if dp[x][visited] != math.inf:       
        return dp[x][visited]

    for i in range(1, n):           
        if not graph[x][i] :       
            continue
        if visited & (1 << i): 
            continue
        dp[x][visited] = min(dp[x][visited], dfs(i, visited | (1 << i)) + graph[x][i])
    return dp[x][visited]

graph = []
for i in range(n):
    graph.append(list(map(int, sys.stdin.readline().split())))

print(dfs(0, 1))