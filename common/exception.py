#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : 自定义异常类


class DataStructureException(Exception):
    def __init__(self, error_info):
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class AstException(Exception):

    def __init__(self, error_info: str):
        super().__init__()
        self.error_info = error_info

    def __str__(self):
        return f"""{super().__str__()} \n {self.error_info}"""


class SQLException(AstException):

    def __init__(self, position, error_info: str):
        super().__init__(error_info)
        self.position = position

    def __str__(self):
        return f"sql error in {str(self.position)} : \n {super().__str__()}"
