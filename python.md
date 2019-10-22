# python

## 创建python虚拟环境

```shell
[root@room8pc16 python01]# python3 -m venv ~/nsd1902
[root@room8pc16 python01]# ls ~/nsd1902
# 激活虚拟环境
[root@room8pc16 python01]# source ~/nsd1902/bin/activate
(nsd1902) [root@room8pc16 python01]# python --version
Python 3.6.7
```

## python语法基础

### 输入输出语句

```python
>>> print('hao', 123, 'abc', sep='***')   # 通过sep指定分隔符
hao***123***abc
>>> print('Hello' + 'World')   # 字符串可以用＋拼接
HelloWorld
```

```python
>>> num = input('number: ')   # 将输入保存到变量num中
number: 100
>>> print(num)   
100
>>> num + 5    # 字符串和数字无法直接运算
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: must be str, not int
>>> int(num)    # 将字符串转成数字
100
>>> int(num) + 5   # 数字的四则运算
105
>>> str(5)     # 将数字转换成字符串
'5'
>>> num + str(5)    # 字符串拼接
'1005'
```

### 变量

- 首字符必须是字母或下划线

- 其他字符可以是字母、数字或下划线

- 区分大小写

  ```python
  >>> a += 1    # a = a + 1的简化写法
  >>> ++a    # 此处不自增，只是正号而已
  >>> x = y = 10
  >>> a, b = 10, 20
  >>> x, y = (100, 200)
  >>> m, n = [1, 2]
  >>> a, b = b, a   # a和b的值互换
  ```

### 运算符

- 算术运算符

```python
>>> a, b = divmod(5, 3)   # 把商和余数分别赋值给a和b
>>> a
1
>>> b
2
>>> 2 ** 3    # 乘方，幂运算
8
```

- 比较运算符：结果是True或False

```python
>>> 10 < 20 < 30    # python支持连续比较
True
>>> 10 < 20 > 15    # 容易引起岐义，不推荐
True
>>> 10 < 20 and 20 > 15   # 等同于 10 < 20 > 15
True
```

- 逻辑运算符

```python
# and 两边的结果都为True，最终结果才为True
>>> 5 > 3 and 10 < 20
True
# or 两边的结果有一边为True，最终结果才为True
>>> 5 > 3 or 3 > 10
True
# not 取反
>>> not 5 > 3
False
```

### 数字分类

- 整数：没有小数点
- 浮点数：有小数点
- 布尔数：True的值是1，False的值0

### 整数的表示方式

- python默认以10进制表示数字
- 8进制以0o开头
- 16进制以0x开头
- 2进制以0b开头

```python
>>> import os    #shell中输入默认为8进制python默认以10进制表示
>>> os.chmod('/tmp/hosts', 600)
[root@room8pc16 nsd2019]# ll /tmp/hosts 
---x-wx--T. 1 root root 9806 7月   1 15:45 /tmp/hosts
>>> os.chmod('/tmp/hosts', 0o600)
[root@room8pc16 nsd2019]# ll /tmp/hosts 
-rw-------. 1 root root 9806 7月   1 15:45 /tmp/hosts
>>> os.chmod('/tmp/hosts', 493)
[root@room8pc16 nsd2019]# ll /tmp/hosts 
-rwxr-xr-x. 1 root root 9806 7月   1 15:45 /tmp/hosts
```

### 字符串

字符串指的是在引号中间的字符，单双引号没有区别。

