#works?
def extract_and_merge_functions_with_dependencies_and_imports_from_outside_the_new_functions(code: str) -> list:
    """
    Extracts each top-level function from code and returns standalone versions,
    where:
    - All required dependencies (import, from ... import, classes, variables)
      are included INSIDE the function body, properly indented.
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
                    base = n.value.id
                    full = f"{base}.{n.attr}"
                    if full not in used:
                        used.append(full)
                    if base not in used:
                        used.append(base)

        local_vars = {arg.arg for arg in func_node.args.args}
        for n in ast.walk(func_node):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        local_vars.add(t.id)

        built_in = set(dir(builtins))
        deps = [d for d in used if d.split('.')[0] not in local_vars and d.split('.')[0] not in built_in]
        return deps

    def add_indent(text: str, prefix: str = '\t') -> str:
        return '\n'.join([prefix + line if line.strip() else '' for line in text.splitlines()])

    def extract_globals(code: str):
        tree = ast.parse(code)
        globals_map = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                target = node.targets[0]
                if isinstance(target, ast.Name):
                    globals_map[target.id] = node
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                globals_map[node.name] = node
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    name = alias.asname or alias.name
                    globals_map[name] = node
        return globals_map

    if not code or not code.strip():
        return []

    globals_map = extract_globals(code)
    functions = []

    for name, node in globals_map.items():
        if not isinstance(node, ast.FunctionDef):
            continue

        func_origin = get_source_segment(code, node)
        deps = get_function_dependencies(node, globals_map)
        seen_nodes = set()
        inlined_blocks = []

        for dep_name in deps:
            base_name = dep_name.split('.')[0]
            rel_node = globals_map.get(base_name)
            if not rel_node:
                continue
            node_id = id(rel_node)
            if node_id in seen_nodes:
                continue
            seen_nodes.add(node_id)
            code_segment = get_source_segment(code, rel_node)
            inlined_blocks.append(add_indent(code_segment))

        lines = func_origin.splitlines()
        if not lines:
            continue
        def_line = lines[0]
        func_body = lines[1:]

        merged_func = [def_line] + inlined_blocks + func_body
        functions.append('\n'.join(merged_func))

    return functions

#from open_and_read_local_python_file_to_plain import open_and_read_local_python_file_to_plain
#path = '/home/wsl/app/test_data/untitled.py'
#code = open_and_read_local_python_file_to_plain(path)
#counter = 0
#for i in extract_and_merge_functions_with_dependencies_and_imports_from_outside_the_new_functions(code):
#    with open(f'test{counter}.py','w') as f:
#        f.write(i)
#        counter += 1