#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @Contact : Artle.Liu
# @Description : 语法树Stack类, 用于sql元素栈和merge规则栈
from collections import deque

from common.exception import AstException, DataStructureException
from typing import List


class Stack:

    def __init__(self):
        self.inner_list = deque()
        self.size = 0

    def push(self, item):
        self.inner_list.append(item)  # 添加元素
        self.size += 1  # 栈元素数量加 1

    def pop(self):
        if not self.isEmpty():
            pop = self.inner_list.pop()  # 删除栈顶元素
            self.size -= 1  # 栈元素数量减 1
            return pop
        raise DataStructureException("Stack is empty")

    def isEmpty(self):
        return self.size == 0

    def sizes(self):
        return self.size

    def peek(self):
        if not self.isEmpty():
            return self.inner_list[-1]
        raise DataStructureException("Stack is empty")

class AstStack:

    def __init__(self):
        self.inner_list = []
        self.size = 0

    def pushN(self, pops: List):
        self.inner_list.extend(pops)
        self.size += len(pops)

    # token入栈, 每次都需要判断规则栈栈顶规则是否满足触发条件
    def pushToken(self, token, merge_rule_stack):

        if token:
            self.inner_list.append(token)
            self.size += 1
        if not merge_rule_stack.isEmpty():
            current_rule = merge_rule_stack.peek()()
            if current_rule.trigger(self):
                merge_rule_stack.pop()
                current_rule.action(self, merge_rule_stack)

        # print("规则栈:")
        # list(map(print, reversed(merge_rule_stack.inner_list)))
        # print("sql元素栈:")
        # list(map(print, self.peek(self.getSize())))
        # print("-" * 50)

    def pop(self):
        pop = self.inner_list.pop()
        self.size -= 1
        return pop

    def popN(self, num):
        if num > self.getSize():
            raise AstException(f"given num: {num} lager than the size of stack:{self.getSize()}")
        pops = [self.pop() for _ in range(num)][::-1]
        return pops

    def isEmpty(self):
        return self.size == 0

    def getSize(self):
        return self.size

    def peek(self, num=1):
        if num == 1:
            return [self.inner_list[-1]]
        return self.inner_list[-num:]

    # # 从栈顶开始查值value首次出现的位置
    # def index(self, value):
    #     tmp_list = self.inner_list[::-1]
    #
    #     for i in range(len(tmp_list)):
    #         if isinstance(tmp_list[i], type(value)) and tmp_list[i].name == value.name:
    #             return i
    #     return -1

    # 从栈顶开始查值value首次出现的位置
    def index(self, value):
        for i in range(self.getSize()):
            if isinstance(self.inner_list[-i-1], type(value)) and self.inner_list[-i-1].name == value.name:
                return i
        return -1

    # 从栈顶开始查类型_type首次出现的位置
    def indexType(self, _type):
        for i in range(self.getSize()):
            if isinstance(self.inner_list[-i-1], _type):
                return i
        return -1
