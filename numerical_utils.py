import ast
import math
from typing import Dict, List, Sequence

import sympy as sp


DEFAULT_LOCALS = {
    "E": sp.E,
    "pi": sp.pi,
    "abs": sp.Abs,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
}


def round_sig(value: float, digits: int = 3) -> float:
    if value == 0 or not math.isfinite(value):
        return float(value)
    sign = -1.0 if value < 0 else 1.0
    value = abs(float(value))
    exponent = math.floor(math.log10(value))
    factor = 10 ** (digits - 1 - exponent)
    return sign * round(value * factor) / factor


def parse_expression(expr_str: str, extra_locals:
                     Dict[str, object] | None = None) -> sp.Expr:
    expr = expr_str.strip().replace("·", ".").replace("^", "**")
    locals_dict = dict(DEFAULT_LOCALS)
    if extra_locals:
        locals_dict.update(extra_locals)
    return sp.sympify(expr, locals=locals_dict)


def make_numeric_function(expr_str: str, symbol_name: str = "x"):
    symbol = sp.Symbol(symbol_name)
    expr = parse_expression(expr_str, {symbol_name: symbol})
    return symbol, expr, sp.lambdify(symbol, expr, "math")


def make_multivariate_function(expr_str: str, variable_names: Sequence[str]):
    symbols = sp.symbols(" ".join(variable_names))
    if not isinstance(symbols, tuple):
        symbols = (symbols,)
    locals_dict = {name: sym for name, sym in zip(variable_names, symbols)}
    expr = parse_expression(expr_str, locals_dict)
    return symbols, expr


def evaluate_rounded_expression(
    expr_str: str,
    digits: int = 3,
    variables: Dict[str, float] | None = None,
) -> float:
    expr = expr_str.strip().replace("·", ".").replace("^", "**")
    tree = ast.parse(expr, mode="eval")
    values = {"pi": math.pi, "e": math.e, "E": math.e}
    if variables:
        values.update(variables)

    allowed_funcs = {
        "abs": abs,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "ln": math.log,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
    }

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return round_sig(float(node.value), digits)
            raise ValueError("Unsupported constant")
        if isinstance(node, ast.Name):
            if node.id not in values:
                raise ValueError(f"Unknown variable '{node.id}'")
            return round_sig(float(values[node.id]), digits)
        if isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return round_sig(+operand, digits)
            if isinstance(node.op, ast.USub):
                return round_sig(-operand, digits)
            raise ValueError("Unsupported unary operator")
        if isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            if isinstance(node.op, ast.Add):
                result = left + right
            elif isinstance(node.op, ast.Sub):
                result = left - right
            elif isinstance(node.op, ast.Mult):
                result = left * right
            elif isinstance(node.op, ast.Div):
                result = left / right
            elif isinstance(node.op, ast.Pow):
                result = left**right
            else:
                raise ValueError("Unsupported binary operator")
            return round_sig(result, digits)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function call")
            func_name = node.func.id
            if func_name not in allowed_funcs:
                raise ValueError(f"Function '{func_name}' not allowed")
            args = [eval_node(arg) for arg in node.args]
            result = allowed_funcs[func_name](*args)
            return round_sig(result, digits)
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    return float(eval_node(tree))


def read_number_list(text: str) -> List[float]:
    parts = [part.strip() for part in text.replace(";", ",").split(",")]
    return [float(part) for part in parts if part]


def read_symbolic_list(text: str) -> List[str]:
    return [part.strip() for part in text.replace(";", ",").split(",")
            if part.strip()]
