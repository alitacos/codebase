def extract_dict_from_Subscript(node:ast.Subscript )  ->dict:
    if node == None or not isinstance(node,(ast.Subscript)) :#,ast.Name ,ast.BinOp,ast.Call,ast.Name,ast.Attribute,ast.Dict,ast.List,ast.Set) ):
        return None
