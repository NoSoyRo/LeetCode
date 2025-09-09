from typing import List, Optional

# Definición típica de nodo de árbol
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class Solution:
    def bstFromPreorder(self, preorder: List[int]) -> List[Optional[int]]:
        # Función recursiva con límites
        self.i = 0
        def helper(bound=float('inf')) -> Optional[TreeNode]:
            if self.i == len(preorder) or preorder[self.i] > bound:
                return None
            root = TreeNode(preorder[self.i])
            self.i += 1
            root.left = helper(root.val)
            root.right = helper(bound)
            return root

        root = helper()
        return self.tree_to_array(root)

    # Convierte árbol a array BFS con None para huecos
    def tree_to_array(self, root: Optional[TreeNode]) -> List[Optional[int]]:
        if not root:
            return []
        res, queue = [], [root]
        while queue:
            node = queue.pop(0)
            if node:
                res.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                res.append(None)
        # Quitar Nones extra al final
        while res and res[-1] is None:
            res.pop()
        return res


# Ejemplo
preorder = [8, 5, 1, 7, 10, 12]
sol = Solution()
print(sol.bstFromPreorder(preorder))