```python
>>> "%s is %s years old." % (name, age)
'tom is 20 years old.'
>>> words = "hello\nwelcome\ngreet"
>>> print(words)
hello
welcome
greet

# 三引号可以保留用户的输入格式
>>> wds = '''hello
... welcome
... greet'''
>>> print(wds)
hello
welcome
greet
>>> wds
'hello\nwelcome\ngreet'

>>> py_str = 'python'
>>> py_str[0]
'p
>>> py_str[-1]
'n'
>>> py_str[2:3]    # 切片操作，起始下标包含，结束下标不包含
't'
>>> py_str[2:6]   # 没有下标6，但切片不会报错
'thon'
>>> py_str[2:]   # 结束下标不写，表示到结尾
'thon'
>>> py_str[:2]   # 开头不写，表示从开头取
'py'
>>> py_str[::2]   # 步长值为2
'pto'
>>> py_str[1::2]
'yhn'
>>> py_str[::-1]   # 负数表示自右向左取
'nohtyp

>>> 'python' + ' good'
'python good'
>>> py_str + ' good'
'python good'
>>> py_str * 3
>>> '*' * 50
'**************************************************'
```

### 字符串格式化

```python
>>> '%s is %s years old' % ('tom', 20)
'tom is 20 years old'
>>> '%s is %d years old' % ('tom', 20)
'tom is 20 years old'
>>> '%10s%8s' % ('name', 'age')   # 第一列宽度为10，第二列8
'      name     age'
>>> '%-10s%-8s' % ('tom', 20)
'tom       20      '

>>> '%d' % (5 / 3)
'1'
>>> '%f' % (5 / 3)   # 浮点数
'1.666667'
>>> '%.2f' % (5 / 3)   # 保留两位小数
'1.67'
>>> '%6.2f' % (5 / 3)   # 总宽度为6，小数位2位
'  1.67'
>>> '%#o' % 10   # 8进制
'0o12'
>>> '%#x' % 10    # 16进制
'0xa'
>>> '%e' % 128000   # 科学计数法
'1.280000e+05'
```

**通过字符串的format方法实现格式化**

```python
>>> '{} is {} years old'.format('tom', 20)
'tom is 20 years old'
>>> '{1} is {0} years old'.format(20, 'tom')
'tom is 20 years old'
>>> '{0[1]} is {0[0]} years old'.format([20, 'tom'])
'tom is 20 years old'
>>> '{:<10}{:<8}'.format('tom', 20)  # 左对齐，宽度为10、8
'tom       20      '
>>> '{:>10}{:>8}'.format('tom', 20)   # 右对齐
'       tom      20'
```

**原始字符串**

```python
>>> win_path = 'c:\temp'
>>> print(win_path)   # \t将被认为是tab
c:	emp
>>> win_path = 'c:\\temp'   # \\真正表示一个\
>>> print(win_path)
c:\temp
>>> wpath = r'c:\temp\new'  # 原始字符串，字符串中的字符都表示字面本身含义
>>> print(wpath)
c:\temp\new
>>> wpath
'c:\\temp\\new'
```

### 字符串方法

```python
# 去除字符串两端空白字符
>>> ' \thello world!\n'.strip()
'hello world!'
# 去除字符串左边空白字符
>>> ' \thello world!\n'.lstrip()
'hello world!\n'
# 去除字符串右边空白字符
>>> ' \thello world!\n'.rstrip()
' \thello world!'

>>> hi = 'hello world'
>>> hi.upper()   # 将字符串中的小写字母转成大写
'HELLO WORLD'
>>> 'HELLO WORLD'.lower()   # 将字符串中的大写字母转成小写
'hello world'
>>> hi.center(30)   # 居中
'         hello world          '
>>> hi.center(30, '*')
'*********hello world**********'
>>> hi.ljust(30)
'hello world                   '
>>> hi.ljust(30, '#')
'hello world###################'
>>> hi.rjust(30, '@')
'@@@@@@@@@@@@@@@@@@@hello world'
>>> hi.startswith('h')   # 字符串以h开头吗？
True
>>> hi.startswith('he')
True
>>> hi.endswith('o')   # 字符串以o结尾吗？
False
>>> hi.replace('l', 'm')   # 把所有的l替换成m
'hemmo wormd'
>>> hi.replace('ll', 'm')
'hemo world'
>>> hi.split()   # 默认以空格进行切割
['hello', 'world']
>>> 'hello.tar.gz'.split('.')    # 以点作为分隔符切割
['hello', 'tar', 'gz']
>>> str_list = ['hello', 'tar', 'gz']
>>> '.'.join(str_list)   # 以点为分隔符进行字符串拼接
'hello.tar.gz'
>>> '-'.join(str_list)
'hello-tar-gz'
>>> ''.join(str_list)
'hellotargz'
>>> hi.islower()   # 判断字符串内的字母都是小写的吗？
True
>>> 'Hao123'.isupper()   # 字符串内的字母都是大写的吗？
False
>>> 'hao123'.isdigit()   # 所有的字符都是数字字符吗？
False
>>> '123'.isdigit()
True
```

