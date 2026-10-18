from __future__ import annotations

import math


class BTreeNode:
    def __init__(self, order: int, leaf=False):
        self.order: int = (
            order  # order of the btree to tell how many keys can fit in a node
        )

        self.leaf: bool = leaf  # boolean for leaf node
        self.keys: list[int] = []  # list of keys in the node
        self.values: list[
            str
        ] = []  # list of values in the node matching the index of keys in the self.keys:list
        self.children: list[BTreeNode] = []  # list of child nodes
        self.parent: BTreeNode | None = None

    # Node could have some helper function for information in nodes
    # as the nodes have key/value pairs

    def is_full(self):
        return len(self.keys) == self.order

    def get_size(self):
        return len(self.keys)

    def get_keyvalue(self, key):
        if key in self.keys:
            return self.values[self.keys.index(key)]
        return None

    def set_keyvalue(self, key, value):
        """
        Set the key and value insertion in sorted matter
        keeping data consistency by adding the value as the same index as the
        """
        # append the element in list and make it sorted
        if not self.is_full():
            if len(self.keys) != len(self.values):
                raise ValueError("keys and values lists must be the same length")

            if key in self.keys:
                raise ValueError("INDEX KEY ALREADY EXISTS")
            self.keys.append(key)
            self.keys.sort()
            # find the index of the keys
            idx = self.keys.index(key)
            self.values.insert(idx, value)

        else:
            raise ValueError("Node is full")

    def set_children(self, node: BTreeNode, idx: int):
        if len(self.children) < (self.order + 1):
            # if element is already there in the children list, replace it
            if idx < len(self.children):
                self.children[idx] = node
            else:
                self.children.append(node)
        else:
            raise ValueError("Cannot have more children")

    @property
    def is_leaf(self):
        return not self.children

    def __str__(self):
        return f"keys: {self.keys}, values: {self.values}"

    def __repr__(self):
        return f"(keys: {self.keys}, values: {self.values})"


class HeaderPageInfo:
    root_page_id: BTreeNode = None


