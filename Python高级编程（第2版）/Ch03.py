### MRO, Method Resolution Order

class A:
    def foo(self):
        print('A.foo')

class B():
    def foo(self):
        print('B.foo')

class C(A, B):
    pass

class D(C):
    pass

# obj = C()
# obj.foo()

### 3.3.1 描述符 descriptor
"""
1. 描述符是一个类，定义了另一个类的属性访问方法，也就是一个类把属性管理托管给了\
    另一个类。
2. 描述符允许你在访问属性时自动触发一些操作，比如类型检查或合法性验证。
3. 描述符是复杂属性访问的基础，在内部被用于实现property、方法、类方法、静态方法\
    和super()等高级功能。
4. 描述符基于__get__、__set__和__delete__这三个特殊方法。\
    实现了这三个方法中的任意一个的类都是描述符。
5. 数据描述符是实现了__set__方法的描述符，它会覆盖实例字典__dict__中同名的属性。
6. 每次通过点号访问属性，都会隐式地调用__getattribute__()方法，该方法按以下顺序\
    数据描述符、实例字典、非数据描述符的顺序查找属性。
7. 函数对象、lambda表达式创建的函数，都是非数据描述符。
"""
class RevealAccess:
    """A data descriptor that sets and returns values
    normally and prints a message logging their access.
    """
    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'var "x"')
    y = 5

# m = MyClass()
# print(m.x)
# m.x = 20
# print(dir(m.x), type(m.x))
# print(dir(RevealAccess), type(RevealAccess))
# print(m.x)
# print(m.y)

class Human:
    cls_val = 1
    def __init__(self) -> None:
        self.ins_val = 10
h = Human()
print(h.__dict__)
print(Human.__dict__)

# print(dir(h))
# print(dir(Human))




### property