"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log, floor
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)

            return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift(top):
            '''
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            '''
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    @property
    def root(self):
        '''
        Returns the root of the tree.
        '''
        return self._root

    @root.setter
    def root(self, other):
        self._root = other

    def children(self, position):
        '''
        Retunrs a list of children of the node on a given position.
        '''
        children = []
        if position is not None:
            if position.left is not None:
                children.append(position.left)
            if position.right is not None:
                children.append(position.right)

        return children

    def num_children(self, position):
        '''
        Returns a number of children of the node on a given position.
        '''
        if position is None:
            return False

        number = 2
        if position.left is None:
            number -= 1
        if position.right is None:
            number -= 1

        return number

    def is_leaf(self, position):
        '''
        Returns if the given node is a leaf.
        '''
        return self.num_children(position) == 0

    def is_root(self, position):
        '''
        Returns if a given node is a root.
        '''
        return position == self.root

    def height(self, position = None):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(position):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self.is_leaf(position):
                return 0

            return 1 + max(height1(child) for child in self.children(position))

        if position is None:
            position = self.root

        return height1(position)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        number = len(list(self.inorder()))
        return self.height() < 2 * log(number + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        items = []
        for node_item in self.inorder():
            if node_item in range(low, high + 1):
                items.append(node_item)

        return items

    def _subtree_inorder(self, position = None):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if position is None:
            position = self.root

        if position.left is not None: # if left child exists, traverse its subtree
            for other in self._subtree_inorder(position.left):
                yield other
        yield position # visit p between its subtrees
        if position.right is not None: # if right child exists, traverse its subtree
            for other in self._subtree_inorder(position.right):
                yield other

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        items = self._subtree_inorder()
        items = list(sorted([item.data for item in items]))
        self.clear()
        lenght = len(items) - 1
        self.root = BSTNode(items.pop(floor(lenght/2)))

        nodes = [self.root]
        new_nodes = []
        while lenght > 0:
            for node in nodes:
                if lenght == 0:
                    break
                node.left = BSTNode(items.pop(floor(lenght/2)))
                lenght -= 1

                if lenght == 0:
                    break
                node.right = BSTNode(items.pop(floor(lenght/2)))
                lenght -=1

                new_nodes += [node.left, node.right]

            nodes = new_nodes

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        successor = None
        for node_item in self.inorder():
            if node_item > item:
                if successor is None:
                    successor = node_item
                if node_item < successor:
                    successor = node_item

        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        predecessor = None
        for node_item in self.inorder():
            if node_item < item:
                if predecessor is None:
                    predecessor = node_item
                if node_item > predecessor:
                    predecessor = node_item

        return predecessor
