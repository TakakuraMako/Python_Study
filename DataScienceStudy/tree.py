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

    def __init__(self, value: T) -> None:
        self._value = value
        self._parent = None
        self._children = []
        self._subtree_size = 1

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T) -> None:
        self._value = value

    def get_parent(self) -> 'Node[T]':
        return self._parent
    
    def get_subtree_size(self) -> int:
        return self._subtree_size

    def set_subtree_size(self, value: int) -> None:
        self._subtree_size = value

    def add_child(self, child: 'Node[T]') -> None:
        self._children.append(child)
        child._parent = self

    def get_children(self) -> List['Node[T]']:
        return self._children

    def num_children(self) -> int:
        return len(self._children)
    
    def is_internal(p: 'Node[T]') -> bool:
        return len(p._children) != 0 # 有子节点
    
    def is_external(p: 'Node[T]') -> bool:
        return len(p._children) == 0 # 无子节点
    
    def is_root(p: 'Node[T]') -> bool:
        return p._parent == None
        
class Tree(Generic[T]):
    _size: int
    _root: Node[T]
 
    def __init__(self, root: 'Node[T]') -> None:
        self._root = root
        self._size = 0
        if root != None:
            self._size = 1

    def get_root(self) -> 'Node[T]':
        return self._root
    
    def get_size(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._root == None  
 
    def is_root(self, p: 'Node[T]') -> bool:
        if p is None:
            return False
        return p.get_parent() == None
    
    def is_leaf(self, p: 'Node[T]') -> bool:
        if p is None:
            return False
        return p.is_external()
    
    def add_node(self, p: 'Node[T]', parent: 'Node[T]') -> None:
        if self._root is None and p != None and parent is None:
            self._root = p
            self._size += 1
            
        elif (p is None) or (parent is None):
            return
        
        else:
            parent.add_child(p)
            self._size += 1
 
        # Update subtree size for parent and all its ancestors.
        while p.get_parent() != None:
            p = p.get_parent()
            p_subtree = p.get_subtree_size()
            p.set_subtree_size(p_subtree + 1)
 
    def remove_node(self, p: 'Node[T]') -> None:
        if p is None:
            return
 
        if p.is_root():
            self._root = None
            self._size = 0
        else:
            current = p
            subtree_size = p.get_subtree_size()
            while p.get_parent() != None:
                p = p.get_parent()
                p.set_subtree_size(p.get_subtree_size() - subtree_size)
            parent = current.get_parent()
            parent.get_children().remove(current)
            self._size -= subtree_size

    def preorder(self, p: 'Node[T]', ls: List['Node[T]']) -> None:
        if p is None:
            return
 
        ls.append(p)
        for child in p._children:
            self.preorder(child, ls)
    
    def postorder(self, p: 'Node[T]', ls: List['Node[T]']) -> None:
        if p is None:
            return
        
        for child in p._children:
            self.postorder(child,ls)
        ls.append(p)