"""Tests for Binary Search Tree implementation."""

import unittest
from binary_search_tree import BinarySearchTree, TreeNode


class TestBSTInsertAndSize(unittest.TestCase):
    
    def test_insert_single(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertEqual(bst.size, 1)
    
    def test_insert_multiple(self):
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)
        self.assertEqual(bst.size, 3)
    
    def test_insert_duplicates_not_counted(self):
        """Duplicates should not increase size."""
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(10)
        self.assertEqual(bst.size, 1)


class TestBSTSearch(unittest.TestCase):
    
    def setUp(self):
        self.bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.insert(val)
    
    def test_search_existing_root(self):
        self.assertTrue(self.bst.search(10))
    
    def test_search_existing_left(self):
        self.assertTrue(self.bst.search(5))
    
    def test_search_existing_right(self):
        self.assertTrue(self.bst.search(15))
    
    def test_search_existing_deep(self):
        self.assertTrue(self.bst.search(3))
        self.assertTrue(self.bst.search(20))
    
    def test_search_not_existing(self):
        self.assertFalse(self.bst.search(100))
        self.assertFalse(self.bst.search(0))


class TestBSTMinMax(unittest.TestCase):
    
    def test_find_min(self):
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)
        self.assertEqual(bst.find_min(), 3)
    
    def test_find_max(self):
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)
        self.assertEqual(bst.find_max(), 20)
    
    def test_find_min_empty_raises(self):
        bst = BinarySearchTree()
        with self.assertRaises(ValueError):
            bst.find_min()
    
    def test_find_max_empty_raises(self):
        bst = BinarySearchTree()
        with self.assertRaises(ValueError):
            bst.find_max()


class TestBSTHeight(unittest.TestCase):
    
    def test_height_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.height(), 0)
    
    def test_height_single_node(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertEqual(bst.height(), 1)
    
    def test_height_balanced(self):
        bst = BinarySearchTree()
        for val in [10, 5, 15]:
            bst.insert(val)
        self.assertEqual(bst.height(), 2)
    
    def test_height_unbalanced(self):
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)
        self.assertEqual(bst.height(), 3)


class TestBSTTraversal(unittest.TestCase):
    
    def test_inorder_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.inorder_traversal(), [])
    
    def test_inorder_sorted(self):
        """Inorder traversal should return sorted values."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)
        self.assertEqual(bst.inorder_traversal(), [3, 5, 7, 10, 12, 15, 20])


class TestBSTValidation(unittest.TestCase):
    
    def test_is_valid_bst_true(self):
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)
        self.assertTrue(bst.is_valid_bst())
    
    def test_is_valid_bst_empty(self):
        bst = BinarySearchTree()
        self.assertTrue(bst.is_valid_bst())


class TestBSTCountNodes(unittest.TestCase):
    
    def test_count_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.count_nodes(), 0)
    
    def test_count_single(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertEqual(bst.count_nodes(), 1)
    
    def test_count_multiple(self):
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)
        self.assertEqual(bst.count_nodes(), 5)


class TestBSTLevelOrder(unittest.TestCase):
    
    def test_level_order_empty(self):
        bst = BinarySearchTree()
        self.assertEqual(bst.level_order_traversal(), [])
    
    def test_level_order_single(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertEqual(bst.level_order_traversal(), [10])
    
    def test_level_order_multiple(self):
        """Level order should return values level by level, left to right."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)
        # Tree structure:
        #       10
        #      /  \
        #     5    15
        #    / \
        #   3   7
        # Level order: 10, 5, 15, 3, 7
        self.assertEqual(bst.level_order_traversal(), [10, 5, 15, 3, 7])


if __name__ == "__main__":
    unittest.main()
