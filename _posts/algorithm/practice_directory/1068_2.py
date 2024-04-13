import sys
sys.setrecursionlimit(10**8)

n=int(input())
inp=list(map(int, sys.stdin.readline().split())) #i노드의 parent는 parent[i]임.
remove=int(input())
tree=[[0 for _ in range(n)] for _ in range(n)] #tree[parent][child]=true

for i in range(n) :
    node, parent=i,inp[i]
    
    if parent==-1 : #root node
        pass
    else :
        tree[parent]=node    
