import sys
import os
import re
import random

def exp_tree_to_mid_exp(exp_tree):
	"""
	将生成的表达式二叉树转化为中缀表达式
	用于判断随机生成的四则运算表达式是否重复
	parameters:
    exp_tree(dict)：表达式二叉树
	return:
    exp_mid(str)：规范的中缀表达式
	"""
	(key, child), = exp_tree.items()  #获取子树

	if type(child[0]) == type(1) or type(child[0]) == type(0.1):
		mid_exp = '(' + str(child[0])
	else:
 		mid_exp = '(' + str(exp_tree_to_mid_exp(child[0]))
	mid_exp += " " + key + " "
	if type(child[1]) == type(1) or type(child[1]) == type(0.1):
		mid_exp += str(child[1]) + ')'
	else:
		mid_exp += str(exp_tree_to_mid_exp(child[1])) + ')'
	return mid_exp

def mid_expression_to_post_expression(exp_mid):
    exp_post = []   # 后缀表达式
    stack = []      # 栈
    operators = {'(': 0, ')': 0, '+': 1, '-': 1, '*': 2} # 操作符

    while (len(exp_mid)):
        # 对中缀表达式中的操作符进行处理
        if exp_mid[0] in operators.keys():
            if exp_mid[0] == ')':   # 操作符为右括号
                while True:
                    if stack[len(stack) - 1] == '(':
                        break
                    else:           # 将栈中属于括号内的运算符加入到后缀表达式中
                        exp_post.append(stack.pop())
                stack.pop()         # 删除左括号
            elif len(stack) == 0 or exp_mid[0] == '(' or operators[stack[-1]] < operators[exp_mid[0]]:
                stack.append(exp_mid[0])    # 左括号、优先级高的操作符进栈，或者栈中没有操作符时进栈
            elif operators[stack[-1]] >= operators[exp_mid[0]]:
                while operators[stack[-1]] >= operators[exp_mid[0]]:
                    exp_post.append(stack.pop()) # 将优先级高的运算符出栈处理
                    if len(stack) == 0:
                        break
                stack.append(exp_mid[0])
        # 对中缀表达式中的操作数进行处理
        else:
            exp_post.append(exp_mid[0])        # 将操作数添加到后缀表达式中
        exp_mid = exp_mid[1:]
        if len(exp_mid) == 0:
            while len(stack):
                exp_post.append(stack.pop())
    return exp_post

def post_expression_to_bitree(post_expression):
	base_node = post_expression.pop()
	exp_tree = {base_node:[]}
	operators = ['+', '-', '*']

	if not post_expression:
		return {}
    # 左子树递归处理
	if post_expression[-1] in operators: # 右子树为操作符
		exp_tree[base_node].append(post_expression_to_bitree(post_expression))
	else:                               # 右子树为操作数
		exp_tree[base_node].append(post_expression.pop())
    # 右子树递归处理
	if post_expression[-1] in operators: # 左子树为操作符
		exp_tree[base_node].insert(0, post_expression_to_bitree(post_expression))
	else:                               # 左子树为操作数
		exp_tree[base_node].insert(0, post_expression.pop())
	return exp_tree


def to_reg_exp_tree(exp_tree):
	"""
将生成的二叉树进行标准化处理
parameters:
    exp_tree(dict)：表达式二叉树
return:
    value(float)：表达式的值
    max_value(float)：左右子树中的最大值
    key(str)：当前节点的操作符
"""
	(key, child), = exp_tree.items()  # 获取子树

	if type(child[0]) == type(1) or type(child[0]) == type(0.1):   # 左子树的操作数
		left_value = (child[0], 1)
		max_lvalue = child[0]
		left_operator = '_'          # 非操作符
	else:                            # 递归规范左子树
		left_value, max_lvalue, left_operator = to_reg_exp_tree(child[0])
		if left_value == None:
			return None, None, None
	if type(child[1]) == type(1) or type(child[1]) == type(0.1):  # 右子树的操作数
		right_value = (child[1], 1)
		max_rvalue = child[1]
		right_operator = '_'
	else:                            # 递归规范右子树
		right_value, max_rvalue, right_operator = to_reg_exp_tree(child[1])
		if right_value == None:
			return None, None, None
	left_value_sub = left_value[0] / left_value[1]
	right_value_sub = right_value[0] / right_value[1]
    # 进行表达式的规范化处理
	if ((max_lvalue < max_rvalue or (left_value_sub < right_value_sub and left_operator != '_' and right_operator != '_')
		or (max_lvalue == max_rvalue and (left_operator == '*' or (left_operator != '_' and
		right_operator == '_')))) and key in ['+', '*']):    # 进行表达式的规范化处理
		exp_tree[key] = [child[1], child[0]]                  # 交换左右子树
		(left_value, right_value) = (right_value, left_value)
    # 计算当前子树的最大操作数
	if max_lvalue >= max_rvalue:
		max_value = max_lvalue
	else:
		max_value = max_rvalue
    # 计算表达式的值
	value = calculate(key, left_value, right_value)

	return value, max_value, key


