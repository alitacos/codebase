import ast
import pprint
import re
from typing import Any, Union, List, Dict, Optional
import typing
import types

class CodeDetailsExtractor:
    """
    A robust utility to extract detailed information about functions and calls.
    Addresses previous bugs regarding argument ordering and default matching.
    """

    def __init__(self, code_str: str):
        self.code_str = code_str
        self.results: List[Dict[str, Any]] = []
        self._parse_code()

    def _parse_code(self):
        try:
            tree = ast.parse(self.code_str)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.results.append(self._extract_function_details(node))
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    self.results.append(self._extract_call_expression_details(node.value))
        except SyntaxError as e:
            print(f"Warning: CodeDetailsExtractor encountered SyntaxError: {e}")
            self.results = []

    def _get_annotation_str(self, node: Optional[ast.AST]) -> Optional[str]:
        if node is None: return None
        return ast.unparse(node).strip()

    def _extract_function_details(self, func_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Dict[str, Any]:
        args_obj = func_node.args
        args_dict = {}

        # 1. Positional-only
        for arg in getattr(args_obj, 'posonlyargs', []):
            args_dict[arg.arg] = self._build_arg_info(arg, kind='positional_only')

        # 2. Positional-or-Keyword
        n_args = len(args_obj.args)
        n_defaults = len(args_obj.defaults)
        for i, arg in enumerate(args_obj.args):
            default_node = None
            if i >= (n_args - n_defaults):
                default_node = args_obj.defaults[i - (n_args - n_defaults)]
            
            args_dict[arg.arg] = self._build_arg_info(
                arg, 
                kind='positional_or_keyword', 
                default_node=default_node
            )

        # 3. Varargs
        if args_obj.vararg:
            args_dict[f"*{args_obj.vararg.arg}"] = self._build_arg_info(args_obj.vararg, kind='var_positional')

        # 4. Keyword-only
        for arg, default_node in zip(args_obj.kwonlyargs, args_obj.kw_defaults):
            args_dict[arg.arg] = self._build_arg_info(
                arg, 
                kind='keyword_only', 
                default_node=default_node
            )

        # 5. Kwargs
        if args_obj.kwarg:
            args_dict[f"**{args_obj.kwarg.arg}"] = self._build_arg_info(args_obj.kwarg, kind='var_keyword')

        return {
            "kind": "function_definition",
            "name": func_node.name,
            "args_dict": args_dict,
            "returns": self._get_annotation_str(func_node.returns),
            "async": isinstance(func_node, ast.AsyncFunctionDef),
            "decorators": [ast.unparse(d) for d in func_node.decorator_list]
        }

    def _build_arg_info(self, arg_node: ast.arg, kind: str, default_node: Optional[ast.AST] = None) -> Dict[str, Any]:
        return {
            "type": self._get_annotation_str(arg_node.annotation),
            "default": ast.unparse(default_node) if default_node else None,
            "optional": default_node is not None,
            "kind": kind
        }

    def _extract_call_expression_details(self, call_node: ast.Call) -> Dict[str, Any]:
        return {
            "kind": "call_expression",
            "name": ast.unparse(call_node.func).strip(),
            "args": [ast.unparse(a) for a in call_node.args],
            "keywords": {kw.arg: ast.unparse(kw.value) for kw in call_node.keywords}
        }

    def reorder_parameters(self, src: str) -> str:
        """Reorders function parameters to place those with defaults after those without."""
        m = re.match(r"def\\s+(\\w+)\\\\(.*\\\\):(.*)", src, re.DOTALL)
        if not m: return src
        name, params_str, rest = m.groups()

        def split_params(p_str):
            res, cur, depth = [], [], 0
            for ch in p_str:
                if ch in "([{": depth += 1
                elif ch in ")]}": depth -= 1
                if ch == "," and depth == 0:
                    res.append("".join(cur).strip())
                    cur = []
                else: cur.append(ch)
            if cur: res.append("".join(cur).strip())
            return res

        params = split_params(params_str)
        no_default = [p for p in params if '=' not in p]
        with_default = [p for p in params if '=' in p]
        return f"def {name}({','.join(no_default + with_default)}):{rest}"

    def get_details(self) -> List[Dict[str, Any]]:
        return self.results