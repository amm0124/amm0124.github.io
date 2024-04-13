import sys
import heapq
n,e=map(int,sys.stdin.readline().split())
k=int(sys.stdin.readline())
graph=[[] for _ in range(n+1)]
for _ in range(e) :
    u,v,w=map(int,sys.stdin.readline().split())
    graph[u].append((v,w))
dist=[int(1e9) for _ in range(n+1)]
dist[k]=0
#dijkstra. start node -> k
hq=[]
heapq.heappush(hq, (0,k))

while hq : #heapq가 빌 때 까지
    now_weight, now_node=heapq.heappop(hq)
    if now_weight > dist[now_node] :
        continue
    dist[now_node]=now_weight
    for i in graph[now_node] : 
        cost=now_weight+i[1]
        if cost < dist[i[0]] :
            dist[i[0]]=cost
            heapq.heappush(hq, (cost,i[0]))
            
for i in range(1,n+1) :
    if dist[i]==int(1e9) :
        print("INF")
    else :
        print(dist[i])
