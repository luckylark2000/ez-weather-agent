# EZ Weather Agent

使用 LangGraph 和 DeepSeek API 构建的智能天气代理

## 项目概述

这是一个基于 LangGraph 框架的天气 AI 代理，集成了 DeepSeek API 来处理自然语言查询并提供天气信息。该项目演示了如何构建一个能够使用工具的 ReAct 代理。

## 主要特性

- **LangGraph 框架**：使用低级编排框架构建有状态的 AI 代理
- **DeepSeek AI 模型**：利用 DeepSeek Chat 模型进行自然语言处理
- **工具集成**：代理可以调用天气查询和预报工具
- **MCP 服务器**：通过 Model Context Protocol 暴露天气功能
- **交互式 CLI**：用户友好的命令行界面

## 项目结构

```
ez-weather-agent/
├── config.py              # 配置管理和环境变量加载
├── weather_agent.py       # 天气代理实现（LangGraph）
├── mcp_weather_server.py  # MCP 服务器实现
├── main.py               # CLI 入口点
├── test_weather_agent.py # 测试脚本
├── pyproject.toml        # 项目配置和依赖
├── .env                  # 环境变量（不包含在版本控制中）
└── README.md            # 本文件
```

## 技术栈

- **Python**: 3.11+
- **LangGraph**: >=1.0.5 - 用于构建 AI 代理
- **DeepSeek API**: 通过 OpenAI SDK 访问
- **LangChain Core**: 核心工具和消息类型
- **python-dotenv**: >=1.2.1 - 环境变量管理

## 安装和设置

### 1. 克隆或初始化项目

```bash
cd ez-weather-agent
```

### 2. 创建 .env 文件

在项目根目录创建 `.env` 文件：

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

使用彩云天气API,context7文档地址：<https://context7.com/websites/caiyunapp_weather-api_v2_v2_6>

可选配置：

```bash
# 可选：自定义 DeepSeek 基础 URL
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 可选：自定义模型名称
DEEPSEEK_MODEL=deepseek-chat
```

获取 DeepSeek API Key：

- 访问 [DeepSeek API 官网](https://api-docs.deepseek.com)
- 注册账户并获取 API 密钥

### 3. 安装依赖

使用 UV 包管理器（推荐）：

```bash
uv sync
```

或使用 pip：

```bash
pip install -e .
```

## 使用方法

### 交互式 CLI

运行主程序进入交互式天气查询界面：

```bash
python main.py
```

示例对话：

```
============================================================
Welcome to EZ Weather Agent!
============================================================
Using model: deepseek-chat
Type 'exit' to quit, or enter a weather query.
============================================================

Weather Query > What's the weather in Beijing?

Processing your query...
