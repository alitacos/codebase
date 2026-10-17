import ast
def preprocess_AstList_to_dict_meta(obj:ast.List)->dict:
    if isinstance(obj, ast.List):
        elts =  obj.elts
        isElts= True if elts and len(elts) > 1 else False
        isElt= True if elts and len(elts) == 1 else False
        if isElts:
            valuetypes = [f'{get_datatype_full_name(i)}' for i in values]
        else:
            valuetypes = f'{get_datatype_full_name(values)}'



        item = {'ast.List':{'keyTypes':[],'eltsNodes':elts if elts else [],'eltsTypes':[], 'hasElts':bool 'hasElt':bool,'keyNodes':[], 'valueTypes':[],  'hasKeys':False,'hasKey':False,'hasValues':  False, 'hasValue':False}}
    else:
        item = {}