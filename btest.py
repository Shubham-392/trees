import random

from btree import BTreeMap, BTreeNode


def sample_insert(node: BTreeNode, order):
    keys = list(range(1, order + 1))
    values = [str(i) for i in keys]
    for key, value in zip(keys, values):
        print(f"Inserting {key}: {value}")
        node.set_keyvalue(key, value)


def test_btree_node():
    # node = BTreeNode(order=2)
    # node1 = BTreeNode(order=2)
    # node2 = BTreeNode(order=2, leaf=True)
    # node3 = BTreeNode(order=2, leaf=True)
    # node4 = BTreeNode(order=2, leaf=True)
    # node.set_keyvalue(10, "yessss")
    # node.set_keyvalue(key=8, value="ohhhhyeahhh!!")
    # node.set_children(node1, 0)
    # node.set_children(node2, 1)
    # node.set_children(node3, 2)
    # node.set_children(node4, 3)
    # get a random high number
    randnum = random.randint(4, 24)
    print(f"Testing BTreeMap with order={randnum}")
    
    btreemap = BTreeMap(order=randnum)
    for i in range(randnum + 4):
        btreemap.insert(i, str(i))
    

    print(btreemap.root)
    print(btreemap.root.children)
    
    del_node = btreemap.delete(randnum + 4)
    print(f"Search for {randnum + 4}")
    print(del_node)
    


# test_btree_node()



# test for deletion operation from the leaf
def test_btree_delete_leaf():
    btreemap = BTreeMap(order=4)
    for i in range(5):
        btreemap.insert(i, str(i))
    print(btreemap.root)
    print(btreemap.root.children)
    btreemap.delete(4)
    print(btreemap.root)
    print(btreemap.root.children)


# test_btree_delete_leaf()
# 
# test for the delete operation in internal node
# 
def test_btree_delete_internal():
    btreemap = BTreeMap(order=5)
    for i in range(30):
        btreemap.insert(i, str(i))
    print(btreemap.root)
    print(btreemap.root.children)
    btreemap.delete(23)
    # print(btreemap.root)
    # print(btreemap.root.children)
    # for child in btreemap.root.children:
    #     print(child)
    #     print(child.children)

    btreemap.delete(22)
    # print(btreemap.root)
    # print(btreemap.root.children)
    # for child in btreemap.root.children:
    #     print(child)
    #     print(child.children)
    btreemap.delete(24)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)
    btreemap.delete(15)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)
    btreemap.delete(29)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)
    btreemap.delete(20)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)
    btreemap.delete(14)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)
    btreemap.delete(16)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)
    btreemap.delete(17)
    print(btreemap.root)
    print(btreemap.root.children)
    for child in btreemap.root.children:
        print(child)
        print(child.children)

    print(btreemap.root)
    print(btreemap.root.children)


test_btree_delete_internal()


def btree_test_insert_ops():
    btreemap = BTreeMap(order=5)
    for i in range(30):
        btreemap.insert(i, str(i))
    # print the tree structure
    print(btreemap.root)
    print(btreemap.root.children)
    
        

# btree_test_insert_ops()