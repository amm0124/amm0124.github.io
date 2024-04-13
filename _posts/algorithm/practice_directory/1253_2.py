#확인만 하면 되는 문제

import sys

n=int(input())
numbers=list(map(int,sys.stdin.readline().split()))
numbers.sort()
number_count=dict()
answer=0

for number in numbers :
    if number in number_count :
        number_count[number]+=1
    else :
        number_count[number]=1

for number in numbers :
    pass