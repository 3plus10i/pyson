# pyson，json和python的混合数据格式

# loadpyson会加载文件中的python程序，这可能会导致安全风险。
# 请确保文件来源可靠，或者在加载前检查文件内容。
# 
# yjy @ 2024年3月28日

import json

def load_pyson(file):
    """
    Load a pyson file and return a python object.

    :param file: The path to the pyson file.
    :return: A python object represented by the pyson file.
    """
    # 载入pyson文件内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.strip()
    
    # 分割并加载json part和code part
    break_index = __find_json_end(content)
    if break_index == -1:
        raise ValueError("Invalid pyson file: JSON part not found")
    # 解析json对象
    json_obj = json.loads(content[:break_index + 1])
    # 解析python代码并执行
    vars = {}
    exec(content[break_index+1:], vars)
    # 替换json中的函数为函数的返回值
    return __replace_function(json_obj, vars)


# 将pyson文件解析为json字符串，并保存到同名文件中
def export_pyson(file):
    """
    Convert a pyson file to a json file.

    :param file: The path to the pyson file.
    """
    obj = load_pyson(file)
    file = file.split('.')
    file = '.'.join(file[:-1]) + '.json'
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, indent=2, ensure_ascii=False))
    return file


# 替换pyson中的函数为函数的返回值
def __replace_function(obj, vars):
    """
    Replace functions in the given object with their return values.
    
    :param obj: The object to be processed.
    :param vars: The dictionary containing the functions.
    :return: The object with functions replaced.
    """
    if isinstance(obj, str) and __parse_placeholder(obj) is not None:
        # 获取函数名，调用并替换
        func_name = __parse_placeholder(obj)
        if func_name in vars:
            return vars[func_name]()
        else:
            raise ValueError(f"No such function: {func_name}")
    elif isinstance(obj, list):
        return [__replace_function(item, vars) for item in obj]
    elif isinstance(obj, dict):
        return {k: __replace_function(v, vars) for k, v in obj.items()}
    else:
        return obj

# 找到json部分的结束位置
def __find_json_end(string):
    """
    Find the end index of a JSON structure in the given string,
    starting from the beginning of the string.

    :param string: The input string.
    :return: The end index of the JSON structure, or -1 if not found.
    """
    
    # 获取目标字符：合法的json开始于{或[，结束于}或]
    target_left = string[0]
    if target_left == '{':
        target_right = '}'
    elif target_left == '[':
        target_right = ']'
    else:
        return -1
    # 处理转义字符
    in_string = False
    escape = False
    # 用栈来记录嵌套层次
    stack = []
    for i in range(len(string)):
        char = string[i]

        if char == '"' and not escape:
            in_string = not in_string
        elif char == "\\" and in_string and not escape:
            escape = True
        else:
            escape = False
            
        if not in_string:
            if char == target_left:
                stack.append('1')
            elif char == target_right:
                stack.pop()
                if len(stack) == 0:
                    return i
    return -1

def __parse_placeholder(string):
    """
    Check if a string is a placeholder.

    :param string: The input string.
    :return: Content if the string is a placeholder, None otherwise.
    """
    if string.startswith("{%"):
        if string.endswith("%}"):
            return string[2:-2].strip()
    else:
        return None


__all__ = ['load_pyson', 'export_pyson']