class BTreeMap:
    def __init__(self, order: int):
        self.order = order
        self.root: BTreeNode = None
        # tree property
        self.minimal_keys: int = 2 * ((math.ceil(self.order - 1) / 2) - 1)
        self.maximal_keys: int = self.order
        self.minimal_children: int = math.ceil(self.order / 2)
        self.maximal_children: int = self.order + 1

        # print(
        #     f"order: {self.order}, minimal_keys: {self.minimal_keys}, maximal_keys: {self.maximal_keys}, minimal_children: {self.minimal_children}, maximal_children: {self.maximal_children}"
        # )

    def insert(self, key, value):
        # if BTree is empty
        if self.root is None:
            root_node = BTreeNode(self.order)
            self.root = root_node
            HeaderPageInfo.root_page_id = root_node
            # insert the key and value
            root_node.set_keyvalue(key, value)
        else:
            # search for element with key for where it would go in a leaf of the tree
            node = self.root
            while not node.is_leaf:
                for idx in range(len(node.keys)):
                    if node.keys[idx] > key:
                        node = node.children[idx]
                        break
                    elif idx == len(node.keys) - 1:
                        node = node.children[idx + 1]
                        break

            # we found the node here where we have to insert
            # check if node is full or not
            if not node.is_full():
                # insert the key simply
                node.set_keyvalue(key, value)
            else:
                self._handle_overflow(node, key, value)

    def _handle_overflow(self, node: BTreeNode, key: int, value: int):
        # if node is the root and not full
        # insert the key, value pair in node and then split the node at median
        # don't use setter method as it raises exception
        node.keys.append(key)
        node.keys.sort()
        idx = node.keys.index(key)
        node.values.insert(idx, value)

        # split the node into left_node, median and right_node
        left_node = BTreeNode(self.order, node.leaf)
        right_node = BTreeNode(self.order, node.leaf)
        median = len(node.keys) // 2
        left_node.keys = node.keys[:median]
        right_node.keys = node.keys[median + 1 :]
        left_node.values = node.values[:median]
        right_node.values = node.values[median + 1 :]
        mkey = node.keys[median]
        mvalue = node.values[median]

        if node.children:
            left_node.children = node.children[: median + 1]
            right_node.children = node.children[median + 1 :]
            for c in left_node.children:
                c.parent = left_node
            for c in right_node.children:
                c.parent = right_node

        if node.parent is None:
            new_root_node = BTreeNode(self.order, False)
            new_root_node.keys = [mkey]
            new_root_node.values = [mvalue]
            new_root_node.children = [left_node, right_node]
            left_node.parent = new_root_node
            right_node.parent = new_root_node
            self.root = new_root_node
            HeaderPageInfo.root_page_id = new_root_node
            return

        # node.parent is full
        idx = node.parent.children.index(node)
        node.parent.children[idx : idx + 1] = [left_node, right_node]
        left_node.parent = node.parent
        right_node.parent = node.parent

        if not node.parent.is_full():
            # append the key into node.parent.keys
            # then sort it
            # then add the value at the same index of key
            # then set the children appropirately as
            node.parent.keys.append(mkey)
            node.parent.keys.sort()
            idx = node.parent.keys.index(mkey)
            node.parent.values.insert(idx, mvalue)
            return

        else:
            self._handle_overflow(node.parent, mkey, mvalue)

    def delete(self, key: int):
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #   We have to maintain the property of btree of Order (m)
        #   min_no_of_children = ceil(m/2)
        #   max_no_of_children = m + 1
        #   min_no_of_keys_in_node = 2(ceil(m/2) - 1)
        #   max_no_of_keys_in_node = m
        #  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # locate the node which contains the key
        # check if it is leaf or not
        # search operation ---------------------------------------------------------------------------
        node = self.root
        found = False
        while not found:
            if key in node.keys:
                found = True
            else:
                for idx in range(len(node.keys)):
                    if node.keys[idx] > key:
                        node = node.children[idx]
                        break
                    elif idx == len(node.keys) - 1:
                        node = node.children[idx + 1]
                        break

        # --------------------------------------------------------------------------------------------------------------
        # #############################################################################################################
        # --------------------------------------------------------------------------------------------------------------
        if node is not None:
            # __________________________________________________________________________________________________________#
            # If the key in the leaf node:#

            if node.is_leaf:
                if len(node.keys) > self.minimal_keys:
                    # print("yes node is leaf")
                    # delete it noramlly from corresponding arrays the
                    # key contain value corresponding to it in the self.values
                    idx = node.keys.index(key)
                    node.keys.remove(key)
                    node.values.remove(node.values[idx])

                else:
                    # now we have to call the function we have created to handle underflow
                    # print("called underflow")
                    self._handle_underflow(node, key)

            else:
                # case1: replace the delkey  with inorder predecessor
                # get the index of the element in the node
                # print(f"Node is internal and node is found in:{node}")
                idx_location = node.keys.index(key)
                # print(f"idx_location: {idx_location}")
                
                leaf = None
                replace_key = None
                
                pre_leaf, pre_replace_key = self._get_inorder_predecessor(
                    node, idx_location
                )
                

                if len(pre_leaf.keys) <= self.minimal_keys:
                    succ_leaf, succ_replace_key = self._get_inorder_successor(
                        node, idx_location
                    )
                    if len(succ_leaf.keys) > self.minimal_keys:
                        leaf, replace_key = succ_leaf, succ_replace_key

                    else:
                        leaf, replace_key = pre_leaf, pre_replace_key

                else:
                    leaf, replace_key = pre_leaf, pre_replace_key
                
                # print(f"leaf: {leaf}, replace_key: {replace_key}")
                
                idx = leaf.keys.index(replace_key)
                node.keys[idx_location] = leaf.keys.pop(idx)
                node.values[idx_location] = leaf.values.pop(idx)
                # print(f"node: {node}")
                self._rebalance(leaf)

        else:
            raise KeyError(f"Key {key} not found")

    def _get_index(self, node: BTreeNode):
        idx = node.parent.children.index(node)
        left_sibling: BTreeNode | None = None
        right_sibling: BTreeNode | None = None
        separator_idx: int | None = None

        if idx > 0:
            left_sibling = node.parent.children[idx - 1]
            separator_idx = idx - 1

        if idx < len(node.parent.keys) - 1:
            right_sibling = node.parent.children[idx + 1]
            separator_idx = idx

        return left_sibling, right_sibling, separator_idx
        
    def _rebalance(self, node):
        # print(f"Now we are in rebalance node with node: {node}")
        # print(f'parent:{node.parent}')
        # According to WikiPedia Algorithm for rebalancing after deletion
        if node.parent is None:
            if node.get_size() == 0 and (len(node.children) == 1):
                # make children new root
                node.children[0].parent = None
                self.root = node.children[0]
                HeaderPageInfo.root_page_id = self.root
                return
            return

        parent = node.parent
        idx = parent.children.index(node)
        left_sibling, right_sibling, sep_idx = self._get_index(node)
        # print(f"parent: {parent}, left_sibling: {left_sibling}, right_sibling: {right_sibling}, sep_idx: {sep_idx}")
        if len(node.keys) >= self.minimal_keys:
                return

        
        if right_sibling and len(right_sibling.keys) > self.minimal_keys:
            # Copy the separator from the parent to the end of the deficient node (the separator moves down; the deficient node now has the minimum number of elements)
            node.keys.append(parent.keys[sep_idx])
            node.keys.sort()
            idx = node.keys.index(parent.keys[sep_idx])
            node.values.insert(idx, parent.values[sep_idx])
            if right_sibling.children:
                # change the parent of the last children to the right_node
                right_sibling.children[0].parent = node
                # pop the child from the right_node
                # add the child at the very end index of the node's children
                node.children.insert(-1, right_sibling.children.pop(0))
            # Replace the separator in the parent with the first element of the right sibling (right sibling loses one node but still has at least the minimum number of elements) 
            parent.keys[sep_idx] = right_sibling.keys.pop(0)
            parent.values[sep_idx] = right_sibling.values.pop(0)

        elif left_sibling and len(left_sibling.keys) > self.minimal_keys:
            # Copy the separator from the parent to the start of the deficient node (the separator moves down; deficient node now has the minimum number of elements)
            sep_idx-=1
            node.keys.append(parent.keys[sep_idx])
            node.keys.sort()
            idx = node.keys.index(parent.keys[sep_idx])
            node.values.insert(idx, parent.values[sep_idx])
            if left_sibling.children:
                # change the parent of the last children to the right_node
                left_sibling.children[-1].parent = node
                # pop the child from the left_node
                # add the children at the very first index
                node.children.insert(0, left_sibling.children.pop())
            # Replace the separator in the parent with the first element of the left sibling (left sibling loses one node but still has at least the minimum number of elements)
            parent.keys[sep_idx] = left_sibling.keys.pop()
            parent.values[sep_idx] = left_sibling.values.pop()
            
        else:
            # if both immediate siblings have only the minimum number of elements, then merge with a sibling sandwiching their separator taken off from their parent. 
            # Copy the separator to the end of the left node (the left node may be the deficient node, or it may be the sibling with the minimum number of elements)
            # left_sibling.keys.append(parent.keys[sep_idx])
            # left_sibling.keys.sort()
            # idx = left_sibling.keys.index(parent.keys[sep_idx])
            # left_sibling.values.insert(idx, parent.values[sep_idx])

            # # Move all elements from the right node to the left node (the left node now has the maximum number of elements, and the right node is empty)
            # left_sibling.keys.extend(right_sibling.keys)
            # left_sibling.values.extend(right_sibling.values)
        
            # right_sibling.keys.clear()
            # right_sibling.values.clear()

            # # Remove the separator from the parent along with its empty right child (the parent loses an element) 
            # parent.keys.pop(sep_idx)
            # parent.values.pop(sep_idx)
            # parent.children.pop(sep_idx + 1)
            # merge: always merge into the left one of the pair
            if left_sibling:
                l, r, sep = left_sibling, node, idx - 1
            else:
                l, r, sep = node, right_sibling, idx
            l.keys.append(parent.keys[sep])
            l.values.append(parent.values[sep])
            l.keys.extend(r.keys)
            l.values.extend(r.values)
            for c in r.children:       # move children too
                c.parent = l
            l.children.extend(r.children)
            parent.keys.pop(sep)
            parent.values.pop(sep)
            parent.children.pop(sep + 1)
        
        if len(parent.keys) < self.minimal_keys:
            self._rebalance(parent)

    def _get_min_subtree(self, node: BTreeNode, idx_location):
        curr = node.children[idx_location + 1]
        while not curr.is_leaf:
            curr = curr.children[0]

        return curr, curr.keys[0]

    def _get_max_subtree(self, node: BTreeNode, idx_location: int) -> int:
        cur = node.children[idx_location]  # root of the left subtree
        while not cur.is_leaf:
            cur = cur.children[-1]  # keep going to the rightmost child
        # check if `cur` node have more than minimal keys
        return cur, cur.keys[-1]

    def _get_inorder_predecessor(self, node: BTreeNode, idx_location: int):
        # to get the inorder predecessor of the given key which resides in the `node`
        # inorder predecessor: the largest element in the left subtree of the key in the node

        return self._get_max_subtree(node, idx_location)

    def _get_inorder_successor(self, node: BTreeNode, idx_location: int):
        # to get the inorder successor of the given key which resides in the `node`
        # inorder successor: the smallest element in the right subtree of the key in the node

        return self._get_min_subtree(node, idx_location)

    

    def _merge(
        self,
        left_node: BTreeNode,
        right_node: BTreeNode,
        parent: BTreeNode,
        separator_index: int,
        target_key: int | None = None,
    ):
        """
        Merge right_node to left_node and delete the right_node from the child pointer in node.parent.children pointer array.

        This merging is only used if both `left_sibling`, `right_sibling` and the `node` itself having miniaml_keys and
        siblings not able to give the key to node
        so merging is always favoured for the `left_sibling` if exists otherwise `right_sibling`

        `This method also removes the key from the btree node`
        """
        # pull down the element from parent to left_node
        separator_key = parent.keys[separator_index]

        parent.keys.remove(separator_key)

        left_node.keys.append(separator_key)
        left_node.values.append(parent.values[separator_index])
        parent.values.remove(parent.values[separator_index])

        # merge right_node with left_node
        left_node.keys.extend(right_node.keys)
        left_node.values.extend(right_node.values)
        # delete the right node from node.parent.children
        parent.children.remove(right_node)
        if target_key is not None:
            idx = left_node.keys.index(target_key)
            left_node.keys.remove(target_key)
            left_node.values.remove(left_node.values[idx])

    def _borrow_from(
        self,
        node: BTreeNode,
        parent: BTreeNode,
        sep_idx: int,
        delkey: int,
        left_node: BTreeNode | None = None,
        right_node: BTreeNode | None = None,
    ):
        # print(node)
        if (left_node is None) and (right_node is not None):
            # borrow from right_node
            borrowed_key = right_node.keys.pop(0)
            borrowed_val = right_node.values.pop(0)
            if right_node.children:
                # change the parent of the last children to the right_node
                right_node.children[0].parent = node
                # pop the child from the right_node
                # add the child at the very end index of the node's children
                node.children.insert(-1, right_node.children.pop(0))
            node.keys.append(parent.keys[sep_idx])
            node.keys.sort()
            idx = node.keys.index(parent.keys[sep_idx])
            node.values.insert(idx, parent.values[sep_idx])

            if delkey is not None:
                idx = node.keys.index(delkey)
                node.keys.remove(delkey)

                node.values.remove(node.values[idx])

            parent.keys[sep_idx] = borrowed_key
            parent.values[sep_idx] = borrowed_val

        elif (left_node is not None) and (right_node is None):
            # borrow from left_node
            borrowed_key = left_node.keys.pop()
            borrowed_val = left_node.values.pop()

            if left_node.children:
                # change the parent of the last children to the right_node
                left_node.children[-1].parent = node
                # pop the child from the left_node
                # add the children at the very first index
                node.children.insert(0, left_node.children.pop())
            node.keys.append(parent.keys[sep_idx])
            node.keys.sort()
            idx = node.keys.index(parent.keys[sep_idx])
            node.values.insert(idx, parent.values[sep_idx])

            if delkey is not None:
                idx = node.keys.index(delkey)
                node.keys.remove(delkey)

                node.values.remove(node.values[idx])

            parent.keys[sep_idx] = borrowed_key
            parent.values[sep_idx] = borrowed_val

        else:
            raise ValueError(
                "Cannot borrow from both left and right nodes. Use _merge() for other reasons"
            )

    def _handle_underflow(self, node: BTreeNode, delkey=None):
        # if node is root, do nothing
        if node.parent is None:
            if node.get_size() == 0 and (len(node.children) == 1):
                # make children new root
                node.children[0].parent = None
                self.root = node.children[0]
                HeaderPageInfo.root_page_id = self.root
                return
            return

        parent = node.parent
        left_sibling, right_sibling, sep_idx = self._get_index(node)
        # print(
        #     f"node: {node}, parent: {parent}, left_sibling: {left_sibling}, right_sibling: {right_sibling}, sep_idx: {sep_idx}"
        # )

        # prefer borrowing first
        if (left_sibling is not None) and len(left_sibling.keys) > self.minimal_keys:
            # borrow from left_sibling
            self._borrow_from(
                node, parent, sep_idx, delkey=delkey, left_node=left_sibling
            )
            return

        if (right_sibling is not None) and len(right_sibling.keys) > self.minimal_keys:
            # borrow from right_sibling
            self._borrow_from(
                node, parent, sep_idx, delkey=delkey, right_node=right_sibling
            )
            return

        # merging
        if left_sibling is not None:
            # print("called _merge to left_sibling")
            self._merge(left_sibling, node, parent, sep_idx, target_key=delkey)
        if right_sibling is not None:
            # print("called _merge to right_sibling")
            self._merge(node, right_sibling, parent, sep_idx, target_key=delkey)

        if len(parent.keys) < self.minimal_keys:
            self._handle_underflow(parent)
