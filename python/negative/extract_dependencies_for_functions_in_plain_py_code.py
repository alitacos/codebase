from open_and_read_local_python_file_to_plain import open_and_read_local_python_file_to_plain

path = '/home/wsl/app/test_data/untitled.py'
code = open_and_read_local_python_file_to_plain(path)

def extract_dependencies_for_functions_in_plain_py_code(code: str = None) -> list:
    import ast
    import builtins

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

        return deps  # keep order of usage

    def get_source_segment(code, node):
        lines = code.splitlines()
        return "\n".join(lines[node.lineno - 1: node.end_lineno])

    if code is None or not code.strip():
        return []

    globals_ = extract_globals(code)
    data = []

    for k, node in globals_['globals_map'].items():
        if isinstance(node, ast.FunctionDef):
            item = {
                'name': k,
                'node': node,
                'related': [],
                'origin': get_source_segment(code, node)
            }

            rels = get_function_dependencies(node, globals_['globals_map'])

            for rel_name in rels:
                base_name = rel_name.split('.')[0]
                attr = rel_name.split('.')[1] if '.' in rel_name else None
                rel_node = globals_['globals_map'].get(base_name)

                if rel_node:
                    related_entry = {
                        'name': rel_name,
                        'node': rel_node,
                        'origin': get_source_segment(code, rel_node)
                    }
                    if attr:
                        related_entry['attr'] = attr
                    item['related'].append(related_entry)

            if k and node and item['related']:
                data.append(item)

    return data
#extract_dependencies_for_functions_in_plain_py_code(code)