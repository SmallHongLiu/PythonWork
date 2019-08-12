'''字符串'''
a = 'some_string'
print(id(a))
print(id('some' + '_' + 'string')) # 注意两个的id值是相同的

'''字符串驻留'''
a = 'wtf'
b = 'wtf'
a is b  # true，发生了字符串的驻留

a = 'wtf!'
b = 'wtf!'
a is b  # false, 因为包含！，则不能发生字符串的驻留

a, b = 'wtf!', 'wtf!'
a is b  # true, 同一行赋值时，第二个会创建一个新对象，然后同时引用第二个变量

'a' * 20 is 'aaaaaaaaaaaaaaaaaaaa'  # true, 常量折叠
'a' * 21 is 'aaaaaaaaaaaaaaaaaaaaa'  # false, 只有长度小于20的字符串才会发生常量折叠

''''''
some_dict = {}
some_dict[5.5] = 'Ruby'
some_dict[5.0] = 'JavaScript'
some_dict[5] = 'Python'  # 这个将覆盖上面的
# python字典通过检查键值是否相等和比较哈希值来确定两个键是否相等

5 == 5.0  # true
hash(5) == hash(5.0) # true 具有相同值的不可变对象在python中始终具有相同的哈希值
# 注意，具有不同值的对象也可能具有相同的哈希值（哈希冲突）

# try...finally 语句，当在try中执行return，break，或continue后，finally子句依然会被执行

some_string = 'wtf'
some_dict = {}
for i, some_dict[i] in enumerate(some_string):
    pass
print(some_dict)  # {0: 'w', 1: 't', 2: 'f'}

# is 和 == 的区别
# is 运算符检查两个运算对象是否引用自同一对象（即， 检查两个预算对象是否相同）
# == 运算符比较两个运算对象的值是否相等
# 因此 is 代表引用相同，== 代表值相等

[] == [] # true
[] is [] # false 这两个空列表位于不同的内存地址

a = 256
b = 256
a is b # true

a = 257
b = 257
a is b # false
# 256 是一个已经存在的对象，而257不是，当python启动时，－5 到 256的数值已经被分配好了

'something' is not None # true
'something' is (not None) # false






