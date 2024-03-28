# pyson
_json和python的混合数据格式，动态加载，灵活定义_

## 数据结构
.pyson文件包括两个部分，分别为 json part 和 function part。
文件以一个json对象开始，此部分称为json part。
之后可能存在一行，内容为'# function'，此行后的内容称为function part。
function part内容为合法的py文件内容，通常为一个或多个python函数的定义。

## 特点
### 1. 动态加载特性

在json part中，可以使用'function 函数名'的字符串作为值，pyson加载器会将'function 函数名'处的对象替换为相应函数返回的对象。

利用这一点，可以将某些高度压缩的原始数据（例如二维数组）放在.pyson文件中，并用函数以特定规则将其填充到json对象中。
这有助于使数据文件更简洁，格式转换更可靠，数据与程序更解耦。

### 2. 允许注释json
文件的任何部分都允许行内注释，包括json part！你可以在使用了function关键字的地方写上注释，提高可读性。

### 3. 返回对象
pyson加载器最终返回一个python对象，就像`json.loads()`所做的那样，保持操作json时的代码一致性。

## 开始使用
导入loadpyson即可
```python
import json
form pyson import loadpyson
pyson_content = loadpyson('example.pyson')
print(json.dumps(pyson_content, indent=4, ensure_ascii=False))
```

## 快速上手自制pyson数据文件
参照`example.pyson`:
```python
{
    "info": [
        {"name": "John", "age": 30},
        {"name": "Jane", "age": 25}
    ],
    "node": "function gen_node", # 允许在json部分使用注释
    "edge": "function gen_edge" # 在json中使用function xxx来调用函数
}

# function

# 可以定义公共数据
data = {
    'mq': [0,30,20],
    'length': [100,200,300]
    }

def gen_node(data=data): # 利用默认参数使用公共数据
    mq_list = data['mq']
    obj = []
    for i,mq in enumerate(mq_list):
        obj.append({'nid': i, 'mq': mq})
    return obj

def gen_edge(data=data):
    length_list = data['length']
    obj = []
    for i,length in enumerate(length_list):
        obj.append({'pid': i, 'length': length})
    return obj
```

# 注意
loadpyson会加载文件中的python程序，这可能会导致安全风险。请确保文件来源可靠，或者在加载前检查文件内容。
