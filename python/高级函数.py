# ZIP压缩
# 把两个可迭代内容生成一个可迭代的tuple元素类型组成的内容
l1 = [1, 2, 3, 4, 5]
l2 = [11, 22, 33, 44]
z = zip(l1, l2)
print(type(z))
print(z)

for i in z:
    print(i)

    