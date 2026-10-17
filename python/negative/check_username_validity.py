def check_username_validity(username)->bool:
    # even if it works, the rules are not always accurate, so this function can only be used in very limited use cases. reqrite in a more global process of validation
    if not username:
        return False    
    elif username:
        if username.__class__ != str or bytes:
            return False
    else:  
        if len(username) == 0:
            return False
        else:
            found = 0
            if username.__class__ == bytes: # if is bytes try to decode, unless you get any error, then return false
                try:
                    username = username.decode('utf-8')
                except Exception as e:
#                    print(str(e))
                    return False
            for i in [',',':','@','#','ö','ä','ü','*',' ','\n','\t','"',';',"'",'´','`','}','{','[',']','(',')','/','\\','%','$','§','!','²','³','^','°','>','<','|','µ','€']:
                if username.lower().count(i) > 0:
                    found += 1 # should stop iteration on first finding
            if found:
                return False
            else:
                return True    
def strip_invalid_parentheses(username):
    if username.__class__ == bytes:
        try:
            username  = username.decode('utf-8')
        except Exception as e:
            return '' 
    if username.__class__ not in [str, bytes]:
        return '' 
    task1 = username.strip().strip('"').strip("'").strip('´').strip('`')
    task2 = task1.strip().strip('"').strip("'").strip('´').strip('`')
    task3 = task2.strip().strip('"').strip("'").strip('´').strip('`')
    task4 = task3.strip().strip('"').strip("'").strip('´').strip('`')
    return task4.lower()

class username: 
    def __init__(s,name:str):
        s.origin : str = name if name else None
        s.value : str = strip_invalid_parentheses(name) if name.__class__ in [str,bytes] else None
        s.valid : bool = check_username_validity(s.value)
        s.length : int =  strip_invalid_parentheses(s.value) if s.value and s.valid else None
        s.type : str = 'username' # should use an import of the type (Name or Person or Entity ??)
        s.category : str = 'name'
        s.cls : type = str
        prefix : str = s.value[0] + '_' + s.value[-1] + '_' + s.length if s.length and s.length >= 1 and s.length > 1 else None  
        s.prefix :str = prefix if prefix and len([i.strip() for i in prefix.split('_') if i]) == 3 else None
        s.index : int = get_index(self)
        s.id :str = s.index +'_'+s.prefix if s.index and s.prefix else None        
        
        def get_index(self):
            database = '/data/usernames.db'
            # check if dir an db exists else create (index,prefix,value)
            # find if prefix exists for username if username valid 
            # if exists in database return index, else write object in database with new index and return index
            # 
        def get_by_id(s):
            counter = s.id.count('_')
            split = s.id.split('_')
            if counter == 3 and len([i.strip() for i in s.id.split('_') if i]) in  [3,4]:
                first_char = 
            
    def __repr__(s):
        # or better just the id???
        return {'id':s.id,'value':s.value,'type':s.type}
       