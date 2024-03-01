import heapq

n,k=map(int,input().split())
if n>=k :
    print(n-k)
else :
    distance=[abs(n-i) for i in range(100001)]
    hq=[]
    heapq.heappush(hq,(0,n))
    while hq :
        dist, now = heapq.heappop(hq)
        #print("DIST AND NOW : ",dist,now)
        if dist>distance[now]:
            continue
        if now==0 : #+만
            if distance[1]>dist+1 :
                distance[1]=dist+1
                heapq.heappush(hq, (dist+1,1))
        elif now==100000: #-만
            if distance[99999]>dist+1 :
                distance[99999]=dist+1
                heapq.heappush(hq, (dist+1,99999))
        else : #3개 다 해봐야 함
            if distance[now+1]>dist+1 :
                distance[now+1]=dist+1
                heapq.heappush(hq, (dist+1, now+1))
                
            if distance[now-1]>dist+1 :
                distance[now-1]=dist+1
                heapq.heappush(hq, (dist+1,now-1))
            if 2*now<=100000 and distance[2*now] > dist :
                distance[2*now]=dist
                heapq.heappush(hq, (dist,2*now))

            """while sister<=100000:
                if distance[sister]>dist :
                    distance[sister]=dist
                    heapq.heappush(hq,(dist, sister))
                sister*=2"""
    #print(distance)
    print(distance[k])    
"""
hq=[]
heapq.heappush(hq,(0,n))
while hq :
    dist, now = heapq.heappop(hq)
    if dist>distance[now] : #heapq의 거리가 현재 저장된 거리보다 길다면 볼 필요가 없음.
        continue
    #print(dist,now)
    if 2*now<=100000 :
        if distance[2*now] > dist :
            distance[2*now]=dist
            heapq.heappush(hq, (dist,2*now))
    
    if now-1>=0 :
        if distance[now-1] > dist+1 :
            distance[now-1]=dist+1
            heapq.heappush(hq, (dist+1, now-1))
    
    if now+1<=100000:
        if distance[now+1] > dist+1 :
            distance[now+1]=dist+1
            heapq.heappush(hq, (dist+1,now-1))
            
print(distance[k])"""