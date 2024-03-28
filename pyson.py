# pyson，json和python的混合数据格式

# pyson文件以一个合法的json对象开始，此部分称为json part。
# 可能存在一行，内容为'# function'，此行后续内容称为function part。
# function part内容为合法的py文件内容，通常为一个或多个python函数的定义。
# 在json part中，可以使用'function 函数名'的字符串作为值，
# pyson加载器会将'function 函数名'处的对象替换为相应函数返回的对象。
# 加载器最终返回一个python对象。
# 
# loadpyson会加载文件中的python程序，这可能会导致安全风险。
# 请确保文件来源可靠，或者在加载前检查文件内容。
# 
# yjy @ 2024年3月28日

import json

def loadpyson(file):
    """
    Load a pyson file and return a python object.

    :param file: The path to the pyson file.
    :return: A python object represented by the pyson file.
    """
    # 载入pyson文件内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 兼容处理纯JSON文件
    if '# function' not in content:
        return json.loads(content)
    
    # 分割并加载json part和function part
    # 只识别第一个"# function"标记
    parts = content.split('\n# function', 1)
    json_part = parts[0].strip()
    function_part = parts[1].strip()
    
    # 解析json对象
    json_part = __strip_comments(json_part) # 允许json中行内注释
    json_obj = json.loads(json_part)
    
    # 解析函数部分
    # 创建一个新的环境来执行函数定义，保护全局环境
    local_vars = {}
    exec(function_part, {}, local_vars)
    # 从执行结果中提取函数
    functions = {k: v for k, v in local_vars.items() if callable(v)}
    
    # 执行替换操作
    return __replace_function(json_obj, functions)

# 替换pyson中的函数为函数的返回值
def __replace_function(obj, functions):
    if isinstance(obj, str) and obj.startswith('function '):
        # 获取函数名，调用并替换
        func_name = obj[len('function '):].strip()
        if func_name in functions:
            return functions[func_name]()
        else:
            raise ValueError(f"No such function: {func_name}")
    elif isinstance(obj, list):
        return [__replace_function(item, functions) for item in obj]
    elif isinstance(obj, dict):
        return {k: __replace_function(v, functions) for k, v in obj.items()}
    else:
        return obj

def __strip_comments(json_text):
    # 移除注释的辅助函数
    lines = json_text.split('\n')
    without_comments = []
    for line in lines:
        # 找到#的位置
        comment_index = line.find('#')
        if comment_index != -1:
            # 如果存在注释，截取#之前的部分
            without_comments.append(line[:comment_index])
        else:
            without_comments.append(line)
    return '\n'.join(without_comments)


if __name__ == '__main__':
    # 示例使用
    pyson_content = loadpyson('example.pyson')
    print(pyson_content)
    # print(json.dumps(pyson_content, indent=4, ensure_ascii=False))