### 列表操作

```python
>>> from random import randint
>>> alist = [randint(1, 100) for i in range(10)]
>>> alist
[95, 58, 74, 39, 42, 32, 41, 35, 40, 65]
>>> alist[0] = 100
>>> alist
[100, 58, 74, 39, 42, 32, 41, 35, 40, 65]
>>> alist[3:5] = [25, 46, 89]
>>> alist
[100, 58, 74, 25, 46, 89, 32, 41, 35, 40, 65]
>>> alist[2:2] = [10, 20]
>>> alist
[100, 58, 10, 20, 74, 25, 46, 89, 32, 41, 35, 40, 65]
```

### 列表方法

```python
>>> alist.append(100)   # 追加append
>>> alist
[100, 58, 10, 20, 74, 25, 46, 89, 32, 41, 35, 40, 65, 100, [10, 20]]
>>> alist.append([10, 20])
>>> alist.extend([10, 20])   # 把序列对象的每一项逐个放到列表中
>>> alist
[100, 58, 10, 20, 74, 25, 46, 89, 32, 41, 35, 40, 65, 100, [10, 20], 10, 20]
>>> alist.remove(10)   # 删除列表中的第一个10
>>> alist.pop()   # 默认弹出最后一项
20
>>> alist.pop(-2)   # 弹出列表下标为-2的项
[10, 20]
>>> alist
[100, 58, 20, 74, 25, 46, 89, 32, 41, 35, 40, 65, 100, 10]
>>> alist.index(46)   # 获取46的下标
5
>>> alist.reverse()   # 将列表原地翻转
>>> alist
[10, 100, 65, 40, 35, 41, 32, 89, 46, 25, 74, 20, 58, 100]
>>> alist.insert(4, 100)   # 在下标为4的位置插入100
>>> alist.count(100)   # 统计100出现的次数
>>> alist.sort()  # 默认升序排列
>>> alist.sort(reverse=True)   # 降序排列
>>> alist
[100, 100, 100, 89, 74, 65, 58, 46, 41, 40, 35, 32, 25, 20, 10]
>>> blist = alist.copy()  # 将alist的值拷贝一份后，赋值给blist
>>> blist
[100, 100, 100, 89, 74, 65, 58, 46, 41, 40, 35, 32, 25, 20, 10]
>>> blist.clear()   # 清空列表
>>> blist
[]
>>> alist
[100, 100, 100, 89, 74, 65, 58, 46, 41, 40, 35, 32, 25, 20, 10]
>>> len(alist)   #查看列表有多少项目
```

### 元组

元组相当于是静态的列表，不可改变。

```python
>>> atuple = (10, 20, 30, 20, 40, 20)
>>> atuple.<tab><tab>
atuple.count(  atuple.index(  
>>> atuple.count(20)
3
>>> atuple.index(20)
1
```

**单元素元组注意，一定要在结尾有个逗号**

```python
>>> a = (10)
>>> a
10
>>> type(a)   # 查看a的类型
<class 'int'>
>>> b = (10,)
>>> b
(10,)
>>> type(b)
<class 'tuple'>
>>> len(b)
1
```

### 字典

**属于容器、可变、映射**

