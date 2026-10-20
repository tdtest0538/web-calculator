"""安全表达式计算引擎。

使用 ast 模块解析表达式，仅允许白名单中的运算符和节点类型，
避免 eval() 的安全风险。
"""

import ast
import operator


class Calculator:
    """安全表达式计算器"""

    # 如下这段代码定义了允许的二元运算符和对应的操作函数
    _BINOPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    # 允许的一元运算符
    _UNARYOPS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def calculate(self, expression: str) -> float:
        """计算表达式并返回结果。

        Args:
            expression: 数学表达式字符串

        Returns:
            计算结果

        Raises:
            ValueError: 表达式不合法
        """
        try:
            tree = ast.parse(expression.strip(), mode="eval")
            return self._eval_node(tree.body)
        except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
            raise ValueError(f"表达式不合法: {e}")

    def _eval_node(self, node: ast.AST) -> float:
        """递归计算 AST 节点。

        Args:
            node: AST 节点

        Returns:
            节点计算结果，neg 表示是否为负数
        """
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"不支持的值类型: {type(node.value).__name__}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._BINOPS:
                raise ValueError(f"不支持的运算符: {op_type.__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._BINOPS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._UNARYOPS:
                raise ValueError(f"不支持的一元运算符: {op_type.__name__}")
            operand = self._eval_node(node.operand)
            return self._UNARYOPS[op_type](operand)

        raise ValueError(f"不支持的表达式元素: {type(node).__name__}")