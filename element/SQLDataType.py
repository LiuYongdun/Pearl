#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql数据类型


from element.SQLElement import SQLElement


class SQLDataType(SQLElement):

    def __init__(self, name, alias):
        super().__init__(name, alias)
