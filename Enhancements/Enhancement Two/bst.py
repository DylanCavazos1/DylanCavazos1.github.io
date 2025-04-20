from Course import Course

# Node class for the Binary Search Tree
class BSTNode:

    def __init__(self, course: Course):
        self.course = course # key
        self.left = None
        self.right = None


#Binary Search Tree Class

class BinarySearchTree:
    def __init__(self):
        self.root = None # create empty tree

    
    def insert(self, course: Course): 
        """
        Inserts Course object into the BST
        Referenced logic for node Insert from https://www.w3schools.com/dsa/dsa_data_binarysearchtrees.php
        """
        def _insert(node, course):# recursive function
            if not node: # if node doesn't exist, create new node with the course and return it
                return BSTNode(course)
            # Recursively go left if course_id is alphabetically smaller
            if course.course_id < node.course.course_id: 
                node.left = _insert(node.left, course) 
            else:  # Otherwise, go right
                node.right = _insert(node.right, course)
            return node # return the updated subtree root
        self.root = _insert(self.root, course) # starts insertion at root

   
    def in_order_traversal(self):
        """
        Performs in-order traversal in alphabetical order
        Referenced logic for In-order Traversal from https://www.w3schools.com/dsa/dsa_algo_binarytrees_inorder.php
        """
        result = [] # create an empty list to store the course results
        def _in_order(node): # recursive function
            if node:    # if the current node exists, then continue
                _in_order(node.left) # traverse down the left side first
                result.append(str(node.course)) # add the current course to the list of results - calls the __str__() method from my Course class
                _in_order(node.right) # Now traverse down the right side
        _in_order(self.root) # start recursion from the root of the tree
        return result # return the full list of sorted course strings 
    
    
    def search(self, course_id: str):
        """
        Searches for a specific course in the BST by course ID
        Referenced logic for searching through tree - https://www.w3schools.com/dsa/dsa_data_binarysearchtrees.php
        """
        # course_id string as input
        def _search(node, course_id): # recursive function 
            if not node: # if current branch ends and the course wasnt found return none
                return None
            if node.course.course_id == course_id: # checks if the current node's course_id matches the one we're searching
                return node.course # if it does then return that course object
            elif course_id < node.course.course_id: # if the course_id we're searching is less than the current node ID, 
                return _search(node.left, course_id) # then recursively search the left child node
            else: # if the course ID is greater, then search the right side
                return _search(node.right, course_id)
        return _search(self.root, course_id) # begin the recursive search

    
    def delete(self, course_id: str):
        """
        Deletes a course from the BST by course ID
        Referenced Delete logic & Case logic using - https://www.geeksforgeeks.org/deletion-in-binary-search-tree/
        """
        def _delete(node, course_id):
            # If node doesn't exist then return none
            if not node: 
                return None
            # Traverse the correct side of the tree
            # if course being deleted is alphabetically before current node, search left subtree
            if course_id < node.course.course_id:
                node.left = _delete(node.left, course_id)
            # if course being deleted is alphabetically after current node, search right subtree
            elif course_id > node.course.course_id:
                node.right = _delete(node.right, course_id)

            
            # Beginning of the 3 Cases:

            else:
                # CASE 1 - Node only has a right child or none - remove current node and connects parent to its right child
                if not node.left:
                    return node.right

                # CASE 2 - Node has no right child, return left child to replace node being deleted
                elif not node.right:
                    return node.left

                # CASE 3 - Node has 2 children - get the successor with inorder traversal
                # Need to find in-order successor
                min_larger_node = self.min_value_node(node.right)
                # Then copy the successor's course into node being deleted
                node.course = min_larger_node.course
                # recursively delete the successor node
                node.right = _delete(node.right, min_larger_node.course.course_id)

            return node
        # begins recursive deletion
        self.root = _delete(self.root, course_id)

    
    def min_value_node(self, node):
        """
        Finds node with smallest course ID in given subtree
        Used where a node has two children, and need to
        find the in-order successor
        """
        current = node
        while current.left: # keep going left to find the smallest value
            current = current.left
        return current

         