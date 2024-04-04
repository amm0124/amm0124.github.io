import sys

def solution(b,matrix):
    if b==1 :
        return matrix
    elif b==2 :
        return matrix_multiplication(matrix, matrix)
    else : #n>=3
        if b&1==0 : #짝수
            result=solution(b//2, matrix)
            return matrix_multiplication(result, result)
        else :
            result=solution(b//2, matrix)
            return matrix_multiplication(matrix_multiplication(result, result), matrix)

        
#n*n matrix multiplication
def matrix_multiplication(matrix1, matrix2):
    global m
    n=len(matrix1)
    answer=[  [sum([matrix1[row][tmp]*matrix2[tmp][col] for tmp in range(n)] )%m   for col in range(n)] for row in range(n)  ]
    return answer


while True :
    #size, modulo base, power
    n,m,p=map(int, sys.stdin.readline().split())
    
    if n==0 and m==0 and p==0 :
        break
    
    matrix=[list(map(int, sys.stdin.readline().split())) for _ in range(n)] 
    result=solution(p,matrix)

    for row in result:
        print(*row)
    print('')
