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

    def getSize(self):
        return self.size

    def peek(self):
        if not self.isEmpty():
            return self.inner_list[-1]
        raise DataStructureException("Stack is empty")


class AstStack(Stack):

    def __init__(self):
        super().__init__()

    def pushN(self, pops: List):
        self.inner_list.extend(pops)
        self.size += len(pops)

    def popN(self, num):
        if num > self.getSize():
            raise AstException(f"given num [{num}] lager than the size of stack [{self.getSize()}]")
        pops = [self.pop() for _ in range(num)][::-1]
        return pops

    def peek(self, num=1):
        if num == 1:
            return [self.inner_list[-1]]
        return self.inner_list[-num:]

    # 从栈顶开始查值value首次出现的位置
    def index(self, value):
        for i in range(self.getSize()):
            if isinstance(self.inner_list[-i - 1], type(value)) and self.inner_list[-i - 1].name == value.name:
                return i
        return self.getSize()

    # 从栈顶开始查类型_type首次出现的位置
    def indexType(self, _type):
        for i in range(self.getSize()):
            if isinstance(self.inner_list[-i - 1], _type):
                return i
        return self.getSize()

    # element入栈, 每次都需要判断规则栈栈顶规则是否满足触发条件
    def pushElement(self, element, rule_stack):

        if element:
            self.inner_list.append(element)
            self.size += 1
        if not rule_stack.isEmpty():
            current_rule = rule_stack.peek()[0]()
            if current_rule.trigger(self):
                rule_stack.pop()
                current_rule.action(self, rule_stack)

        # print("规则栈:")
        # list(map(print, reversed(rule_stack.inner_list)))
        # print("sql元素栈:")
        # list(map(print, self.peek(self.getSize())))
        # print("-" * 50)

    def pushRule(self, rule, element_stack):
        if rule:
            self.inner_list.append(rule)
            self.size += 1
        if self.getSize():
            current_rule = self.peek()[0]()
            if current_rule.trigger(element_stack):
                self.pop()
                current_rule.action(element_stack, self)


