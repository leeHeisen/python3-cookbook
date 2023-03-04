from attrs import define, field
import time
import attrs

## 2.2 高级语法
### 2.2.1 迭代器 iterator
l = [1, 2, 3]
s = "abc"
iter_o = iter(l)
# print(next(iter_o))

@define
class CountDown:
    step: int
    def __next__(self):
        if self.step <= 0:
            raise StopIteration
        self.step -= 1
        return self.step
    def __iter__(self):
        return self


# for i in CountDown(step=10):
#     print(i)
    


### 2.2.2 yield语句
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
    
# fib = fibonacci()
# print(fib)
# for i in range(10):
#     print(next(fib))

@define
class Fibonacci:
    step: int = field(default=10)
    a: int = field(default=0)
    b: int = field(default=1)
    current_step: int = field(default=0)
    
    def __next__(self):
        # print(type(self.a))
        if self.current_step >= self.step:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        self.current_step += 1
        return self.a
    
    def __iter__(self):
        return self



# for i in range(10):
#     print(fib.__next__())
# for i in range(10):
#     print(next(fib))
    
# a = [1, 2, 3]
# print(dir(iter(a)))
# print(dir(list))

idx = 0# print(a)
# for i in a:
#     print(i)
    # time.sleep(1)
    # idx += 1
    # if idx > 10:
    #     break



## 2.2.3 装饰器 Decorator
def repeat_func(func):
    def wrapper(*args, **kwargs):
        rt = None
        for i in range(3):
            print('i am repeat_func')
            rt = func(*args, **kwargs)
        return rt
    return wrapper
    

def repeat(number):
    def decorator(func):
        def wrapper(*args, **kwargs):
            rt = None
            for i in range(number):
                print('i am repeat')
                rt = func(*args, **kwargs)
            return rt
        return wrapper
    return decorator

@repeat(1)
@repeat_func
def foo():
    print('foo')
# foo()
### 典型的装饰器
def mydeco(func):
    # 保留func的名称信息和文档
    # from functools import wraps
    # @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
### 输入参数的装饰器
def mydeco(*a, **kv):
    def inner_deco(func):
        def wrapper(*args, **kwargs):
            print(*a, **kv)
            return func(*args, **kwargs)
        return wrapper
    return inner_deco


rpc_info = {}
def xmlrpc(in_=(), out=(type(None),)):
    def xmlrpc_d(func):
        func_name = func.__name__
        rpc_info[func_name] = (in_, out)
        def _check_types(elements, types):
            if len(elements) != len(types):
                raise TypeError('argument count mismatch')
            typed = enumerate(zip(elements, types))
            for index, couple in typed:
                arg, right_type = couple
                if isinstance(arg, right_type):
                    continue
                else:
                    raise TypeError('argument {} must be {}'.
                                    format(index, right_type))

        def xmlrpc_w(*args):
            checkable_args = args[1:]
            _check_types(checkable_args, in_)

            rlt = func(*args)
            if not type(rlt) in (tuple, list):
                checkable_rlt = (rlt,)
            else:
                checkable_rlt = rlt
            _check_types(checkable_rlt, out)
            return rlt
        return xmlrpc_w
    return xmlrpc_d


class RPCView:
    @xmlrpc((int, int))
    def meth1(self, int1, int2):
        print("received %d and %d" % (int1, int2))
    @xmlrpc((str, ), (int,))
    def meth2(self, phrase):
        print("received %s" % phrase)
        return len(phrase)
        
# rpc =RPCView()
# print(rpc.meth1(1, 2))
# print(rpc.meth2("hello"))
# print(rpc_info)
            
### 缓存

import time
import hashlib
import pickle

cache = {}

def is_obsolete(entry, duration):
    b = time.time() - entry['time'] > duration
    return b

def compute_key(func, args, kw):
    key = pickle.dumps((func.__name__, args, kw))
    return hashlib.sha1(key).hexdigest()

def memoize(duration=10):
    def real_memoize(func):
        def wrapper(*args, **kw):
            key = compute_key(func, args, kw)
            if key in cache and not is_obsolete(cache[key], duration):
                print('we got a winner')
                return cache[key]['value']
            else:
                rlt = func(*args, **kw)
                cache[key] = {'value': rlt, 'time': time.time()}
                return rlt
            return wrapper
        return real_memoize
        
## 2.3 其他语法元素
### for else: else executes if for loop terminates normally
### 函数注解

def square(number: int = 10) -> print(type('10')): return number ** 2

print(square())