```python
>>> adict = dict(['ab', ['name', 'bob'], ('age', 20)])
>>> adict
{'a': 'b', 'name': 'bob', 'age': 20}

# 创建值相同的字典
>>> bdict = {}.fromkeys(['jerry', 'tom', 'bob'], 20)
>>> bdict
{'jerry': 20, 'tom': 20, 'bob': 20}

# 字典中的key不能重复
>>> adict = {'name': 'tom', 'age': 20}
>>> adict['age']
20
# 赋值时，key已存在则修改它的值
>>> adict['age'] = 22
>>> adict
{'name': 'tom', 'age': 22}
# 赋值时，key不存在，则增加新项目
>>> adict['email'] = 'tom@tedu.cn'
>>> adict
{'name': 'tom', 'age': 22, 'email': 'tom@tedu.cn'}

# tom是字典的key吗？
>>> 'tom' in adict
False
>>> for key in adict:
...     print(key, adict[key])

>>> '%(name)s: %(age)s %(email)s' % adict
'tom: 22 tom@tedu.cn'
```

**字典的key只能是不可变对象**

```python
>>> adict[[1, 2]] = 10
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> bdict[(1, 2)] = 10
>>> bdict
{(1, 2): 10}
```

**字典的相关方法：**

```python
>>> adict.items()
dict_items([('name', 'tom'), ('age', 22), ('email', 'tom@tedu.cn')])
# 遍历字典
>>> for key, val in adict.items():
...     print(key, val)
... 
name tom
age 22
email tom@tedu.cn

>>> adict.keys()   # 只取出key
dict_keys(['name', 'age', 'email'])
>>> adict.values()  # 只取出value
dict_values(['tom', 22, 'tom@tedu.cn'])  # 更新字典
>>> adict.update({'qq': '13542632', 'phone': '15088997766'})
>>> adict
{'name': 'tom', 'age': 22, 'email': 'tom@tedu.cn', 'qq': '13542632', 'phone': '15088997766'}

>>> adict.popitem()   # 随机移出一项
('phone', '15088997766')
>>> adict.pop('qq')   # 通过key删除项
'13542632'

>>> adict['birth_date']   # 没有相应的key，则报错
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'birth_date'

# get是字典中用得最多的一个方法
>>> print(adict.get('birth_date'))  # key不在字典中默认返回None
None
>>> adict.get('age')
22
>>> adict.get('age', 30)   # 如果get到值则返回值，get不到则返回30
22
>>> adict.get('birth_date', 'not found')
'not found'
```

### 集合

**集合用set表示，由不同（不可变）元素构成**

**集合分为不可变集合和forzenset和可变集合set。**

```python
>>> fs = frozenset('abc')   # 创建不可变集合
>>> s1 = set('abc')         # 创建可变集合
>>> fs
frozenset({'a', 'c', 'b'})
>>> s1
{'a', 'c', 'b'}
>>> s10 = set(['aaa', 'bbb', 'ccc'])
>>> s10
{'ccc', 'bbb', 'aaa'}

>>> len(s10)
3
>>> for word in s10:
...     print(word)
>>> 'aaa' in s10
True
>>> 'fff' in s10
False
```

集合和字典都是无序的，字典的key和集合元素都是不可变的、不能重复的。**因此，集合就像是一个没有value的字典。**

### 集合相关方法

