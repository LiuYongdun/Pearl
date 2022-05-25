#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : sql方言类

from enum import unique, Enum


@unique
class SQLDialect(Enum):
    FLINK_SQL = 0
    HIVE_SQL = 1
    SPARK_SQL = 2
    MYSQL = 3
