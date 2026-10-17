def extract_dependencies_for_functions_in_plain_py_code(code:str=None) -> list:
    def get_function_dependencies(func_node, globals_map):
        import ast
        import builtins
        used = []
        for n in ast.walk(func_node):
            if isinstance(n, ast.Name):
                if n.id not in used:
                    used.append(n.id)
            elif isinstance(n, ast.Attribute):
                if isinstance(n.value, ast.Name):
                    if n.value.id not in used:
                        used.append(n.value.id)
        local_vars = {arg.arg for arg in func_node.args.args}
        for n in ast.walk(func_node):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        local_vars.add(t.id)
        built_in = set(dir(builtins))
        deps = [d for d in used if d not in local_vars and d not in built_in and d != func_node.name and d in globals_map]
        return deps  # keep order of usage
    def get_source_segment(code, node):
        lines = code.splitlines()
        return "\n".join(lines[node.lineno - 1: node.end_lineno])
    if code is None or not code or not str(code).strip():
        return []
    globals_ = extract_globals(code)
    data = []
    for k,node in globals_['globals_map'].items():
        if 'ast.FunctionDef' in str(node):
            item = {'name':k,'node':node,'related':[],'origin':get_source_segment(code, node)}
            rel = get_function_dependencies(globals_['globals_map'][k], globals_['globals_map'])
            # HIER IS MY PROBLEM..... HOW TO GET THE SUB_NODE OF EACH RELATED OBJECT´s NAME?????
            if rel:
                for rel_name in rel:
                    rel_node = globals_['globals_map'].get(rel_name)
                    if rel_node:  # Make sure it exists
                        item['related'].append({
                            'name': rel_name,
                            'node': rel_node,
                            'origin': get_source_segment(code, rel_node)
                            })

                
                if k and v and item['related']:
                    data.append(item)
    return data


#extract_dependencies_for_functions_in_plain_py_code(code)