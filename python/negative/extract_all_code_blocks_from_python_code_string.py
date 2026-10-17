import ast
import tokenize
from io import StringIO

def extract_all_code_blocks_from_python_code_string(source_code):
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)
    results = []
    
    # Tokenize entire source to find all comments
    comment_map = {}
    tokens = list(tokenize.generate_tokens(StringIO(source_code).readline))
    for toknum, tokval, (srow, scol), (_, _), _ in tokens:
        if toknum == tokenize.COMMENT:
            comment_map.setdefault(srow, []).append(tokval.strip())

    def extract_lines(start, end):
        result = []
        for lineno in range(start, end + 1):
            raw_line = lines[lineno - 1]
            stripped = raw_line.strip()
            leading_ws = raw_line[:len(raw_line) - len(raw_line.lstrip())]
            spaces = sum(1 for ch in leading_ws if ch in (' ', '\t'))

            code_part = None
            comment_part = None

            if '#' in raw_line:
                code_raw, comment_raw = raw_line.split('#', 1)
                code_part = code_raw.strip() or None
                comment_part = '#' + comment_raw.strip()
            else:
                code_part = stripped or None

            if lineno in comment_map and comment_part is None:
                comment_part = ' '.join(comment_map[lineno])

            result.append({
                'line': {
                    'type': 'text',
                    'code': code_part,
                    'comment': comment_part
                },
                'spaces': spaces if stripped else 0,
                'strip': stripped
            })
        return result

    def extract_functions():
        functions = sorted(
            [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))],
            key=lambda n: n.lineno
        )
        function_blocks = []
        covered_lines = set()

        for func in functions:
            start = func.lineno
            end = getattr(func, 'end_lineno', func.lineno)
            covered_lines.update(range(start, end + 1))
            function_blocks.append({
                'type': 'function',
                'block': func.name,
                'lines': extract_lines(start, end)
            })

        return function_blocks, covered_lines

    def extract_classes():
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        class_blocks = []
        covered_lines = set()

        for class_node in classes:
            start = class_node.lineno
            end = getattr(class_node, 'end_lineno', class_node.lineno)
            covered_lines.update(range(start, end + 1))
            class_blocks.append({
                'type': 'class',
                'block': class_node.name,
                'lines': extract_lines(start, end)
            })

        return class_blocks, covered_lines

    def extract_variables():
        variables = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append(target.id)
        return list(set(variables))

    def extract_execution_block(covered_lines):
        # Detecting if __name__ == "__main__"
        execution_block = []
        if '__name__' in source_code:
            if '__main__' in source_code:
                start = source_code.find('__name__')
                end = source_code.find('__main__') + len('__main__')
                execution_block.append({
                    'type': 'execution',
                    'block': '__name__ == "__main__"',
                    'lines': extract_lines(start, end)
                })
        return execution_block

    # Extract all blocks
    functions, covered_lines = extract_functions()
    classes, class_covered_lines = extract_classes()
    variables = extract_variables()
    execution_block = extract_execution_block(covered_lines | class_covered_lines)

    # Now combine everything
    all_blocks = []
    all_blocks.extend(functions)
    all_blocks.extend(classes)
    all_blocks.extend(execution_block)

    # Also extract top-level comments (module-level) outside functions/classes
    module_comment_lines = [
        lineno for lineno in comment_map.keys() if lineno not in covered_lines and lineno not in class_covered_lines
    ]
    
    if module_comment_lines:
        min_line = min(module_comment_lines)
        max_line = max(module_comment_lines)
        all_blocks.insert(0, {
            'type': 'module',
            'block': 'module_comments',
            'lines': extract_lines(min_line, max_line)
        })
    
    # Include variables (if any) as a separate block
    if variables:
        all_blocks.append({
            'type': 'variables',
            'block': 'variable_definitions',
            'lines': [{'line': {'type': 'text', 'code': var, 'comment': None}, 'spaces': 0, 'strip': var} for var in variables]
        })
    
    return all_blocks

# Example
code = '''
# module-level comment
# another comment

def foo(x):
    # Check if x is positive
    if x > 0:
        return x  # return as is
    else:
        return -x  # return negated

def bar():
    print("Hello")  # greeting

# End of script check
if __name__ == "__main__":
    print("This script is being executed.")
'''

#from pprint import pprint
#pprint(extract_all_code_blocks_from_python_code_string(code), width=150)#out: IndexError