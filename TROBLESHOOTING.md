# MCP Simple-Client 开发常见问题及解决方案

在使用 MCP 开发客户端与服务器交互的过程中，我遇到了很多问题。下面的文档内容详细记录了遇到的问题以及我使用的解决方案。

## 问题与解决方案

### 1. MCP 客户端导入错误

**问题描述**：
```
from mcp.client import client as Client
ImportError: cannot import name 'client' from 'mcp.client'
```

**原因**：
MCP 客户端库的导入路径不正确，可能是由于 API 结构的变更导致的。

**解决方法**：
检查 MCP 客户端库的正确导入方式，常见的解决方案包括：

```python
# 正确导入 ClientSession 类
from mcp import ClientSession

# 导入与传输相关的模块
from mcp.client.stdio import stdio_client

# 导入参数类型
from mcp import StdioServerParameters
```

### 2. 异步上下文管理器使用错误

**问题描述**：
```
Error: object _AsyncGeneratorContextManager can't be used in 'await' expression
```

**原因**：
错误地使用 `await` 语句直接等待一个异步上下文管理器，而不是使用 `async with`。

**解决方法**：
使用正确的 `async with` 语法处理异步上下文管理器：

```python
# 错误的用法
stdio_transport = await stdio_client(server_params)

# 正确的用法
async with AsyncExitStack() as exit_stack:
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio_reader, stdio_writer = stdio_transport
```

### 3. StreamWriter 对象错误

**问题描述**：
```
Error: 'StreamWriter' object has no attribute 'send'
```

**原因**：
尝试使用不存在的 `send` 方法与 MCP 服务器通信，而 `StreamWriter` 对象没有该方法。

**解决方法**：
使用 `AsyncExitStack` 正确管理异步资源，并使用与 MCP 客户端库兼容的通信方式：

```python
from contextlib import AsyncExitStack

async def run_client():
    async with AsyncExitStack() as exit_stack:
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        stdio_reader, stdio_writer = stdio_transport
        session = await exit_stack.enter_async_context(ClientSession(stdio_reader, stdio_writer))
        await session.initialize()
```

### 4. TaskGroup 异常处理问题

**问题描述**：
```
Error: unhandled errors in a TaskGroup (1 sub-exception)
```

**原因**：
在异步任务组中发生了未处理的异常，但错误信息不够详细。

**解决方法**：
添加详细的异常捕获和日志记录，以便更好地诊断问题：

```python
try:
    # 可能引发异常的代码
    result = await session.call_tool("get_alerts", {"state": state})
except Exception as e:
    print(f"详细错误信息:")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误消息: {str(e)}")
    print("\n调用栈:")
    traceback.print_exc()
```


### 5. 列表类型内容处理错误

**问题描述**：
```
TypeError: can only concatenate str (not "list") to str
```

**原因**：
尝试将一个列表类型的内容与字符串连接，而 MCP 服务器返回的内容可能是 `TextContent` 对象列表。

**解决方法**：
编写一个通用的格式化函数来处理不同类型的响应内容：

```python
def format_content(content):
    """格式化内容，可以处理 TextContent 对象列表或其他类型。"""
    if isinstance(content, list):
        # 处理 TextContent 对象列表
        try:
            # 合并所有 TextContent 对象的文本
            return ''.join(item.text for item in content)
        except AttributeError:
            # 如果项目没有 text 属性，则作为字符串连接
            return ''.join(str(item) for item in content)
    # 如果不是列表，则直接返回内容
    return content
```

## 开发技巧与最佳实践

### 1. 使用诊断脚本

在遇到 API 不一致或文档不明确的情况下，编写简短的诊断脚本来检查对象结构：

```python
import inspect

# 检查类的方法和属性
for name in dir(some_object):
    if not name.startswith("_"):
        print(f"- {name}")

# 尝试不同的属性名
for attr in ['content', 'contents', 'text', 'data']:
    try:
        value = getattr(result, attr, None)
        if value is not None:
            print(f"{attr} 可用: {type(value)}")
    except Exception as e:
        print(f"{attr} 错误: {e}")
```

### 2. 使用 AsyncExitStack 管理资源

使用 `AsyncExitStack` 正确管理异步资源，确保它们在完成时被正确关闭：

```python
from contextlib import AsyncExitStack

async def run_client():
    async with AsyncExitStack() as exit_stack:
        # 进入异步上下文
        transport = await exit_stack.enter_async_context(some_async_context())
        # 使用资源
        # 退出时自动关闭资源
```

### 3. 打印错误详细信息

添加全面的错误处理，包括异常类型、消息和调用栈：

```python
try:
    # 可能失败的操作
except Exception as e:
    print(f"错误类型: {type(e).__name__}")
    print(f"错误消息: {str(e)}")
    traceback.print_exc()  # 打印完整调用栈
```

### 4. 使用 `async with` 而非直接 `await`

对于返回异步上下文管理器的函数，使用 `async with` 而不是 `await`：

```python
# 错误
result = await async_context_manager()

# 正确
async with async_context_manager() as result:
    # 使用 result
```
