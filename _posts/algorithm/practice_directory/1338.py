import sys
s,e=map(int,sys.stdin.readline().split())
x,y=map(int,sys.stdin.readline().split())
cycle=e-s
#범위 내에서 여러 사이클이 생긴다면 -> Unknown Number

#cycle = x+1인 경우  7 8 9 0 1 2 3 4 5 6  이런 경우
if cycle>=x+1  :
    print("YES")
elif cycle<=2*x: #7 8 9 0 1 2 3 4 5 6 7 8 에서 y가 9면 된다.
    print("YES")
else : 
    print("NO")


if e>=s+x-1 : 
    pass
else :
    print("Unknwon Number")

"""
if 1cycle not :
    print(Unknown Number)
else : #일단 한 사이클은 됨. 
    
    
    

    
    """