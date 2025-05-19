# 天气 MCP 服务器

## 概述

该项目基于 [MCP Server Guide](https://modelcontextprotocol.io/quickstart/server#windows) ，实现了一个基于 MCP 的天气信息服务器。天气 MCP 服务器提供了一个标准化接口，用于通过简单的 API 获取天气预警和预报信息，并可选择性地通过 Deepseek API 提供人工智能增强的解读。

## 功能特点

- **天气预警**：获取任何美国州的活动天气预警
- **天气预报**：使用坐标获取任何地点的详细天气预报
- **AI 增强**：可选集成 Deepseek API，提供智能化的天气数据解读和关键要点提取
- **MCP 标准**：完全符合 MCP 协议标准，可与任何兼容 MCP 的客户端集成
- **简单易用**：提供命令行客户端，简化与服务器的交互

## 安装指南

### 前置条件

- Python 3.10 或更高版本
- pip 包管理器

### 设置步骤

1. 克隆此仓库：
   ```bash
   git clone <仓库地址>
   ```

2. 设置虚拟环境：
   ```bash
   python -m venv .venv
   # Windows 系统：
   .venv\Scripts\activate
   # Unix/MacOS 系统：
   source .venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   - 将 `.env.example` 复制为 .env（如果尚未存在）
   - 更新 .env 文件中的 API 密钥（特别是如果您想使用 Deepseek API 集成）

## 使用方法

### 运行服务器

您可以直接运行天气服务器：

```bash
python weather_server.py
```

这将使用默认传输方法（stdio）启动 MCP 服务器。

### 使用 MCP 开发工具

对于开发和测试，可以使用 MCP CLI 开发工具：

```bash
mcp dev weather_server.py
```

这将启动带有 MCP Inspector 界面的服务器，允许您交互式测试工具和资源。

### 使用简单客户端

本项目包含一个简单的命令行客户端（simple_client.py），演示了如何与天气 MCP 服务器交互：

```bash
# 获取州级天气预警
python simple_client.py alerts CA

# 获取特定位置的天气预报（纬度，经度）
python simple_client.py forecast 37.7749 -122.4194

# 查看服务器帮助信息
python simple_client.py help

# 列出所有可用工具和资源
python simple_client.py list
```

## 服务器组件

### 核心组件

- **weather_server.py**：主服务器实现，包含 MCP 工具定义
- **config.py**：配置设置和环境变量加载
- **simple_client.py**：用于与服务器交互的命令行客户端
- **deepseek_client.py**：Deepseek AI API 客户端，用于增强天气数据解读

### 工具函数

- **weather_api.py**：美国国家气象服务（NWS）API 的客户端
- **formatters.py**：将天气数据格式化为人类可读文本的函数

## API 工具

### 获取天气预警

```python
get_alerts(state: str) -> str
```

获取指定美国州的活动天气预警。

**参数**：
- `state`：两字母美国州代码（例如 CA 表示加利福尼亚州，NY 表示纽约州）

**返回**：
- 格式化的天气预警信息，如果启用了 Deepseek 集成，则包括 AI 增强的解读

### 获取天气预报

```python
get_forecast(latitude: float, longitude: float) -> str
```

获取指定位置的天气预报。

**参数**：
- `latitude`：位置的纬度
- `longitude`：位置的经度

**返回**：
- 格式化的天气预报信息，如果启用了 Deepseek 集成，则包括 AI 增强的解读

## 资源

### 帮助信息

```
URI: weather://help
```

提供关于如何使用天气服务器的帮助信息。

## 配置选项

天气 MCP 服务器可以通过 .env 文件和 config.py 进行配置：

| 配置项 | 描述 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | Deepseek API 密钥 | 无 |
| `NWS_API_KEY` | 美国国家气象服务 API 密钥（目前不需要） | 无 |
| `USER_AGENT` | 用于 API 请求的用户代理字符串 | `weather-mcp-server/1.0` |
| `REQUEST_TIMEOUT` | API 请求超时时间（秒） | 30.0 |
| `MAX_RETRIES` | 请求失败后的最大重试次数 | 3 |
| `DEEPSEEK_MODEL` | 使用的 Deepseek 模型 | `deepseek-chat` |
| `SERVER_NAME` | MCP 服务器名称 | `weather` |
| `DEFAULT_TRANSPORT` | 默认传输协议 | `stdio` |
| `ENABLE_CACHE` | 是否启用缓存 | `True` |
| `CACHE_TTL` | 缓存数据的生存时间（秒） | 300 |

## MCP 客户端使用示例

以下是使用简单客户端与天气 MCP 服务器交互的示例：

### 获取加利福尼亚州的天气预警

```bash
python simple_client.py alerts CA
```

输出结果：
```
Connecting to weather server...
Creating client session...
Initializing session...
Getting available tools...
Connected to server with 2 available tools

Getting weather alerts for CA...

Here's a concise summary of the key weather alerts affecting California and their significance:

**1. Wind Advisories (Multiple Locations)**
- *Areas*: Antelope Valley, Santa Barbara/Ventura County mountains, I-5 corridor
- *Hazards*: Gusts 50-55 mph (strongest in foothills)
- *Timing*: Through Monday morning (varies by location)
- *Key Impacts*:
  - Difficult driving (especially for trucks/RVs)
  - Possible power outages, downed tree limbs
  - Blowing dust reducing visibility (Antelope Valley)

**2. Air Quality Alert (Coachella Valley)**
- *Cause*: Windblown dust creating particle pollution
- *Timing*: Sunday PM - Monday PM
- *Health Risks*: Aggravates respiratory/heart conditions
- *Advice*: Sensitive groups should limit outdoor activity

**3. Red Flag Warning (Sacramento/San Joaquin Valleys)**
- *Conditions*: 15-25% humidity + 35 mph gusts
- *Fire Risk*: Extreme fire spread potential
- *Critical Areas*: Along I-5 corridor
- *Duration*: Through Monday evening

**Key Takeaways:**
- Northern/central CA faces high fire danger due to dry winds
- Southern CA contends with hazardous driving conditions and poor air quality
- All regions should secure outdoor objects and monitor updates
- Fire bans are effectively in place for northern areas

The combination of these alerts indicates an unusually active wind event affecting nearly the entire state with multiple simultaneous hazards.
```

### 获取旧金山的天气预报

```bash
python simple_client.py forecast 37.7749 -122.4194
```

输出结果：
```
Connecting to weather server...
Creating client session...
Initializing session...
Getting available tools...
Connected to server with 2 available tools

Getting weather forecast for coordinates (37.7749, -122.4194)...

### Key Takeaways:
1. **Cool & Windy Conditions**: Expect cool nights (low 50s°F) and mild daytime highs (upper 60s/low 70s°F), with persistent west/northwest 
winds. Gusts up to **30 mph** (Monday night) could make it feel cooler and pose minor challenges for outdoor activities.

2. **Dry and Clear Skies**: No precipitation expected—ideal for outdoor plans, but pack layers for the significant **day-night temperature swings** (~20°F difference).

3. **Wind Advisory**: Strongest winds occur **Monday afternoon/night** (gusts 29–30 mph). Secure loose outdoor items and be cautious driving high-profile vehicles.

4. **Gradual Cooling Trend**: Temperatures dip slightly from Monday (72°F) to Tuesday (68°F), with winds easing by Tuesday night.

**Notable Pattern**: A dry, windy northwest flow dominates, typical of high-pressure systems clearing out humidity. Great for stargazing but may exacerbate fire risk in arid areas.

*Practical Tip*: Wear wind-resistant layers, especially in the evenings, and enjoy the sunny days!
```

### 查看帮助信息

```bash
python simple_client.py help
```

### 列出可用工具和资源

```bash
python simple_client.py list
```

### 扩展指南

想要扩展项目功能，您可以：

1. 添加新的天气数据源（修改 weather_api.py）
2. 增加新的工具函数（在 weather_server.py 中添加新的 `@mcp.tool()` 装饰函数）
3. 改进 AI 增强功能（修改 deepseek_client.py）
4. 添加更多资源（使用 `@mcp.resource()` 装饰器）

## 实现过程中遇到的问题

实现 server_demo 中遇到的问题参见同目录下的 [TrobleShooting](TROBLESHOOTING.md) 文档。

## 注意事项

- 本项目使用美国国家气象服务 API，主要提供美国地区的天气数据
- Deepseek 集成需要有效的 API 密钥，否则将退回到基本的天气数据格式化
- 坐标必须是有效的经纬度值（纬度范围 -90 到 90，经度范围 -180 到 180）

## 许可证

本项目使用 MIT 许可证。有关详细信息，请参阅 LICENSE 文件。

