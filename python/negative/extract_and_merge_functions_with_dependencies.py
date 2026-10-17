def extract_and_merge_functions_with_dependencies(code: str) -> list:
    """
    From plain Python code, extract all top-level functions,
    find their related dependencies (variables, classes),
    and return a list of new function definitions where
    dependencies are inlined as indented code blocks inside the function body.
    """
    import ast
    import builtins

    def get_source_segment(code, node):
        lines = code.splitlines()
        return "\n".join(lines[node.lineno - 1: node.end_lineno])

    def get_function_dependencies(func_node, globals_map):
        used = []
        for n in ast.walk(func_node):
            if isinstance(n, ast.Name):
                if n.id not in used:
                    used.append(n.id)
            elif isinstance(n, ast.Attribute):
                if isinstance(n.value, ast.Name):
                    full_name = f"{n.value.id}.{n.attr}"
                    if full_name not in used:
                        used.append(full_name)
                    if n.value.id not in used:
                        used.append(n.value.id)

        local_vars = {arg.arg for arg in func_node.args.args}

        for n in ast.walk(func_node):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        local_vars.add(t.id)

        built_in = set(dir(builtins))
        deps = [d for d in used if d.split('.')[0] not in local_vars and d.split('.')[0] not in built_in and d.split('.')[0] != func_node.name and d.split('.')[0] in globals_map]

        return deps

    def add_indent_to_each_line(text: str, sub: str = '\t') -> str:
        return '\n'.join([sub + line if line.strip() else '' for line in text.splitlines()])

    def extract_globals(code: str):
        tree = ast.parse(code)
        globals_map = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Assign)):
                if isinstance(node, ast.Assign):
                    # use first target name
                    target = node.targets[0]
                    if isinstance(target, ast.Name):
                        globals_map[target.id] = node
                else:
                    globals_map[node.name] = node
        return {'globals_map': globals_map}

    if code is None or not code.strip():
        return []

    globals_ = extract_globals(code)
    globals_map = globals_['globals_map']
    functions = []

    for name, node in globals_map.items():
        if isinstance(node, ast.FunctionDef):
            func_origin = get_source_segment(code, node)
            related_blocks = []
            deps = get_function_dependencies(node, globals_map)

            for rel_name in deps:
                base_name = rel_name.split('.')[0]
                attr = rel_name.split('.')[1] if '.' in rel_name else None
                rel_node = globals_map.get(base_name)
                if rel_node:
                    rel_origin = get_source_segment(code, rel_node)
                    indented = add_indent_to_each_line(rel_origin)
                    related_blocks.append(indented)

            lines = func_origin.splitlines()
            if not lines:
                continue
            def_line = lines[0]
            body_lines = lines[1:]

            merged = [def_line] + related_blocks + body_lines
            functions.append('\n'.join(merged))

    return functions