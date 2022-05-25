#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql字面量


from element.SQLElement import SQLElement


class SQLLiteral(SQLElement):

    def __init__(self, name, alias):
        super().__init__(name, alias)
