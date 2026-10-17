#missing get_datatype_full_name  
def preprocessAstDict(obj:ast.Dict):
    if isinstance(obj, ast.Dict):
        keys =  obj.keys
        isKeys= True if keys and len(keys) > 1 else False
        isKey= True if keys and len(keys) == 1 else False
        if isKeys:
            keytypes = [f'{get_datatype_full_name(i)}' for i in keys]
        else:
            keytypes = f'{get_datatype_full_name(keys)}'
        values =  obj.values
        isValues= True if values and len(values) > 1 else False
        isValue= True if values and len(values) == 1 else False
        if isValues:
            valuetypes = [f'{get_datatype_full_name(i)}' for i in values]
        if isValue:
            valuetypes = f'{get_datatype_full_name(values)}'
        item = {'eltsNodes':[],
                'eltsTypes':[],
            'keyTypes':keytypes,'keyNodes':keys if keys else keys,'valueNodes':valuetypes,
            'valueTypes':values if values else [],
            'elts':[],
            'hasKeys':isKeys,
            'hasKey':isKey,
            'hasValues':isValues,
            'hasValue':isValue}

    else:
        item = {}
