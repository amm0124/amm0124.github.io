import sys,copy
sys.setrecursionlimit(10**8)

def solution(index ,use_number) :
    global alphabet, alphabet_dict,answer,n
    
    if index==n :
        answer=max(answer, calculation(alphabet_dict))
        return answer    
        
    for i in range(10):
        if i not in use_number :
            #copy_ver=copy.deepcopy(use_number)
            alphabet_dict[alphabet[index]]=i
            solution(index+1, use_number.add(i))
            use_number.remove(i)

def calculation(number_dict):
    global arr
    result=0
    for string in arr :
        len_=len(string)
        for i in range(len_) :
            answer+=(10**(len_ - i))*number_dict[string[i]]
    return result

n=int(input())
arr=[sys.stdin.readline().strip() for _ in range(n)]
alphabet_dict=dict()
numbers=set([0 for _ in range(10)])
answer=0
for chars in arr :
    for char in chars :
        if char not in alphabet_dict :
            alphabet_dict[char]=-1
#print(alphabet_dict)
alphabet=list(alphabet_dict)

print(solution(0, set()))



# brute-force 
