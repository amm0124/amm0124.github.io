import sys, heapq
n = int(sys.stdin.readline())
lecture = [ list(map(int, sys.stdin.readline().split())) for _ in range(n) ]
lecture.sort(key=lambda x : x[1]) 
hq = []
for i in lecture: 
    heapq.heappush(hq, i[0]) 
    if len(hq) > i[1]: 
        heapq.heappop(hq)
print(sum(hq)) 

# hq를 강의 저장하는 곳으로 넣음 
# 강연료를 알고, 몇 개의 강연을 갔는지 알면 -> 며칠 째인지 알 수 있습니다