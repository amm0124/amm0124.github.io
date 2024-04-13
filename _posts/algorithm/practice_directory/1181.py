import sys

n=int(input())
words=[0 for _ in range(n)]
for _ in range(n) : 
    word=sys.stdin.readline().rstrip()
    words[_] = word
words=list(set(words))
words.sort()
words.sort(key=len)
for word in words :
    print(word)