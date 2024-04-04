import sys,copy
sys.setrecursionlimit(10**8)

def calculation(number_dict):
    global arr
    result=0
    for string in arr :
        len_=len(string)
        for i in range(len_) :
            result+=(10**(len_ - i))*number_dict[string[i]]
    return result

def solution(index,use_number) :
    global depth,answer
    if index==depth:
        answer=max(answer, calculation(alphabet_dict))
        return 
    
    for i in range(10) :
        if i not in use_number :
            alphabet_dict[alphabet[index]]=i
            use_number.add(i)
            solution(index+1, use_number)
            use_number.remove(i)
    
    
n=int(input())
arr=[sys.stdin.readline().strip() for _ in range(n)]
alphabet_dict=dict()
answer=0
for chars in arr :
    for char in chars :
        if char not in alphabet_dict :
            alphabet_dict[char]=-1
alphabet=list(alphabet_dict) #문자 저장
depth=len(alphabet)
tmp=set()

for i in range(10) :
    alphabet_dict[alphabet[0]]=i
    solution(1, {i})
    
print(answer)



# brute-force 
