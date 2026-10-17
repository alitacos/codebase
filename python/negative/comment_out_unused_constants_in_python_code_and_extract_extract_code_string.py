def comment_out_unused_constants_in_python_code_and_extract_extract_code_string(code:str='')->str:
    
    def comment_out_unused_constants_in_python_code(code: str = '') -> str:
        """
        Comments out non-Python lines, unused top-level constants, imports, and expressions.
        """
        if not code:
            return ''
        import ast
    
        lines = code.splitlines()
    
        # Phase 1: Comment out lines that cause SyntaxErrors
        while True:
            try:
                source = "\n".join(lines)
                tree = ast.parse(source)
                break
            except SyntaxError as e:
                # Comment out the line where the syntax error occurred
                error_idx = e.lineno - 1
                if error_idx < len(lines):
                    if not lines[error_idx].strip().startswith('#'):
                        lines[error_idx] = '# ' + lines[error_idx]
                    else:
                        # If already commented but still failing, we must stop to avoid infinite loop
                        break
                else:
                    break
    
        # Phase 2: Identify unused top-level items
        try:
            final_source = "\n".join(lines)
            tree = ast.parse(final_source)
        except SyntaxError:
            return "\n".join(lines)
    
        class UsedNameCollector(ast.NodeVisitor):
            def __init__(self):
                self.used_names = set()
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    self.used_names.add(node.id)
                self.generic_visit(node)
    
        used_names = set()
        # Collect names used in functions/classes
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                collector = UsedNameCollector()
                collector.visit(node)
                used_names.update(collector.used_names)
    
        lines_to_comment = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
    
            start_lineno = getattr(node, "lineno", None)
            end_lineno = getattr(node, "end_lineno", start_lineno)
    
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split('.')[0] for alias in node.names]
                if not any(name in used_names for name in names):
                    lines_to_comment.update(range(start_lineno, end_lineno + 1))
    
            elif isinstance(node, ast.Assign):
                target_names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                if target_names and not any(name in used_names for name in target_names):
                    lines_to_comment.update(range(start_lineno, end_lineno + 1))
    
            elif isinstance(node, ast.Expr):
                lines_to_comment.update(range(start_lineno, end_lineno + 1))
    
        for lineno in sorted(lines_to_comment):
            idx = lineno - 1
            if idx < len(lines) and not lines[idx].lstrip().startswith("#"):
                lines[idx] = "# " + lines[idx]
    
        return "\n".join(lines


    def extract_code_string_from_outcommented_text(text:str=None)->str:
        import ast
        code = None
        try:
            node = ast.parse(text)
            code =  ast.unparse(node)
        except Exception as e:
            try:
                text = comment_out_unused_constants_in_python_code(test)
                node = ast.parse(text)
                code =  ast.unparse(node)
            except Exception as e1:
                code =  None
        return code

    text = comment_out_unused_constants_in_python_code(code)
    return extract_code_string_from_outcommented_text(text)