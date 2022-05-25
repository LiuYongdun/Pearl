#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql关键字枚举类


from enum import Enum, unique
from itertools import chain


@unique
class SQLCommonKeyWord(Enum):
    SELECT = ("SELECT", {"is_clause": 1})
    FROM = ("FROM", {"is_clause": 1})
    WHERE = ("WHERE", {"is_clause": 1})
    GROUP = ("GROUP", {"is_clause": 1})
    HAVING = ("HAVING", {"is_clause": 1})
    ORDER = ("ORDER", {"is_clause": 1})
    LIMIT = ("LIMIT", {"is_clause": 1})
    SPACE = (" ", {"is_special_char": 1})
    ALL = ("*", {"is_special_char": 1})
    COMMA = (",", {"is_special_char": 1})
    LEFT_PARENTHESIS = ("(", {"is_special_char": 1, "is_operator": 1})
    RIGHT_PARENTHESIS = (")", {"is_special_char": 1})
    EQUAL = ("=", {"is_special_char": 1, "is_operator": 1})
    GREATER_THAN = (">", {"is_special_char": 1, "is_operator": 1})
    LESS_THAN = ("<", {"is_special_char": 1, "is_operator": 1})
    AS = ("AS", {"is_operator": 1})
    AND = ("AND", {"is_operator": 1})
    OR = ("OR", {"is_operator": 1})
    BY = ("BY", {})
    MAX = ("MAX", {})
    MIN = ("MIN", {})
    SIN = ("SIN", {})
    COS = ("COS", {})
    TAN = ("TAN", {})
    ARCSIN = ("ARCSIN", {})
    ARCCOS = ("ARCCOS", {})
    ARCTAN = ("ARCTAN", {})
    ABS = ("ABS", {})
    LN = ("LN", {})
    LG = ("LG", {})
    VARCHAR = ("VARCHAR", {"is_datatype": 1})
    DESC = ("DESC", {})
    ASC = ("ASC", {})
    ADD = ("+", {"is_special_char": 1, "is_operator": 1})
    SUB = ("-", {"is_special_char": 1, "is_operator": 1})
    DIV = ("/", {"is_special_char": 1, "is_operator": 1})
    POW = ("^", {"is_special_char": 1, "is_operator": 1})

    def __str__(self):
        return self.name


@unique
class FlinkKeyWord(Enum):
    HOP = ("HOP", {})
    HOP_START = ("HOP_START", {})
    HOP_END = ("HOP_END", {})
    TUMBLE = ("TUMBLE", {})
    TUMBLE_START = ("TUMBLE_START", {})
    TUMBLE_END = ("TUMBLE_END", {})
    INTERVAL = ("INTERVAL", {"is_operator": 1})
    SECOND = ("SECOND", {})
    SECONDS = ("SECONDS", {})
    HOUR = ("HOUR", {})
    HOURS = ("HOURS", {})
    ROW = ("ROW", {"is_datatype": 1})


FlinkKeyWord = Enum(FlinkKeyWord.__name__, [(_.name, _.value) for _ in chain(SQLCommonKeyWord, FlinkKeyWord)])
