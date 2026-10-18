"""

B+Tree:
    - The B+Tree only stores values in `leaf` nodes. Inner
    nodes only guide the search process.
    - A deleted key must be removed from the leaf node, but it may
    still exist in inner nodes.

B+Tree Design choices:
    - Node Size
    - Merge Threshold
    - Variable-Length Keys
    - Intra-Node Search
"""

from __future__ import annotations

import math
from typing import Any


class HeaderInfoPage:
    root_page_id: BPlusNode = None


class BPlusNode:
    def __init__(self, order: int, leaf: bool):
        self.order = order
        self.leaf = leaf
        self.keys: list[Any] = []
        self.children: list[BPlusNode] = []
        self.parent: BPlusNode | None = None

        if self.leaf:
            self.values: list[Any] = []
            self.prev_leaf: BPlusNode = None
            self.next_leaf: BPlusNode = None

    # //-- helper function for BPlusNode -- //
    def is_leaf(self):
        return self.leaf

    def is_full(self):
        """
        True if node is full otherwise False
        """
        return len(self.keys) >= self.order

    def is_root(self):
        return self.parent is None

    def get_size(self):
        return len(self.keys)

    def get_parent(self):
        return self.parent

    # only use these two helper methods if the node is leaf
    # if it is not leaf node then it will throw the error
    #
    def get_next_leaf(self):
        return self.next_leaf

    def get_prev_leaf(self):
        return self.prev_leaf

    def __str__(self):
        return f"BPlusNode(order={self.order}, leaf={self.leaf}, keys={self.keys}, cs= {self.children})"

    def __repr__(self):
        return self.__str__()

    def _insert_element(self, key: Any, value: Any):
        if self.leaf:
            self.keys.append(key)
            self.keys.sort()
            idx = self.keys.index(key)
            self.values.insert(idx, value)

        else:
            raise KeyError(
                "You are trying to insert (key, value) pair in non-leaf node which cannot be possible.This method is not designed for this purpose !!!"
            )

    def _delete(self, key: Any):
        # remove the key from keys and corresponding value
        idx = self.keys.index(key)
        self.keys.remove(key)
        self.values.pop(idx)

    def _get_siblings(self):
        # self index in parent's children list
        self_idx = self.parent.children.index(self)
        print(f'\nself_idx: {self_idx}\n')
        left_s: BPlusNode | None = None
        right_s: BPlusNode | None = None
        sep_idx: int | None = None
        if self_idx > 0:
            left_s = self.prev_leaf
            sep_idx = self_idx - 1

        if self_idx <= len(self.parent.keys) - 1:
            right_s = self.next_leaf
            sep_idx = self_idx
        return left_s, right_s, sep_idx

    def _borrow_from(
        self,
        sep_idx: int,
        left_s: BPlusNode | None = None,
        right_s: BPlusNode | None = None,
    ):
        if left_s is None:
            # borrow from right_s
            borrow_key = right_s.keys.pop(0)
            borrow_value = right_s.values.pop(0)

            # both self and right_s are leaf node
            self.keys.append(borrow_key)
            self.values.append(borrow_value)
            if right_s.children:
                right_s.children[0].parent  = self

                self.children.insert(-1, right_s.children.pop(0))
            # replace the parent.keys[sep_idx] with current right_s[0]
            self.parent.keys[sep_idx] = right_s.keys[0]


