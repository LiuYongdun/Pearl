#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql元素基类


from abc import ABCMeta


class SQLElement(metaclass=ABCMeta):

    def __init__(self, name, alias=None):
        """
        :param name: sql元素名称
        :param alias: sql元素别名
        """
        self.__name = name
        self.__alias = alias
        self.__position: Position = None

    def __eq__(self, other):
        if isinstance(other, type(self)) \
                and other.name == self.name \
                and other.alias == self.alias:
            return True
        return False

    def __str__(self):
        return str({"name": self.name, "alias": self.alias})

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, alias):
        self.__alias = alias

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position


class Position:

    def __init__(self, row_num: int, col_num: int):
        """sql元素位置
        :param row_num: 行序号
        :param col_num: 列序号
        """
        self.row_num = row_num
        self.col_num = col_num

    def __str__(self):
        return str({"row_num": self.row_num, "col_num": self.col_num})
