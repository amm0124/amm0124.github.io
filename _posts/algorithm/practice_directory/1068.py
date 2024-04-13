import sys
sys.setrecursionlimit(10**8)
def make_tree(parent) :
    global n
    tree=[[] for _ in range(n)]
    for i in range(n) :
        parent_node=parent[i] #i의 부모가 parent_node임
        if parent_node!=(-1) :
            tree[parent_node].append(i)
    return tree

def dfs(node):
    global tree,remove
    ans=0
    if tree[node]==None :
        return 0
    if tree[node]==[] or tree[node]==[remove ]: #leaf node
        return 1
    for i in tree[node]:
        ans+=dfs(i)
    return ans
    
n=int(input())
parent=list(map(int, sys.stdin.readline().split())) #i노드의 parent는 parent[i]임.
remove=int(input())
root=parent.index(-1)
tree=make_tree(parent)
answer=0
tree[remove]=None

if tree[root]==[remove] :
    print(1)
else:
    #print(tree)
    print(dfs(root))
