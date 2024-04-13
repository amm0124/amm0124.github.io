import sys
sys.setrecursionlimit(10**8)

def solution(n, pos_x, pos_y) :
    if n==1 :
        if pos_x==2 and pos_y==2:
            return ' '
        else :
            return '*'
    else :
        answer=''
        for i in range(1,4) :
            for j in range(1,4) :
                answer+=solution(n//3,i,j)
            answer+='\n'
        return answer
        
n=int(input())
answer=''
for i in range(1,4) :
    for j in range(1,4) :
        answer+=solution(n//3,i,j)
    answer+='\n'
print(answer)