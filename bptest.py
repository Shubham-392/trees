from bplus import BPlusTreeMap

bptmap = BPlusTreeMap(4)
bptmap.insert(12,"dg")
bptmap.insert(13,"dg")
bptmap.insert(14,"dg")
bptmap.insert(15,"dg")
bptmap.insert(16,"dg")
bptmap.insert(17,"dg")
bptmap.insert(18,"dg")
bptmap.insert(19,"dg")
bptmap.insert(20,"dg")
bptmap.insert(21,"dg")

bptmap.insert(22,"dg")
bptmap.insert(23,"dg")
bptmap.insert(24,"dg")
bptmap.insert(25,"dg")
bptmap.insert(26,"dg")
bptmap.insert(27,"dg")
bptmap.insert(28,"dg")

bptmap.insert(29,"dg")
bptmap.insert(30,"dg")
bptmap.insert(27.5,"dg")

bptmap.delete(30)
bptmap.delete(27.5)

print(bptmap.root)
