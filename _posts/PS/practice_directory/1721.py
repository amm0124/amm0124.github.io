import sys

p=sys.stdin.readline().strip().split('x') #x를 기준으로 parsing

if len(p)==1: #상수항만 있는 경우
    if int(p[0])==0:
        answer='W'
    else :
        if int(p[0])==1 :
            answer="x+W"
        elif int(p[0])==-1 :
            answer="-x+W"
        else :
            answer=p[0]+"x+W"
else : #x를 기준으로 parsing한 결과 -> x를 포함함 -> 부호 음수 봐야함
    x_coefficient=int(p[0])
    
    if x_coefficient<0 : #음수 
        if (x_coefficient//2)==-1 :
            answer="-xx"
        else:
            answer=str(x_coefficient//2)+"xx"  
    else : #양수
        if (x_coefficient//2)==1 :
            answer="xx"
        else:
            answer=str(x_coefficient//2)+"xx"
                
    if p[1]=='':
        answer+='+W'
    else : #상수항이 있다면
        if int(p[1])<0 :
            if int(p[1])==-1 :
                answer+="-"+"x+W"
            else :
                answer+=str(int(p[1]))+"x+W"
        elif int(p[1])==0 : 
            pass
        else :
            if int(p[1])==1 :
                answer+="+"+"x+W"
            else :
                answer+="+"+str(int(p[1]))+"x+W"
    
    
print(answer)    
    