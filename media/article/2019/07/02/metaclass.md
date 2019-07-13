title: python metaclass
tags:
  - python
  - 基础
categories:
  - back-end
comments: true
type: categories
author: ANT锟
date: 2019-06-10 18:18:00
---
### python中元类metaclass分析

metaclass是python中的重要概念，我来说一下理解吧，如有不对的地方，还请大家指正。

我认为metaclass是一切类的元类，可以理解为python中其实只有这一个类，就是type，其他的类都是type的实例对象，也就是平时我们定义的class，而我们实例化class，其实是调用type的实例的某个方法。
<!-- more -->
#### 认识type
type有两种用法
* type(object) -> object的类型
* type(name,base,dict) -> 生产class  

我们这里讲第二种方法

| 参数 | 描述 | 
| :------| ------: |
| name | class的名字，调用class().\__class\__会返回 | 
| base|一个元祖，继承的基类|
| dict | class.\__dict\__ |

#### 自定义type
```python
def __init__(self):
    self.a = 1
    
MyClass = type('MyClass', (), {'__init__': __init__, 'b': 1})
print(MyClass.__dict__)  # {'__init__': <function __init__ at 0x000002AB8C992E18>, 'b': 1, ...}
print(MyClass().__dict__)  # {'a': 1}
```
这里我们用type生成了一个MyClass类，从而避免了使用class语法定义  
那么type的具体实现是怎么样的呢？
```python
def __init__(self):
    self.a = 1


class MyType(type):
    def __init__(self, *args, **kwargs):
        print('__init__方法执行了', args, kwargs)
        super(MyType, self).__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        print('__new__方法执行了', args, kwargs)
        return type.__new__(cls, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('__call__方法执行了', args, kwargs)
        return super(MyType, self).__call__(*args, **kwargs)


MyClass = MyType('MyClass', (), {'__init__': __init__, 'b': 1})
print(MyClass.__dict__)
print(MyClass().__dict__)
```
输出结果如下

```python
__new__方法执行了 ('MyClass', (), {'__init__': <function __init__ at 0x000001FAC63D2E18>, 'b': 1}) {}
__init__方法执行了 ('MyClass', (), {'__init__': <function __init__ at 0x000001FAC63D2E18>, 'b': 1}) {}
{'__init__': <function __init__ at 0x000001FAC63D2E18>, 'b': 1, '__module__': '__main__', '__dict__': <attribute '__dict__' of 'MyClass' objects>, '__weakref__': <attribute '__weakref__' of 'MyClass' objects>, '__doc__': None}
__call__方法执行了 () {}
{'a': 1}
```
我们其实可以发现  
* 先执行\__new__方法，返回一个MyClass类对象
* 立马执行\__init__方法，进行MyClass类的初始化,定义一些属性
* 当MyClass类进行实例化的时候，调用\__call__方法

在平时实例化类的时候，我们知道，会调用\__new\__和\__init\__方法，而这里，实例化的时候调用了\__call\__方法，我们是不是可以猜测\__call\__里面调用了这两个方法呢，答案确实是这样，如果你在添加上
```python
def __new__(cls, *args, **kwargs):
    print('__new__方法2执行了', cls, args, kwargs)
    return object.__new__(cls, *args, **kwargs)
```
然后将代码改成
```python
def __init__(self):
    print('__init__方法2执行了')
    self.a = 1
MyClass = MyType('MyClass', (), {'__init__': __init__, 'b': 1, '__new__': __new__})
```
你就会发现在call后会输出new和init

#### 结论
python中()的执行，是靠魔法方法\__call\__的，也就是你在一个变量x后面加上(),即x()其实是调用的\__call\__方法，而实例化类的时候，其实就是调用了这个方法，最后返回一个对象，我们称作为实例。
class == type(name,base,dict)
self == class() == class.\__call\__\(\)
因此python中可以认为只有一个类，那就是元类，其他的类都是元类的实例，而类的实例，只是类调用了魔法方法，而产生了不同的对象，即实例对象。