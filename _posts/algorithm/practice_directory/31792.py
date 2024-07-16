import sys
q=int(input())

media_dict=dict()

for _ in range(q) :
    query=list(map(int,sys.stdin.readline().split()))
    if query[0]==1 : # 1번 질의. append
        media_dict[query[0]]==1
    elif query[1]==2: # 2번 질의
        pass
    else : # 3번 질의
        pass 