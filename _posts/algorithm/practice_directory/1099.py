import sys

def calculate_cost(string1, string2) :
    if sorted(string1)!=sorted(string2) :
        return float("INF")
    
    answer=0
    for i in range(len(string1)) :
        if string1[i]!=string2[i]:
            answer+=1
    return answer

target=" "+sys.stdin.readline().rstrip()
n=int(input())
word_dict=dict()
for _ in range(n) :
    word=sys.stdin.readline().rstrip()
    if len(word) not in word_dict :
        word_dict[len(word)]=[word]
    else :
        word_dict[len(word)].append(word)    

#print(word_dict)
dp=[float("INF") for _ in range(len(target))]
dp[0]=0

for i in range(1, len(target)) : # i에서 끝나고
    for key in word_dict : # key값
        prev_end = i - key # key 길이를 갖는 문자열 끝나는 부분
        if prev_end>=0 :
            for value in word_dict[key] :
                cost=calculate_cost(target[prev_end+1:i+1],value)
                dp[i]=min(dp[i], dp[prev_end]+cost)      
        
#print(dp)      
print(dp[-1] if dp[-1]!=float("INF") else -1)
