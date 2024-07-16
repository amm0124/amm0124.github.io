import sys,heapq

n,m=map(int,sys.stdin.readline().split())
male=list(map(int,sys.stdin.readline())).sort()
female= list(map(int,sys.stdin.readline())).sort()

dp=[[0 for _ in range(m+1)] for _ in range(n+1) ]

for i in range(1,n+1) :
    for j in range(1,m+1) :
        pass