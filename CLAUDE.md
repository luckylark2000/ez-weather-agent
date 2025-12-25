# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ez-weather-agent** is a Python project that builds a weather AI agent using LangGraph. The project integrates with OpenWeather API and implements an MCP (Model Context Protocol) server for weather-related operations.

## Technology Stack

- **Python**: 3.11+ (specified in `.python-version`)
- **Package Manager**: UV (with Tsinghua PyPI mirror)
- **Key Dependencies**:
  - `langgraph>=1.0.5`: For building the AI agent graph
  - `python-dotenv>=1.2.1`: For environment variable management
- **Configuration**: Uses `.env` for API keys (specifically `OPEN_WEATHER_API_KEY`)

## Architecture

The project is structured as follows:

- **main.py**: Entry point that loads environment variables and demonstrates basic functionality
- **weather_agent.py**: Placeholder for weather agent implementation (comments in Chinese: "天气 agent")
- **mcp_weather_server.py**: Placeholder for MCP server implementation (comments in Chinese: "天气MCP server")
- **config.py**: Placeholder for configuration loading (comments in Chinese: "一些配置加载")

Currently, most implementation files contain only placeholder comments in Chinese. The architecture is designed to have:

1. An AI agent that handles weather queries (weather_agent.py)
2. An MCP server that exposes weather capabilities (mcp_weather_server.py)
3. Configuration management (config.py)
4. A main entry point that orchestrates everything (main.py)

## Common Development Commands

### Running the Application

```bash
python main.py
```

Requires `OPEN_WEATHER_API_KEY` environment variable to be set.

### Managing Dependencies

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package_name>

# Update dependencies
uv update
```

### Setting Up Development Environment

```bash
# Create/activate virtual environment (handled by uv)
uv venv

# Install project with development setup
uv sync
```

## Environment Setup

Create a `.env` file in the project root with:

```
OPEN_WEATHER_API_KEY=<your_api_key_here>
```

The `.env` file is excluded from version control and must be created locally.

## Project Status

This is an early-stage project with placeholder implementations. Focus areas for future development:

- Implement the weather agent logic in `weather_agent.py` using LangGraph
- Implement the MCP server in `mcp_weather_server.py`
- Complete configuration management in `config.py`