```python
>>> aset = set('abc')
>>> bset = set('bcd')
>>> aset
{'a', 'c', 'b'}
>>> bset
{'c', 'd', 'b'}
>>> aset & bset   # 交集
{'c', 'b'}
>>> aset | bset   # 并集
{'c', 'b', 'a', 'd'}
>>> aset - bset   # 差补，在aset中有，bset中没有
{'a'}
>>> bset - aset
{'d'}

>>> aset.add('new')   # 将new作为整体添加到集合
>>> aset
{'new', 'a', 'c', 'b'}
>>> aset.update('new')   # 将序列对象中的每个元素逐一添加到集合
>>> aset
{'new', 'c', 'a', 'n', 'w', 'b', 'e'}
>>> aset.update(['hello', 'world'])
>>> aset
{'new', 'c', 'a', 'w', 'n', 'hello', 'world', 'b', 'e'}
>>> aset.remove('new')   # 删除一项
>>> aset
{'c', 'a', 'w', 'n', 'hello', 'world', 'b', 'e'}

# 作为了解的方法
>>> s1 = set('abcde')
>>> s2 = set('bcd')
>>> s1
{'c', 'a', 'b', 'e', 'd'}
>>> s2
{'c', 'd', 'b'}
>>> s1.issuperset(s2)   # s1是s2的超集吗？
True
>>> s2.issubset(s1)     # s2是s1的子集吗？
True
>>> s1.union(s2)    # s1 | s2
{'c', 'b', 'a', 'e', 'd'}
>>> s1.intersection(s2)    # s1 & s2
{'c', 'd', 'b'}
>>> s1.difference(s2)    # s1 - s2
{'a', 'e'}
```

**集合的应用**

```python
# 去重操作
>>> num_list = [randint(1, 20) for i in range(10)]
>>> num_list
[1, 7, 19, 13, 18, 16, 19, 15, 9, 19]
>>> set(num_list)
{1, 7, 9, 13, 15, 16, 18, 19}
>>> list(set(num_list))
[1, 7, 9, 13, 15, 16, 18, 19]
```



### 数据类型比较

**按存储模型分为：**

- 标量：数字、字符串
- 容器：列表、字典、元组

**按更新模型分为：**

- 不可变：数字、字符串、元组
- 可变：列表、字典

**按访问模型分为：**

- 直接：数字
- 顺序：字符串、列表、元组
- 映射：字典

## 文件对象

**最常用的、读取文本文件的方式是for循环遍历：**

```python
>>> f = open('/tmp/mima')
>>> for line in f:
...     print(line, end='')
>>> f.close()
```

```python
src_fname = '/bin/ls'
dst_fname = '/tmp/list2'

with open(src_fname, 'rb') as src_fobj:
    with open(dst_fname, 'wb') as dst_fobj:
        while True:
            data = src_fobj.read(4096)   # 每次最多读4096字节
            if not data:    # data值为b''，表示False
                break
            dst_fobj.write(data)
```

**写入文件：**

```python
[root@room8pc16 day02]# cp /usr/bin/ls /tmp/
>>> f = open('/tmp/ls')
>>> f.read(10)   # 报错。因为打开时默认以utf8编码打开，但是ls不是文本文件。读取时，Python试图把读出来的10个字节显示为utf8字符。
>>> f.close()

>>> f = open('/tmp/ls', 'rb')   # 以bytes类型打开
>>> f.read(10)
b'\x7fELF\x02\x01\x01\x00\x00\x00'
>>> f.close()

# 文本文件也能以bytes方式打开
>>> f = open('/tmp/mima', 'rb')
>>> f.read()
b'hello world!\n2nd line.\n3rd line.\nend\n'
>>> f.close()
```

**移动文件指针：seek(x, y)。y可以取值0，1，2，分别表示文件开头、当前位置和结尾。x是偏移量。**

```python
>>> f = open('/tmp/mima')
>>> f.tell()   # 显示当前位置，永远从开头算偏移量
0
>>> f.seek(5, 0)
5
>>> f.read(1)
' '
>>> f.close()

>>> f.read()   # 读取全部内容
>>> f.read()   # 再读就没有数据了
''
>>> f.seek(0, 0)   # 回到文件开头
0
>>> f.read()   # 再次读取文件内容
>>> f.close()  # 关闭文件


>>> f = open('/tmp/mima', 'rb')
>>> f.seek(-5, 2)   # 指针移动到文件结尾前5个字节处
32
>>> f.read()
b'\nend\n'
```

## 序列对象

**内建函数：**

