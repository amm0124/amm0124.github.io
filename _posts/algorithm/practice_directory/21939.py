import sys,heapq

#O(1)으로 or log n으로 정렬해야 함
#hq1 , hq2 = [] , []
#git = dict()
n=int(input())

hq = [ tuple(reversed(list(map(int, sys.stdin.readline().split())))) for _ in range(n)]
minheap = []
maxheap = []

#print(hq1)

m=int(input())

for _ in range(m) :
    query = list(sys.stdin.readline().split())
    if query[0]=='add' :
        hq.append(int(query[1]), int(query[0]))
    elif query[0]=='recommend' :
        if query[1]=='1' : # 가장 어려운 난이도 문제 pop
            pass
        else : # 가장 쉬운 문제 난이도 pop
            pass
    else : # solved -> remove
        pass