def calculate(operator, left_value, right_value):
	"""
计算字符串表达式的值
parameters:
    operator(str)：操作符
    left_value(float)：表达式的左操作数
    right_value(float)：表达式的右操作数
return:
    result(tuple)：分数组成的元组,第一个值为分子，第二个值为分母
"""
	tuple_type = type(())
	if operator == '+':
		if type(left_value) == tuple_type and type(right_value) == tuple_type:
			return (left_value[0]*right_value[1]+right_value[0]*left_value[1], left_value[1]*right_value[1])
		elif type(left_value) == tuple_type and type(right_value) != tuple_type:
			return (left_value[1]*right_value+left_value[0], left_value[1])
		elif type(left_value) != tuple_type and type(right_value) == tuple_type:
			return (left_value*right_value[1]+right_value[0], right_value[1])
		else:
			return (left_value + right_value, 1)
	elif operator == '-':
		if type(left_value) == tuple_type and type(right_value) == tuple_type:
			return (left_value[0]*right_value[1]-right_value[0]*left_value[1], left_value[1]*right_value[1])
		elif type(left_value) == tuple_type and type(right_value) != tuple_type:
			return (left_value[0]-left_value[1]*right_value, left_value[1])
		elif type(left_value) != tuple_type and type(right_value) == tuple_type:
			return (left_value*right_value[1]-right_value[0], right_value[1])
		else:
			return (left_value - right_value, 1)
	elif operator == '*':
		if type(left_value) == tuple_type and type(right_value) == tuple_type:
			return (left_value[0]*right_value[0], left_value[1]*right_value[1])
		elif type(left_value) == tuple_type and type(right_value) != tuple_type:
			return (left_value[0]*right_value, left_value[1])
		elif type(left_value) != tuple_type and type(right_value) == tuple_type:
			return (left_value*right_value[0], right_value[1])
		else:
			return (left_value * right_value, 1)

def generate_mid_exp(max_num):
	"""
	随机生成题目数量为n，数值在r以内的四则运算表达式
	parameters:
    	n(int)：四则运算表达式的个数
    	r(int)：操作数的值上界
	return:
    	mid_exps(list)：存储中缀表达式的列表
	"""
	data_num = 3                        # 操作数个数
	datas = []                          # 操作数
	operators = ['+', '-', '*']
	select_operators = []               # 操作符

	for i in range(data_num):          # 随机生成操作数
		data = int(random.random() * max_num)
		datas.append(data)
	for i in range(data_num - 1):      # 随机生成操作符
		operator = operators[int(random.random() * 3)]
		select_operators.append(operator)

    # 操作符只存在 + 或 *，进行特殊处理
	select_operators_set = set(select_operators)
	op = select_operators_set.copy().pop()
	reg_mid_exp = None
	expression_value = None
	if len(select_operators_set) == 1 and op in ['+', '*']:
		reg_mid_exp = list(map(str, sorted(datas, reverse=True)))
		expression_value = datas[0]
		for i in range(len(reg_mid_exp)-1):
			reg_mid_exp.insert(i*2+1, op)
			if op == '+':
				expression_value = expression_value + datas[i+1]
			else:
				expression_value = expression_value * datas[i+1]
    # 生成中缀表达式
	mid_exp = [datas[-1]]
	for i in range(data_num - 1):
		mid_exp.append(select_operators[i])
		mid_exp.append(datas[i])
	mid_exp = add_bracket(mid_exp, len(datas)) # 以33%的概率随机生成括号
	if reg_mid_exp == None:         # 操作符随机的情况
		return mid_exp, None, None
	else:                           # 操作符全为 + 或 * 的情况
		return mid_exp, ' '.join(reg_mid_exp), (expression_value,1)


def add_bracket(mid_exp, data_num):
	"""
	以67%的概率，给生成的表达式加上括号
	parameters:
    	mid_exp(list)：随机生成的表达式
    	data_num(int)：操作数个数
	return:
    	mid_exp(list)：处理后的中缀表达式
	"""
    # 为生成的表达式加括号
	bracket_way = random.randint(0, 4)
	prob = [1, 0, 2, 0, 3, 4]  # 以67%的概率加上括号，33%的概率不加括号
	bracket_way = prob[bracket_way]
	if bracket_way == 1:
		mid_exp.insert(0, '(')
		mid_exp.insert(4, ')')
	elif bracket_way == 2:
		mid_exp.insert(2, '(')
		mid_exp.append(')')
	return mid_exp


def generate_expressions(n, r):
	"""
	生成n个满足要求的四则运算表达式
	parameters:
    	n(int)：表达式的个数
    	r(int)：参与运算的操作数的上界
	结果生成两个文件，保存题目和答案
	"""
	mid_exps = []       # 生成的表达式
	answers = []        # 表达式对应的答案
	reg_mid_exps = []   # 规范化后的表达式
	equations = []
	exp_num = 0
	while exp_num != n:
		origin_exp, reg_mid_exp, answer = generate_mid_exp(r)  # 随机生成表达式
		if reg_mid_exp == None:
			mid_exp = origin_exp[:]
			post_exp = mid_expression_to_post_expression(mid_exp) # 生成后缀表达式
			exp_tree = post_expression_to_bitree(post_exp)  # 生成后缀表达式对应的二叉树
			(answer,_,_) = to_reg_exp_tree(exp_tree)        # 规范化生成的二叉树
			reg_mid_exp = exp_tree_to_mid_exp(exp_tree)     # 生成规范化后的中缀表达式
        # 判断生成的表达式是否重复
		if reg_mid_exp not in reg_mid_exps:
			if reg_mid_exp[0]=='(' and reg_mid_exp[-1]==')':
				reg_mid_exp = reg_mid_exp[1:-1]
			mid_exps.append(origin_exp)
            # 将表达式的值标准化
			answer = answer[0]
			equation = reg_mid_exp + '=' + str(answer)
			answers.append(answer)
			reg_mid_exps.append(reg_mid_exp)
			equations.append(equation) 
			exp_num += 1
        
	return equations