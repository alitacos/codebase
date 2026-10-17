import ast
def extract_FunctionDef_to_sample_parsable_funcSnippets_in_ast_node_and_clean_comments(ast_tree:ast.Module=None,functionNames:list=None)->list:
    top_imports = []
    for node in ast_tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imp_name = alias.asname or alias.name.split('.')[0]
                line = f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else "")
                top_imports.append((line, imp_name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imp_name = alias.asname or alias.name
                line = f"from {module} import {alias.name}" + (f" as {alias.asname}" if alias.asname else "")
                top_imports.append((line, imp_name))
    top_imports = list(dict(top_imports).items())

    def walk_functions(node):
        functions = []
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(child)
                functions.extend(walk_functions(child))
            elif isinstance(child, ast.ClassDef):
                functions.extend(walk_functions(child))
        return functions

    func_nodes = walk_functions(ast_tree)
    func_map = {f.name: f for f in func_nodes}
    results = []

    for f_node in func_nodes:
        local_defs = {n.name for n in ast.walk(f_node) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        names_used = {n.id for n in ast.walk(f_node) if isinstance(n, ast.Name)}

        # Track names used specifically in hints of the parent
        hint_names = set()
        if f_node.returns:
            hint_names.update(n.id for n in ast.walk(f_node.returns) if isinstance(n, ast.Name))
        for arg in f_node.args.args + f_node.args.kwonlyargs:
            if arg.annotation:
                hint_names.update(n.id for n in ast.walk(arg.annotation) if isinstance(n, ast.Name))

        deps_to_inject = []
        for name in list(names_used):
            if name in func_map and name != f_node.name and name not in local_defs:
                dep_node = func_map[name]
                dep_code = ast.unparse(dep_node)
                indented_dep = textwrap.indent(dep_code, '    ')
                deps_to_inject.append(indented_dep)
                # If the injected dependency uses a name, parent 'uses' it too
                dep_names = {n.id for n in ast.walk(dep_node) if isinstance(n, ast.Name)}
                names_used.update(dep_names)
                # Crucially check if the dependency uses a name in its signature hints
                if dep_node.returns:
                    hint_names.update(n.id for n in ast.walk(dep_node.returns) if isinstance(n, ast.Name))
                for arg in dep_node.args.args + dep_node.args.kwonlyargs:
                    if arg.annotation:
                        hint_names.update(n.id for n in ast.walk(arg.annotation) if isinstance(n, ast.Name))

        outside_lines = []
        inside_lines = []
        for line, imp_name in top_imports:
            if imp_name in names_used:
                if imp_name in hint_names:
                    outside_lines.append(line)
                else:
                    inside_lines.append("    " + line)

        f_code = textwrap.dedent(ast.unparse(f_node))
        lines = f_code.splitlines()

        insert_idx = 1
        if len(lines) > 1 and lines[1].strip().startswith(("\"\"\"", "'''")):
            for i in range(1, len(lines)):
                if lines[i].strip().endswith(("\"\"\"", "'''")):
                    insert_idx = i + 1
                    break

        for dep in reversed(deps_to_inject):
            lines.insert(insert_idx, "")
            lines.insert(insert_idx, dep)

        if inside_lines:
            for iline in reversed(inside_lines):
                lines.insert(insert_idx, iline)

        final_code = "\n".join(outside_lines) + ("\n\n" if outside_lines else "") + "\n".join(lines)

        try:
            #info = extract_function_info(final_code)
            #results.append({'code': final_code, 'info': info})#->list[dict]
            #results.append({'name':f_node.name, 'FunctionDef':ast.unparse(f_node), 'PreprocessImports':final_code})#->list[dict]
            #results.append(final_code)
        except:
            continue
    functionNames = [i.strip() for i in functionNames if i and isinstance(i,str) and i.strip()] 
    if not functionNames or (isinstance(functionNames,str) and not functionNames.strip()) or  (isinstance(functionNames, (list, set)) and not [a.strip() for a in functionNames if a and isinstance(a,str) and a.strip()]) or functionNames in [None, '*','**','***' ]:
        return results
    elif isinstance(functionNames,str):
        if functionNames in func_map:
            for rs in results:
                if rs.get('name','') ==:
                    return [rs]
    records = []
    elif isinstance(functionNames,(list,set)):
        for fName in functionNames:
            if fName in func_map:
                for rs in results:
                    if rs.get('name','') == fName:
                        if rs not in records:
                            records.append(rs)
        return records
    else:
        return results