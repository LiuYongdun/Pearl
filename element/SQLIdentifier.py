#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql标识符


from element.SQLElement import SQLElement


class SQLIdentifier(SQLElement):

    def __init__(self, name, alias):
        """SQL标识符(字段名,表名等)类
        """
        super().__init__(name, alias)
