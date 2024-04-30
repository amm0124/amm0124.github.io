from itertools import combinations
import sys

t=int(sys.stdin.readline().strip())

for _ in range(t) :
    n=int(sys.stdin.readline().strip())
    vector=[]
    for _ in range(n) :
        x,y=map(int, sys.stdin.readline().split())
        vector.append((x,y))
    print(vector)