import sys
sys.setrecursionlimit(10**9)

def preorder_traverse(root):
    global tree
    
    if root=='.':
        return ""
    return root + preorder_traverse(tree[root][0]) + preorder_traverse(tree[root][1])

def inorder_traverse(root):
    global tree
    
    if root=='.' :
        return ""
    return inorder_traverse(tree[root][0]) + root + inorder_traverse(tree[root][1])
    
def postorder_traverse(root):
    global tree
    
    if root=='.' :
        return ""
    else :
        return postorder_traverse(tree[root][0]) + postorder_traverse(tree[root][1]) + root 

n=int(input())
tree=dict()
for _ in range(n) :
    query=list(sys.stdin.readline().split())
    tree[query[0]] = (query[1], query[2])

print(preorder_traverse('A'))
print(inorder_traverse('A'))
print(postorder_traverse('A'))

