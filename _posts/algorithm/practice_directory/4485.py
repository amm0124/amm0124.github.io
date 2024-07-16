import heapq,sys
cnt = 1
while True :
    n=int(input())
    cost = []
    if n==0 :
        sys.exit()
    graph = [[0]*(n) for _ in range(n)]
    for i in range(n) :
        graph[i]=list(map(int,sys.stdin.readline().split()))
    pq = []
    
    heapq.heappush(pq, (0 , 0, 0)) # (cost, x, y)
    while pq :
        pass


    
    print(f"Problem {cnt}: {cost[n-1][n-1]}")
    cnt+=1