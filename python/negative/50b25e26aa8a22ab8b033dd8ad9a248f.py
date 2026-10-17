import ast

def check_if_src_is_single_function(src):
    class FunctionNameAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.loaded_names = set()
            self.shadowed_names = set() # Names that are function parameters or assigned to locally

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                self.loaded_names.add(node.id)
            elif isinstance(node.ctx, ast.Store):
                # Names assigned locally within the function body shadow globals
                self.shadowed_names.add(node.id)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # Parameters shadow globals
            all_args = node.args.args + node.args.kwonlyargs + getattr(node.args, 'posonlyargs', [])
            for arg in all_args:
                self.shadowed_names.add(arg.arg)
                # Collect names from argument type annotations and default values
                if arg.annotation:
                    self._collect_names_from_expr(arg.annotation)
                if arg.default:
                    self._collect_names_from_expr(arg.default)

            # Handle vararg (*args) and kwarg (**kwargs)
            if node.args.vararg:
                self.shadowed_names.add(node.args.vararg.arg)
            if node.args.kwarg:
                self.shadowed_names.add(node.args.kwarg.arg)

            # Collect names from function return annotation
            if node.returns:
                self._collect_names_from_expr(node.returns)

            # Continue visiting the function body and decorators to find other loaded and assigned names
            for stmt in node.body:
                self.visit(stmt)
            for decorator in node.decorator_list:
                self.visit(decorator)

        def visit_AsyncFunctionDef(self, node):
            # Apply the same logic for async functions
            self.visit_FunctionDef(node)

        def _collect_names_from_expr(self, expr):
            # Helper to collect all loaded names from an arbitrary expression (e.g., annotations, default values)
            for sub_node in ast.walk(expr):
                if isinstance(sub_node, ast.Name) and isinstance(sub_node.ctx, ast.Load):
                    self.loaded_names.add(sub_node.id)

    if isinstance(src, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return True

    tree = None
    if isinstance(src, ast.AST):
        tree = src
    elif isinstance(src, (str, bytes)): # Handle both string and bytes source
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return False # Not valid Python syntax
    else:
        return False # Invalid source type

    if tree is None or not tree.body:
        return False

    func_node_index = -1
    for i, node in enumerate(tree.body):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if func_node_index != -1: # Found a second function definition
                return False
            func_node_index = i

    if func_node_index == -1: # No function definition found in the source
        return False

    # Check for any code existing after the function definition
    if func_node_index < len(tree.body) - 1:
        return False

    func_node = tree.body[func_node_index]

    # Analyze the function node to find all loaded and shadowed names
    analyzer = FunctionNameAnalyzer()
    analyzer.visit(func_node)

    # Track names defined by leading import/assign statements
    leading_defined_names = set()
    for i in range(func_node_index):
        node = tree.body[i]
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                leading_defined_names.add(name)
        elif isinstance(node, ast.Assign):
            # Only support simple Name assignments for leading constants for now
            # As per previous discussion, complex assignments like x,y = 1,2 would need further refinement.
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                leading_defined_names.add(node.targets[0].id)
            else:
                return False # Disallow complex assignment targets for leading statements
        else:
            return False # Only imports and assignments are allowed before the function

    # Verify that all leading defined names are truly used and not shadowed
    for name in leading_defined_names:
        # A leading name is considered 'used' only if it's loaded within the function
        # AND it's not shadowed by a function parameter or local assignment.
        if name not in analyzer.loaded_names or name in analyzer.shadowed_names:
            return False

    return True

