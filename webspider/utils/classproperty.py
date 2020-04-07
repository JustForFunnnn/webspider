# coding: utf-8


class ClassPropertyDescriptor(object):
    """类属性"""
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, obj_type=None):
        if obj_type is None:
            obj_type = type(obj)
        return self.fget.__get__(obj, obj_type)()

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)
