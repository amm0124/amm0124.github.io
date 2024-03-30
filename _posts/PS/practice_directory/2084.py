import sys
n=int(input())
graph_degree=list(map(int,sys.stdin.readline().split()))

if sum(graph_degree)%2!=0:
    print(-1)
else :
    pass