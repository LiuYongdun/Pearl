#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql子句关键字(select,from,where,group,order,having等)


from element.SQLElement import SQLElement


class SQLClause(SQLElement):

    def __init__(self, name, alias=None):
        super().__init__(name, alias)
