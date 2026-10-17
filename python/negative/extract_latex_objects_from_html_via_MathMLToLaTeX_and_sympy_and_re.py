def extract_latex_objects_from_html_via_MathMLToLaTeX_and_sympy_and_re(html_text):
    import re
    import html
    import sympy as sp
    from bs4 import BeautifulSoup, Tag
    from mathml_to_latex.converter import MathMLToLaTeX
    from sympy.parsing.latex import parse_latex
    
    converter = MathMLToLaTeX()
    
    
    def normalize_latex(value):
        if not value:
            return None
    
        value = html.unescape(value)
    
        # MathML invisible operators
        value = value.replace("\u2061", "")  # ⁡
        value = value.replace("\u2062", " ")  # ⁢
        value = value.replace("\u2063", " ")  # ⁣
        value = value.replace("\u2064", " ")  # ⁤
        value = value.replace("\u2060", "")
        value = value.replace("\ufeff", "")
    
        # Converter artifacts
        value = value.replace(r"\left(\right.", "(")
        value = value.replace(r"\left.\right)", ")")
        value = value.replace(r"\left[\right.", "[")
        value = value.replace(r"\left.\right]", "]")
        value = value.replace(r"\left(", "(")
        value = value.replace(r"\right)", ")")
        value = value.replace(r"\left[", "[")
        value = value.replace(r"\right]", "]")
    
        value = re.sub(r"\s+", " ", value).strip()
    
        return value or None
    
    
    def extract_math(element):
        if not isinstance(element, Tag):
            return None
    
        tag = element.name.lower()
    
        if tag == "latex":
            return normalize_latex(element.get_text())
    
        if tag != "math":
            return None
    
        # 1. alttext
        value = element.get("alttext")
        if value:
            value = normalize_latex(value)
            if value:
                return value
    
        # 2. TeX annotation
        tex_encodings = {"application/x-tex", "application/tex", "text/x-tex"}
    
        for annotation in element.find_all("annotation"):
            encoding = annotation.get("encoding", "").lower().strip()
            if encoding in tex_encodings:
                value = normalize_latex(annotation.get_text())
                if value:
                    return value
    
        # 3. Any annotation
        for annotation in element.find_all("annotation"):
            value = normalize_latex(annotation.get_text())
            if value:
                return value
    
        # 4. MathML -> LaTeX
        try:
            value = normalize_latex(converter.convert(str(element)))
            if value:
                return value
        except Exception:
            pass
    
        return None
    
    
    def latex_to_sympy(latex):
        latex = normalize_latex(latex)
        if not latex:
            return None
    
        try:
            return parse_latex(latex)
        except Exception:
            return None
    
    
    def latex_to_function(latex):
        expr = latex_to_sympy(latex)
    
        if expr is None:
            return None, None, None
    
        variables = sorted(expr.free_symbols, key=lambda x: x.name)
        function = sp.lambdify(variables, expr, modules="math")
    
        return function, variables, expr


    soup = BeautifulSoup(html_text, "html.parser")
    results = []

    for element in soup.find_all(["math", "latex"]):
        latex = extract_math(element)

        if not latex:
            continue

        function, variables, expression = latex_to_function(latex)

        results.append({
            "latex": latex,
            "expression": expression,
            "variables": variables,
            "function": function,
            "element": element
        })

    return results
