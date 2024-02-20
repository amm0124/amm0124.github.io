import sys,math

def tsp(cur, visited):
    global cache,cost,n
    
    if cache[cur][visited]!=math.inf :
        return cache[cur][visited]

    if visited==(1<<cur):
        return cost[0][cur]

    for prev in range(n) :
        if cost[prev][cur]==0:
            continue
        if (1<<prev)&visited==0:
            continue
        cache[cur][visited]=min(cache[cur][visited], tsp(prev, visited&~(1<<prev)) + cost[prev][cur])

    return cache[cur][visited]

n=int(sys.stdin.readline())
cost=[list(map(int, sys.stdin.readline().split())) for _ in range(n)]

cache=[[math.inf]*((1<<n)-1) for _ in range(n)]

ans=math.inf
for i in range(n) :
    ans=min(ans, tsp(i, (1<<n)-1))
print(ans)

n = int(input())

INF = int(1e9)
dp = [[math.inf] * (1 << n) for _ in range(n)]
def dfs(x, visited):
    if visited == (1 << n) - 1:     # 모든 도시를 방문했다면
        if graph[x][0]:             # 출발점으로 가는 경로가 있을 때
            return graph[x][0]
        else:                       # 출발점으로 가는 경로가 없을 때
            return math.inf

    if dp[x][visited] != math.inf:       # 이미 최소비용이 계산되어 있다면
        return dp[x][visited]

    for i in range(1, n):           # 모든 도시를 탐방
        if not graph[x][i]:         # 가는 경로가 없다면 skip
            continue
        if visited & (1 << i):      # 이미 방문한 도시라면 skip
            continue

        # 점화식 부분(위 설명 참고)
        dp[x][visited] = min(dp[x][visited], dfs(i, visited | (1 << i)) + graph[x][i])
    return dp[x][visited]


graph = []
for i in range(n):
    graph.append(list(map(int, input().split())))

print(dfs(0, 1))