```python
# list用于转换成列表
>>> list('hello')
['h', 'e', 'l', 'l', 'o']
>>> list(range(1, 10))
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> list((10, 20, 30))
[10, 20, 30]

# tuple用于转换成元组
>>> tuple('hello')
('h', 'e', 'l', 'l', 'o')
>>> tuple(range(1, 10))
(1, 2, 3, 4, 5, 6, 7, 8, 9)
>>> tuple(['bob', 'tom', 'jerry'])
('bob', 'tom', 'jerry')

# str用于转成字符串
>>> str(100)
'100'
>>> str([100, 200])
'[100, 200]'
```

**常用于序列对象的方法：**

```python
>>> from random import randint
>>> num_list = [randint(1, 100) for i in range(5)]
>>> num_list
[53, 95, 37, 50, 54]

# reversed用于翻转
>>> list(reversed(num_list))
[54, 50, 37, 95, 53]
>>> for i in reversed(num_list):
...     print(i)

# sort排序
>>> sorted(num_list)
[37, 50, 53, 54, 95]
>>> sorted(num_list, reverse=True)   # 降序
[95, 54, 53, 50, 37]

# enumerate返回下标和元素
>>> list(enumerate(num_list))
[(0, 53), (1, 95), (2, 37), (3, 50), (4, 54)]
>>> for data in enumerate(num_list):
...     print(data)
>>> for ind, num in enumerate(num_list):
...     print(ind, num)
```







## 模块：

### shutil模块

```python
>>> import shutil
# copyfileobj只是了解底层原理，实际代码不需要使用
>>> f1 = open('/bin/ls', 'rb')
>>> f2 = open('/tmp/list4', 'wb')
>>> shutil.copyfileobj(f1, f2)
>>> f1.close()
>>> f2.close()

# shutil.copyfile只拷贝内容
>>> shutil.copyfile('/bin/ls', '/tmp/list5')
# shutil.copy既拷贝内容，又拷贝权限 
>>> shutil.copy('/bin/ls', '/tmp/list6')
# shutil.copy2相当于系统命令cp -p
>>> shutil.copy2('/bin/ls', '/tmp/list7')
# shutil.move => 相当于系统命令mv
>>> shutil.move('/tmp/list7', '/var/tmp/list')
# copytree相当于cp -r
>>> shutil.copytree('/etc/security', '/tmp/security')
>>> shutil.move('/tmp/security', '/var/tmp/auquan')
# rmtree 相当于rm -rf
>>> shutil.rmtree('/var/tmp/auquan')

# 删除单个文件的函数在os模块
>>> import os
>>> os.remove('/tmp/list5')
# 改变属主属组
>>> shutil.chown('/tmp/list', user='bob', group='bob')
```





### subprocess模块： 用于调用系统命令

```python
>>> subprocess.run(['ls', '/home'])
bob  lisi  Student  wangwu  zhangsan
CompletedProcess(args=['ls', '/home'], returncode=0)

>>> subprocess.run('ls /home', shell=True)
bob  lisi  Student  wangwu  zhangsan
CompletedProcess(args='ls /home', returncode=0)

>>> subprocess.run(['ls', '~'])
ls: 无法访问~: 没有那个文件或目录
CompletedProcess(args=['ls', '~'], returncode=2)

>>> subprocess.run('ls ~', shell=True)

# subprocess.run的返回值
>>> rc = subprocess.run('ping -c2 192.168.4.254 &> /dev/null', shell=True)
>>> rc.returncode   # 就是系统命令的$?
0

# 捕获输出
>>> rc = subprocess.run('id root; id john', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
>>> rc.returncode
1
>>> rc.stdout
b'uid=0(root) gid=0(root) \xe7\xbb\x84=0(root)\n'
>>> rc.stderr
b'id: john: no such user\n'
# 将bytes类型转成str类型
>>> rc.stdout.decode()
'uid=0(root) gid=0(root) 组=0(root)\n'
```

