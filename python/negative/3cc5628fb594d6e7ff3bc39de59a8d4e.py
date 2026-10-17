def check_if_src_is_single_function_candidate(src:str|bytes|ast.AST=None)->float: #  
    def clean_body_from_top_level_imports_and_constants_up_to_next_diff_instance(node:ast.AST=None)->ast.AST|None:
        # code can be used for example if we want to label if a script is a single function or many etc. so we clean from top level constants and imports to double check later. can also have other uses. just to clean for whatever reason the spesific region
        """
        """
        def functreebodylist2func(body_list: list[ast.stmt]) -> ast.AST:
            try:
                return ast.Module(body=body_list, type_ignores=[])
            except Exception:
                return  None

        if not node:
            return None
        try:
            if not isinstance(node, (str,bytes)):
                try:
                    node = ast.parse(node)
                    node_body = node.body
                except Exception as e:
                    return None
            if isinstance(node, ast.AST) and not hasattr(node, "body") or (isinstance(node, ast.AST) and not isinstance(node.body, list)):
                return None
            if not isinstance(node, ast.AST):
                #node = ast.parse(node)
                node_body = node.body
            if isinstance(node, list):
                for i in node:
                    if not isinstance(i, ast.AST):
                      return None
                node_body = node
                node = functreebodylist2func(node_body)
            #if len(node.body) == 1 isinstance(node, (ast.AsyncFunctionDef,ast.FunctionType, ast.AsyncFunctionDef))   :
            #    return node.body[0]
            for item in node.body[:]:

                # remove imports
                if isinstance(item, (ast.Import, ast.ImportFrom)):
                    node.body.remove(item)
                    continue

                # remove assignments (x = ...)
                if isinstance(item, ast.Assign):
                    node.body.remove(item)
                    continue

                # remove annotated assignments (x: int = ...)
                if isinstance(item, ast.AnnAssign):
                    node.body.remove(item)
                    continue
            return node
        except Exception as e:
            return None

    def check_if_src_is_single_function(src:str|bytes|ast.AST=None)->float: #  
        """
        Determines whether the given source represents exactly one top-level Python function definition using AST parsing. The function performs a strict structural check on module-level AST nodes and returns a confidence-style score where 1.0 indicates that the input is a valid single function module, and 0.0 indicates that the input either does not contain a function, contains multiple top-level elements, or is invalid/unparsable. It does not analyze function internals or nested structures beyond the top-level module body.

        Args:
            src (str | bytes | ast.AST): Input Python source code or AST node. If a string or bytes object is provided, it is parsed using ast.parse; if parsing fails or the type is unsupported, the function returns 0.0.

        Returns:
            float: Returns 1.0 if the input represents exactly one top-level function definition (FunctionDef or AsyncFunctionDef). Returns 0.0 if the input is invalid, contains no function, contains multiple top-level nodes, or the single top-level node is not a function definition.

        Example usage:
            >>> result = check_if_src_is_single_function(src='def f(): pass')
        """
        # 1. Initial input check: if src is already an AST function node
        if isinstance(src, (ast.FunctionDef, ast.AsyncFunctionDef)):  # direct function node check (already parsed AST function)
            return 1.0 # Return simple score for basic valid function node

        # 2. Parse src if it's a string, or use directly if it's an AST tree
        tree = None
        if isinstance(src, (ast.AST, ast.Module)):  # already an AST node, no parsing needed
            tree = src
        if isinstance(src, (str,bytes)):  # raw source input that must be parsed
            try:
                tree = ast.parse(src)  # convert source code into AST module
            except SyntaxError:
                return 0.0 # invalid Python syntax cannot be processed

        if not src or not isinstance(src, ast.AST) or not tree or tree is None or len(tree.body) == 0:  # empty module or failed parsing result
            print('debug : 1')
            return 0.0

        has_function = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in tree.body)  # check if any top-level function exists

        if not has_function:  # early rejection if no function is present
            print('debug : 2')
            return 0.0

        if len(tree.body) == 1 and isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):  # strict single-function module check
            print('debug : 3')
            return 1.0      
        elif len(tree.body) == 1 and not isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):  # single node but not a function
            print('debug : 4')
            return 0.0   
        else:
            tree_body = clean_body_from_top_level_imports_and_constants_up_to_next_diff_instance(tree)
            print(tree_body)
            if not tree_body or tree_body == tree.body: # no need to check further if same again
                print('debug : 5')
                return 0.0
            has_function = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in tree_body)  # check if any top-level function exists
            if not has_function or (has_function and len(tree_body) != 1):  # early rejection if no function is present or other elements
                return 0.0 # multiple top-level statements (could be extended scoring logic in future)
            if len(tree_body) == 1 and isinstance(tree_body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):  # strict single-function module check
                return 1.0      
            elif len(tree_body) == 1 and not isinstance(tree_body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):  # single node but not a function
                return 0.0   
        return 0.0   
    return check_if_src_is_single_function(src)