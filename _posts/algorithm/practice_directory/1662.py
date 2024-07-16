import sys
from collections import deque

s=sys.stdin.readline().rstrip()
stack=deque()
answer,idx="",0

for i in range(len(s)) :
    char = s[i]
    stack.append(char)
    
    if char==')' :
        cnt=0
        stack.pop()
        while True :
            #top=stack[-1]
            top = stack.pop()
            
            if top=='(' :
                break
            
            if type(top)==int :
                cnt+=top
            else :
                cnt+=1  
        top = stack[-1]
        cnt=int(top)*cnt
        stack.pop()
        stack.append(cnt)   
ans = 0
while stack :
    top = stack.pop()
    if type(top) == int :
        ans+=top
    else :
        ans+=1
print(ans)