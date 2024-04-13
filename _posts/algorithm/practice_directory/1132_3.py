import sys,copy
sys.setrecursionlimit(10**8)

def solution(index, use_number):
    global depth, answer
    if index == depth:
        answer = max(answer, calculation(alphabet_dict))
        return
    
    for i in range(10):
        if i not in use_number:
            alphabet_dict[alphabet[index]] = i
            new_use_number = use_number | {i}  # 새로운 set을 생성하여 사용
            solution(index + 1, new_use_number)

def calculation(number_dict):
    global arr
    result=0
    for string in arr :
        len_=len(string)
        for i in range(len_) :
            result+=(10**(len_ - i))*number_dict[string[i]]
    return result

n = int(input())
arr = [sys.stdin.readline().strip() for _ in range(n)]
alphabet_dict = dict()
answer = 0
for chars in arr:
    for char in chars:
        if char not in alphabet_dict:
            alphabet_dict[char] = -1
alphabet = list(alphabet_dict.keys())  # keys() 메소드를 사용하여 키 리스트 생성
depth = len(alphabet)

for i in range(10):
    alphabet_dict[alphabet[0]] = i
    solution(1, {i})

print(answer)
