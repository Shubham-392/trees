from bplus import BPlusTreeMap

bptmap = BPlusTreeMap(4)
# bptmap.insert(12,"dg")
# bptmap.insert(13,"dg")
# bptmap.insert(14,"dg")
# bptmap.insert(15,"dg")
# bptmap.insert(16,"dg")
# bptmap.insert(17,"dg")
# bptmap.insert(18,"dg")
# bptmap.insert(19,"dg")
# bptmap.insert(20,"dg")
# bptmap.insert(21,"dg")

# bptmap.insert(22,"dg")
# bptmap.insert(23,"dg")
# bptmap.insert(24,"dg")
# bptmap.insert(25,"dg")
# bptmap.insert(26,"dg")
# bptmap.insert(27,"dg")
# bptmap.insert(28,"dg")

# bptmap.insert(29,"dg")
# bptmap.insert(30,"dg")

# bptmap.delete(30)
# bptmap.delete(27)
# bptmap.delete(key=29)
# bptmap.delete(28)
# bptmap.delete(26)
# bptmap.delete(25)
# bptmap.delete(24)
# bptmap.delete(23)
# bptmap.delete(22)
# bptmap.delete(21)
# bptmap.delete(20)
# bptmap.delete(19)
# bptmap.delete(18)
# bptmap.delete(17)

keys = [7, 10, 1, 23, 5, 15, 17, 9, 11, 39,35,8,40,25]
for key in keys:
    bptmap.insert(key, value=f'{key}')
print(bptmap.root)
