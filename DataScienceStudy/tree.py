from typing import Generic, TypeVar, List
T = TypeVar('T')
'''
从 typing 模块导入了 Generic、TypeVar 和 List
Generic 是一个泛型基类，用来定义泛型类型
TypeVar 用于定义类型变量
List 是一个泛型类型，表示列表
接着定义一个类型变量 T 用于表示节点存储的值的类型
'''
class Node(Generic[T]):
    _value: int
    _parent: 'Node[T]'
    _children: List['Node[T]']
    _subtree_size: int