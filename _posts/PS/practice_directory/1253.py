#확인만 하면 되는 문제

import sys,bisect

n=int(input())
numbers=list(map(int,sys.stdin.readline().split()))
numbers.sort()
number_count=dict()
answer=0

for i in range(n) :
    target=numbers[i]
    for j in range(n) :
        if i!=j : #binary_search
            
            
            pass

