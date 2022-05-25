#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql子查询


from typing import List
from element.SQLElement import SQLElement


class SQLQuery(SQLElement):
    def __init__(self, name, alias,
                 selectList: List[SQLElement] = None,
                 from_: SQLElement = None,
                 where: SQLElement = None,
                 group_by: List[SQLElement] = None,
                 having: SQLElement = None,
                 order_by: List[SQLElement] = None,
                 limit: SQLElement = None):
        """
        :param name:
        :param alias:
        :param selectList: select子句
        :param from_: from子句
        :param where: where子句
        :param group_by: group by子句
        :param having: having子句
        :param order_by: order by子句
        :param limit: limit子句
        """
        super().__init__(name, alias)
        self.__selectList = selectList
        self.__from = from_
        self.__where = where
        self.__group_by = group_by
        self.__having = having
        self.__order_by = order_by
        self.__limit = limit

    @property
    def selectList(self):
        return self.__selectList

    @selectList.setter
    def selectList(self, selectList):
        self.__selectList = selectList

    @property
    def from_(self):
        return self.__from

    @from_.setter
    def from_(self, from_):
        self.__from = from_

    @property
    def where(self):
        return self.__where

    @where.setter
    def where(self, where):
        self.__where = where

    @property
    def group_by(self):
        return self.__group_by

    @group_by.setter
    def group_by(self, group_by):
        self.__group_by = group_by

    @property
    def having(self):
        return self.__having

    @having.setter
    def having(self, having):
        self.__having = having

    @property
    def order_by(self):
        return self.__order_by

    @order_by.setter
    def order_by(self, order_by):
        self.__order_by = order_by

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        self.__limit = limit

    def clear(self):
        self.__selectList = None
        self.__from = None
        self.__where = None
        self.__group_by = None
        self.__having = None
        self.__order_by = None
        self.__limit = None
