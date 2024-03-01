#걸을 때는 1초당 1, 점프는 t초당 d 
#나의 위치 (x,y) -> (0,0)

import sys,math
x,y,d,t=map(int,sys.stdin.readline().split())
answer=math.sqrt((x**2)+(y**2))
base_distance=answer
count=float((int(base_distance//d)) + 1)
if count<=2 :
    count=2
print(min(answer, t+ abs(base_distance - d) , float(count*t), (count-1)*t+abs(base_distance-(count-1)*d) ))
        
        
"""
    import sys,math
x,y,d,t=map(int,sys.stdin.readline().split())
#걸을 때는 1초당 1, 점프는 t초당 d 
#나의 위치 (x,y) -> (0,0)
answer=math.sqrt((x**2)+(y**2))
if d%t<=1.0 or t>=answer : #움직이는 거리 가성비가 좋지 않거나, 점프 1회했을 때 -> 손해인 경우 
    print(answer)
else : 
    base_distance=answer
    count=1
    while base_distance-(count)*d>=0:
        count+=1
    print(count)
    print(min(answer, count*t + abs(base_distance - count*d), (count-1)*t+abs(base_distance)-(count-1)*d) ) 
        
    
    """