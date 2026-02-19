"""Binary Search Tree implementation with various operations."""


class TreeNode:
    """A node in the binary search tree."""
    
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree with insert, search, delete, and traversal operations."""
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, value):
        """Insert a value into the BST."""
        if self.root is None:
            self.root = TreeNode(value)
            self.size += 1
            return
        
        self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        """Helper for recursive insertion."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                self.size += 1
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
                self.size += 1
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        """Search for a value in the BST. Returns True if found."""
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        """Helper for recursive search."""
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def find_min(self):
        """Find minimum value in the tree."""
        if self.root is None:
            raise ValueError("Tree is empty")
        
        current = self.root
        while current.left is not None:
            current = current.left
        return current.value
    
    def find_max(self):
        """Find maximum value in the tree."""
        if self.root is None:
            raise ValueError("Tree is empty")
        
        current = self.root
        while current.right is not None:
            current = current.right
        return current.value
    
    def height(self):
        """Calculate the height of the tree."""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Helper for recursive height calculation."""
        if node is None:
            return 0
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return max(left_height, right_height) + 1
    
    def inorder_traversal(self):
        """Return list of values in inorder (sorted) order."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper for recursive inorder traversal."""
        if node is None:
            return
        
        self._inorder_recursive(node.left, result)
        result.append(node.value)
        self._inorder_recursive(node.right, result)
    
    def is_valid_bst(self):
        """Check if the tree is a valid BST."""
        return self._is_valid_recursive(self.root, float('-inf'), float('inf'))
    
    def _is_valid_recursive(self, node, min_val, max_val):
        """Helper for recursive BST validation."""
        if node is None:
            return True
        
        if not (min_val < node.value < max_val):
            return False
        
        return (self._is_valid_recursive(node.left, min_val, node.value) and
                self._is_valid_recursive(node.right, node.value, max_val))
    
    def count_nodes(self):
        """Count total number of nodes in the tree."""
        return self._count_recursive(self.root)
    
    def _count_recursive(self, node):
        """Helper for recursive node counting."""
        if node is None:
            return 0
        
        return 1 + self._count_recursive(node.left) + self._count_recursive(node.right)
    
    def level_order_traversal(self):
        """Return list of values in level order (BFS)."""
        if self.root is None:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result