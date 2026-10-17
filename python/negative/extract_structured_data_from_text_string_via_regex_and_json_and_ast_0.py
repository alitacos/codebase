def extract_structured_data_from_text_string_via_regex_and_json_and_ast(text: str) -> list:
    import ast
    import json
    import re

    def json_literals_to_python(s):
        """Convert JSON literals outside quoted strings."""
        result = []
        i = 0
        in_string = False
        escape = False

        while i < len(s):
            char = s[i]

            if in_string:
                result.append(char)

                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False

                i += 1
                continue

            if char == '"':
                in_string = True
                result.append(char)
                i += 1
                continue

            # Replace JSON literals only outside strings
            matched = False
            for json_value, python_value in (
                ("null", "None"),
                ("true", "True"),
                ("false", "False"),
            ):
                if s.startswith(json_value, i):
                    before = s[i - 1] if i > 0 else ""
                    after = s[i + len(json_value)] if i + len(json_value) < len(s) else ""

                    if not (before.isalnum() or before == "_") and \
                       not (after.isalnum() or after == "_"):
                        result.append(python_value)
                        i += len(json_value)
                        matched = True
                        break

            if not matched:
                result.append(char)
                i += 1

        return "".join(result)

    results = []
    i = 0

    while i < len(text):
        if text[i] not in "[{":
            i += 1
            continue

        candidate = text[i:]

        # ---------------------------------------------------------
        # Try JSON
        # ---------------------------------------------------------
        try:
            decoder = json.JSONDecoder()
            value, end = decoder.raw_decode(candidate)

            if isinstance(value, (list, dict, set)):
                results.append(value)
                i += end
                continue

        except json.JSONDecodeError:
            pass

        # ---------------------------------------------------------
        # Try Python literal / JSON-like Python literal
        # ---------------------------------------------------------
        python_candidate = json_literals_to_python(candidate)

        try:
            value = ast.literal_eval(python_candidate)

            if isinstance(value, (list, dict, set)):
                # Find the actual end of the parsed literal.
                # literal_eval doesn't expose the consumed length,
                # so use the AST parser progressively.
                for end in range(1, len(python_candidate) + 1):
                    try:
                        ast.literal_eval(python_candidate[:end])
                        if python_candidate[end:].strip() == "":
                            results.append(value)
                            i = len(text)
                            break
                    except (ValueError, SyntaxError):
                        continue
                else:
                    i += 1
                continue

        except (ValueError, SyntaxError, TypeError):
            pass

        i += 1

    return results
#example usage:
#extract_structured_data_from_text_string_via_regex_and_json_and_ast("Result: {'a', 1, 'c'},, ok {'q', 3, 'c'}")

# negative
#error ..extracts only the first found dict or list or json and the rest is excluded
