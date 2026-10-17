# PARTIALLY MISLEADING MEANING AND EXTRACTIONS


# extract from node1 and no2 the arguments along with their datatype and default {'key':str, 'type':type|types.Union|types.GenericAlias, 'value':object, 'hasDatatype':bool, 'hasDefault':bool'}# Note if has default and is None, then value == None hasDefault == True, if has no default the value == None hasDefault =False, isKwarg, isPosonlyarg,isVararg,iskwarg,  isKwonlyarg, isNormal}
import ast
import typing
import types

def get_arg_details_list(func_node: ast.FunctionDef):
    arguments = func_node.args
    arg_details = []

    # Helper function to get the string representation of the annotation type
    def _get_annotation_type_string(annotation_node) -> str | None:
        if annotation_node is None:
            return None
        try:
            # Prefer unparse to keep semantic meaning like 'list[int]'
            annotation_str = ast.unparse(annotation_node).strip()
            if not annotation_str:
                return None

            # Validate with eval to check if it's a valid type, but return the readable string
            evaluation_scope = {
                'str': str, 'int': int, 'bool': bool, 'list': list, 'dict': dict,
                'float': float, 'object': object, 'None': type(None),
                'typing': typing, 'Union': typing.Union
            }
            eval(annotation_str, evaluation_scope)
            return annotation_str
        except Exception:
            try:
                return ast.unparse(annotation_node)
            except Exception:
                return None

    # Process positional-only arguments (before '/')
    for arg_node in arguments.posonlyargs:
        has_annot = arg_node.annotation is not None
        arg_details.append({
            'key': arg_node.arg,
            'type': _get_annotation_type_string(arg_node.annotation),
            'value': None,
            'hasDatatype': has_annot,
            'hasDefault': False,
            'isKwarg': False,
            'isPosonlyarg': True,
            'isVararg': False,
            'isKwonlyarg': False,
            'isNormal': False
        })

    # Process regular arguments
    num_defaults = len(arguments.defaults)
    # Args without defaults
    for arg_node in arguments.args[:-num_defaults] if num_defaults > 0 else arguments.args:
        has_annot = arg_node.annotation is not None
        arg_details.append({
            'key': arg_node.arg,
            'type': _get_annotation_type_string(arg_node.annotation),
            'value': None,
            'hasDatatype': has_annot,
            'hasDefault': False,
            'isKwarg': False,
            'isPosonlyarg': False,
            'isVararg': False,
            'isKwonlyarg': False,
            'isNormal': True
        })

    # Args with defaults
    if num_defaults > 0:
        for i, arg_node in enumerate(arguments.args[-num_defaults:]):
            default_node = arguments.defaults[i]
            has_annot = arg_node.annotation is not None
            try:
                default_value = ast.literal_eval(default_node) if isinstance(default_node, ast.Constant) else ast.unparse(default_node)
            except Exception:
                default_value = ast.unparse(default_node)

            arg_details.append({
                'key': arg_node.arg,
                'type': _get_annotation_type_string(arg_node.annotation),
                'value': default_value,
                'hasDatatype': has_annot,
                'hasDefault': True,
                'isKwarg': False,
                'isPosonlyarg': False,
                'isVararg': False,
                'isKwonlyarg': False,
                'isNormal': True
            })

    # *args
    if arguments.vararg:
        arg_node = arguments.vararg
        arg_details.append({
            'key': arg_node.arg,
            'type': _get_annotation_type_string(arg_node.annotation),
            'value': None,
            'hasDatatype': arg_node.annotation is not None,
            'hasDefault': False,
            'isKwarg': False,
            'isPosonlyarg': False,
            'isVararg': True,
            'isKwonlyarg': False,
            'isNormal': False
        })

    # Keyword-only arguments (after *)
    for i, arg_node in enumerate(arguments.kwonlyargs):
        default_node = arguments.kw_defaults[i]
        has_annot = arg_node.annotation is not None
        has_default = default_node is not None
        
        default_value = None
        if has_default:
            try:
                default_value = ast.literal_eval(default_node) if isinstance(default_node, ast.Constant) else ast.unparse(default_node)
            except Exception:
                default_value = ast.unparse(default_node)

        arg_details.append({
            'key': arg_node.arg,
            'type': _get_annotation_type_string(arg_node.annotation),
            'value': default_value,
            'hasDatatype': has_annot,
            'hasDefault': has_default,
            'isKwarg': False,
            'isPosonlyarg': False,
            'isVararg': False,
            'isKwonlyarg': True,
            'isNormal': False
        })

    # **kwargs
    if arguments.kwarg:
        arg_node = arguments.kwarg
        arg_details.append({
            'key': arg_node.arg,
            'type': _get_annotation_type_string(arg_node.annotation),
            'value': None,
            'hasDatatype': arg_node.annotation is not None,
            'hasDefault': False,
            'isKwarg': True,
            'isPosonlyarg': False,
            'isVararg': False,
            'isKwonlyarg': False,
            'isNormal': False
        })

    return arg_details