class BPlusTreeMap:
    def __init__(self, order: int):
        self.order = order
        self.header = HeaderInfoPage()
        self.root = BPlusNode(order, True)

        self.header.root_page_id = self.root
        self._median = math.ceil(self.order // 2)

    @property
    def get_min_keys(self):
        return math.ceil((self.order) / 2)

    @property
    def get_min_children(self):
        return math.ceil((self.order) / 2) + 1

    @property
    def get_max_children(self):
        return self.order + 1

    @property
    def get_max_keys(self):
        return self.order

    def _leaf_search(self, key, node: BPlusNode):
        if node.is_leaf():
            return node

        node_children = node.children
        node_keys = node.keys
        for i, bound_key in enumerate(node_keys):
            if key < bound_key:
                return self._leaf_search(key, node_children[i])

        return self._leaf_search(key, node_children[node.get_size()])

    def _search(self, key):
        """
        Used for both insert() and delete() operations to search for appropirate node

        In insert() case:
            - If key_exists=True then `key` already exists and insert will throw KeyError Exception
            - If key_exists=False then insert() function will add the `key` in that `leaf` with handling overflow

        In delete() case:
           - for delete operation to work key must exists in first place otherwise key_exists=False will be the result
           - So key_exists=True is mandate for delete() operation to use this search functionality
        """
        leaf = self._leaf_search(key, node=self.root)
        for leaf_key in leaf.keys:
            if key == leaf_key:
                return True, leaf
        return False, leaf

    def _handle_overflow(self, node: BPlusNode, key: Any, value: Any):
        # We have already inserted the element in node and that causes overflow it's function is to handle that overflow
        # Case1: insertion is in leaf
        # Case2: insertion is in Internal Node
        # Case3: Insertion in root node and causes split
        node._insert_element(key, value)
        # Case 1: Insertion in Leaf Node
        while node and len(node.keys) > self.order:
            parent = node.get_parent()

            if node.is_root():
                new_root = BPlusNode(order=self.order, leaf=False)
                right_node = BPlusNode(order=self.order, leaf=node.leaf)

                push_key = node.keys[self._median]
                right_node.keys = node.keys[self._median + 1 :]
                right_node.children = node.children[self._median + 1 :]

                del node.keys[self._median :]
                del node.children[self._median + 1 :]

                for child in right_node.children:
                    child.parent = right_node

                new_root.keys.append(push_key)
                new_root.children.extend([node, right_node])
                node.parent = new_root
                right_node.parent = new_root

                self.root = new_root
                self.header.root_page_id = new_root

                break

            else:
                push_key: Any = None
                right_node = BPlusNode(order=self.order, leaf=node.leaf)
                if node.is_leaf():
                    # split the node keys and values at median

                    right_node.keys = node.keys[self._median :]
                    right_node.values = node.values[self._median :]

                    del node.keys[self._median :]
                    del node.values[self._median :]

                    # Update leaf pointers
                    right_node.prev_leaf = node
                    right_node.parent = node.parent
                    right_node.next_leaf = node.next_leaf
                    if right_node.next_leaf:
                        right_node.next_leaf.prev_leaf = right_node
                    node.next_leaf = right_node

                    push_key = right_node.keys[0]

                else:
                    push_key = node.keys[self._median]
                    # split the node keys and values at median
                    right_node.keys = node.keys[self._median + 1 :]
                    right_node.children = node.children[self._median + 1 :]

                    del node.keys[self._median :]
                    del node.children[self._median + 1 :]

                    for c in right_node.children:
                        c.parent = right_node

                parent.keys.append(push_key)
                parent.keys.sort()
                idx = parent.keys.index(push_key)
                parent.children.insert(idx + 1, right_node)
                right_node.parent = parent

            node = parent

    def insert(self, key: Any, value: Any):
        # search for the appropirate node to insert
        # if key already exists what we are searching
        # we have handle that case also
        key_exists, leaf = self._search(key)

        if key_exists:
            raise ValueError("Key already exists can't add same key twice!!!")

        else:
            # key found is guranteed leaf and we need to insert the key & value in the
            # leaf if it is not full and otherwise check if it needs splitting
            if not leaf.is_full():
                # insert the element simply
                leaf._insert_element(key, value)

            # insert the new record and split the node at the median
            # `copy` the median element to the parent and insert new node to the parent
            # repeat until a parent is found which need no spliting
            # at root is our first split
            elif leaf.is_root() and leaf.is_full():
                # If the root splits,
                # treat it as if it has an empty parent and split as outlined below in the insertion case
                # create a new node to point as a new root and the parent of current root leaf as the
                # update the pointers first
                new_root = BPlusNode(
                    order=self.order, leaf=False
                )  # as the root cannot be leaf now
                leaf.parent = new_root

                # now add the element in leaf
                leaf._insert_element(key, value)
                median = leaf.keys[self._median]
                # split the node keys and values at median
                right_node = BPlusNode(order=self.order, leaf=True)
                right_node.keys = leaf.keys[self._median :]
                right_node.values = leaf.values[self._median :]

                # delete the keys and values from leaf as they are inserted in right_node
                del leaf.keys[self._median :]
                del leaf.keys[self._median :]

                # copy the median to the new_root
                new_root.keys.append(median)

                # update the pointers carefully
                # make the leaf, right_node as new children of new_root
                new_root.children.extend([leaf, right_node])

                # new_root will be the parent of right_node
                right_node.parent = new_root

                # linked leafs pointer updates
                leaf.next_leaf = right_node
                right_node.prev_leaf = leaf

                # update the BTreeMap main properties
                self.root = new_root

            else:
                self._handle_overflow(leaf, key, value)

    def _handle_underflow(self, node: BPlusNode):
        # left_sibling and right_sibling are those sibling which belongs to the `leaf` parent's
        # children and for a `leaf` atmost one sibling must exists
        # we will prioritize the left_sibling to sacrifice first and then move on to next
        # first operation to get left_sibling and right_sibling
        left_s, right_s, sep_idx = node._get_siblings()
        print(f'\n left_s: {left_s}   right_s: {right_s}   idx: {sep_idx}\n')
        parent = node.get_parent()
        if (left_s is not None) and len(left_s.keys) > self.get_min_keys:
            # borrow from left_sibling
            node._borrow_from(sep_idx, left_s=left_s)
            return

        if (right_s is not None) and len(right_s.keys) > self.get_min_keys:
            # borrow from right_sibling
            node._borrow_from(sep_idx, right_s=right_s)
            return

        if len(parent.keys) < self.get_min_keys:
            self._handle_underflow(node=parent)

    def delete(self, key: Any):
        """
        Deletion from a B+-tree again needs to be sure to maintain the property that all nodes must be at least half full.
        """
        #     The steps to delete from a B+-tree are:
        # 1). Perform the search process on the key of the record to be deleted. This search will end at a leaf L.
        #
        # 2). If the leaf L contains more than the minimum number of elements (more than m/2 - 1),
        #     then the index entry for the record to be removed can be safely deleted
        #     from the leaf with no further action.
        #
        # 3).If the leaf contains the minimum number of entries,
        #    then the deleted entry is replaced with another entry that can take its place while maintaining the correct order.
        #
        #    To find such entries, we inspect the two sibling leaf nodes `L_left` and `L_right` adjacent to L -- at most one of these may not exist.
        #     a). If one of these leaf nodes has more than the minimum number of entries,
        #         then enough records are transferred from this sibling so that both nodes have the same number of records.
        #         This is a heuristic and is done to delay a future underflow as long as possible;
        #         otherwise, only one entry need be transferred.
        #             The placeholder key value of the parent node may need to be revised.
        #
        #     b). If both `L_left` and `L_right` have only the minimum number of entries,
        #         then L gives its records to one of its siblings and it is removed from the tree.
        #         The new leaf will contain no more than the maximum number of entries allowed.
        #         This merge process combines two subtrees of the parent, so the separating entry at the parent needs to be removed
        #           -- this may in turn cause the parent node to underflow; such an underflow is handled the same way that an underflow of a leaf node.
        #
        #     c). If the last two children of the root merge together into one node,
        #         then this merged node becomes the new root and the tree loses a level.

        key_exists, leaf = self._search(key)
        if key_exists:
            # delete the index key first then start to balance the tree from leaf-to-root upward
            leaf._delete(key)
            leaf_size = leaf.get_size()
            if leaf_size < self.get_min_keys:
                print("Called underflow")
                self._handle_underflow(leaf)
        else:
            raise KeyError(f"Index key `{key}` not found in tree")
