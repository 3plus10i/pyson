# pyson
_json和python的混合数据格式，动态加载，灵活定义_

## 数据结构
.pyson文件包括两个部分，分别为 json part 和 code part。
文件以一个 json 对象开始，此部分称为 json part。
之后的内容称为 code part, 内容通常为一个或多个python函数的定义。

## 特点
### 1. 动态加载数据

在 json part 中，可以使用 "{% myfunc %}" 字符串作为对象，pyson加载器会将该处替换为相应函数返回的对象。

利用这一点，可以将某些高度压缩的原始数据（例如二维数组）放在.pyson文件中，并用函数以任意规则将其填充到json对象中。
这有助于使数据文件更简洁，格式转换更可靠，数据与程序更解耦。


### 2. 返回python对象
pyson加载器最终返回一个python对象，就像`json.loads()`所做的那样，保持操作json时的代码一致性。


### 3. 可转换为普通json
使用 export_pyson() 将 pyson 文件导出为 json 文件, 最大限度的兼容其他代码。


## 开始使用
导入pyson即可
```python
import json
form pyson import *
pyson_content = load_pyson('example.pyson')
print(json.dumps(pyson_content, indent=4, ensure_ascii=False))
```

## 快速上手自制pyson数据文件
参照`example.pyson`:
```python
{
    "info": [
        {"name": "John", "age": 30}
    ],
    "node": "function gen_node",
    "edge": "function gen_edge"
}

import time # 允许使用库
# 可以定义公共数据
data = [
    [0,30,20],
    [100,200,300]
    ]

def gen_node():
    m_list = data[0] # 可以直接使用公共数据
    obj = []
    for i,m in enumerate(m_list):
        obj.append({'id': i, 'm': __foo(m)}) # 允许调用自定义函数
    return obj

def gen_edge():
    length_list = data[1]
    obj = []
    for i,length in enumerate(length_list):
        obj.append({'len': length/100, 'time': time.time()})
    return obj

def __foo(x):
    return x**2
```

# 注意
pyson会加载文件中的python程序，这可能会导致安全风险。请确保文件来源可靠，或者在加载前检查文件内容。
