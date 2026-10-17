import ast
import os
import sys
import importlib.util
from typing import List, Optional
# NEGATIVE
def flatten_python_project(entry_file_path: str, base_path: str = ".") -> str:
    """
    Recursively flattens a project and merges imports into the file.Helper for sandalone script building. 
    """
    seen_paths = set()
    result_parts = []
    abs_base = os.path.abspath(base_path)

    def _resolve_module(name: str) -> Optional[str]:
        # Add base_path to sys.path temporarily to help find_spec find local modules
        original_path = sys.path.copy()
        if abs_base not in sys.path: sys.path.insert(0, abs_base)
        try:
            spec = importlib.util.find_spec(name)
            if spec and spec.origin and os.path.isfile(spec.origin) and spec.origin.endswith('.py'):
                # Only return if it's inside our base_path (local dependency)
                full_origin = os.path.abspath(spec.origin)
                if full_origin.startswith(abs_base):
                    return full_origin
        except Exception:
            pass
        finally:
            sys.path = original_path
        return None

    def _process_file(abs_path: str):
        if abs_path in seen_paths: return
        seen_paths.add(abs_path)

        with open(abs_path, 'r', errors='ignore') as f:
            source = f.read()
        
        try:
            tree = ast.parse(source)
        except Exception:
            return

        lines_to_scrub = set()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = []
                if isinstance(node, ast.Import):
                    names = [n.name for n in node.names]
                else:
                    if node.module: names = [node.module]
                
                resolved_path = None
                for name in names:
                    temp_path = _resolve_module(name)
                    if temp_path and temp_path != abs_path:
                        resolved_path = temp_path
                        break
                
                if resolved_path:
                    _process_file(resolved_path)
                    start = node.lineno
                    end = getattr(node, 'end_lineno', start)
                    for i in range(start, end + 1):
                        lines_to_scrub.add(i)

        source_lines = source.splitlines()
        cleaned_content = "\n".join([
            line for i, line in enumerate(source_lines, 1)
            if i not in lines_to_scrub
        ])

        result_parts.append(f"# --- START: {abs_path} ---\n{cleaned_content.strip()}")

    entry_abs = os.path.abspath(os.path.join(abs_base, entry_file_path))
    _process_file(entry_abs)
    
    return "\n\n".join(result_parts)
