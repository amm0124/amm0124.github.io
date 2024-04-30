import sys

n=int(input())
word_count=dict()
answer=0

for _ in range(n) :
    word = sys.stdin.readline().strip()
    word = word[::-1]
    for i in range(len(word)) :
        if word[i] not in word_count :
            word_count[word[i]]=0
        word_count[word[i]]+=10**i
        
word_count = sorted(word_count.items(), key=lambda item:item[1], reverse=True)
num=9

for word in word_count:
    answer+=word[1]*num
    num-=1
print(answer)



