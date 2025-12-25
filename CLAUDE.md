# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ez-weather-agent** is a Python project that builds an intelligent weather agent using LangGraph and DeepSeek AI. It integrates with the **Caiyun Weather API** to provide real-time weather data, forecasts, and air quality information. The project also implements an MCP (Model Context Protocol) server for exposing weather capabilities.

## Technology Stack

- **Python**: 3.11+ (specified in `.python-version`)
- **Package Manager**: UV (with Tsinghua PyPI mirror)
- **Key Dependencies**:
  - `langgraph>=1.0.5`: For building the AI agent graph with stateful nodes and conditional routing
  - `openai>=1.3.0`: DeepSeek API client (used via OpenAI SDK)
  - `httpx>=0.28.1`: Async HTTP client for Caiyun Weather API calls
  - `mcp[cli]>=1.5.0`: Model Context Protocol server implementation
  - `pydantic>=2.10.6`: Data validation
  - `python-dotenv>=1.2.1`: Environment variable management

## Architecture

### High-Level Design

The project follows a **ReAct pattern** (Reasoning + Acting) with LangGraph:

1. **LangGraph Agent Graph**: StatefulGraph with two main nodes:
   - `chatbot` node: Calls DeepSeek API with tool schemas, receives decisions on which tools to invoke
   - `tools` node: Executes weather tools based on agent decisions
   - Conditional routing: `should_continue()` determines whether to invoke tools or end

2. **Weather Tools**: Three callable tools exposed to the LLM:
   - `get_realtime_weather(location)`: Current weather, humidity, wind, air quality, life indices
   - `get_hourly_forecast(location, hours)`: 72-hour forecast with hourly granularity
   - `get_daily_forecast(location, days)`: 7-day daily forecast with min/max temps

3. **Caiyun Weather API Integration**:
   - Location lookup via hardcoded city coordinates (extensible via `CITY_COORDINATES` dict)
   - Async HTTP requests to Caiyun API endpoints (`/realtime`, `/hourly`, `/daily`)
   - Coordinates: `(longitude, latitude)` tuples for ~15 cities (Beijing, Shanghai, London, Tokyo, etc.)

### Key Files

- **weather_agent.py**: Core LangGraph agent implementation. Manages message routing, tool execution, and state transitions. Houses the three weather tools with hardcoded city coordinates.
- **mcp_caiyun_weather_server.py**: FastMCP server wrapping the same three weather tools with field-based parameter definitions. Exposes weather capabilities via MCP protocol.
- **main.py**: Interactive CLI entry point. Accepts user weather queries in a loop, calls `run_weather_agent()`, displays responses.
- **config.py**: Environment variable loaders for `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, and `DEEPSEEK_MODEL`.
- **test_caiyun.py**: Test script demonstrating agent functionality with sample queries.

## Environment Setup

Create a `.env` file in the project root with:

```txt
DEEPSEEK_API_KEY=<your_deepseek_api_key>
CAIYUN_WEATHER_API_TOKEN=<your_caiyun_api_token>
```

Optional variables:

```txt
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

Get API keys from:

- **DeepSeek**: <https://api-docs.deepseek.com> (register and create API key)
- **Caiyun Weather**: <https://www.caiyunapp.com/> (register, go to developer/API section, create app)

The `.env` file is excluded from version control and must be created locally.

## Common Development Commands

### Running the Application

```bash
# Interactive weather query CLI
python main.py
```

### Testing

```bash
# Test the weather agent with sample queries
python test_caiyun.py
```

### Running the MCP Server

```bash
# Start the MCP server (requires mcp[cli] package)
mcp-run mcp_caiyun_weather_server.py
```

### Managing Dependencies

```bash
# Install/sync dependencies
uv sync

# Add a new dependency
uv add <package_name>

# Update dependencies
uv update
```

## Implementation Notes

### Agent Message Flow

1. User query → `HumanMessage` added to state
2. `chatbot_node` calls DeepSeek with message history + tool schemas
3. DeepSeek returns either:
   - `AIMessage` with `tool_calls` (structured tool invocations)
   - `AIMessage` with plain text response (no tools needed)
4. `should_continue()` checks for tool_calls; if present, routes to `tools` node
5. `tool_node` executes tools, creates `ToolMessage` responses
6. Loop back to `chatbot` node with tool results
7. Eventually returns final `AIMessage` without tool_calls → END

### Tool Execution

Tools are LangChain `@tool` decorated functions. They:

- Run synchronously but make async HTTP calls to Caiyun API using `asyncio.new_event_loop()`
- Require location to be in `CITY_COORDINATES` dict (case-insensitive lookup)
- Return formatted strings for display/context
- Handle errors gracefully with descriptive error messages

### City Coordinates

Located in `weather_agent.py` as `CITY_COORDINATES` dict. To add support for new cities:

1. Add entry: `"city_name": (longitude, latitude)`
2. Find coordinates via Google Maps or equivalent
3. Both nodes (agent, MCP server) use the same dict for consistency

### MCP Server

`mcp_caiyun_weather_server.py` uses **FastMCP** for simplified tool definition. Tools are async and exposed via MCP protocol. Run independently or integrate with Claude via MCP configuration.

## Common Development Tasks

### Adding a New Weather Tool

1. Define the tool function with `@tool` decorator in `weather_agent.py`
2. Create corresponding schema entry in `tools_schema` list in `chatbot_node()`
3. Add execution branch in `tool_node()`
4. Optionally add corresponding `@mcp.tool()` in `mcp_caiyun_weather_server.py`

### Adding Support for New Cities

Edit `CITY_COORDINATES` in `weather_agent.py`:

```python
CITY_COORDINATES = {
    ...existing entries...
    "new_city": (longitude, latitude),
}
```

Coordinates must be `(longitude, latitude)` tuples. No other changes needed; agent uses dict lookups.

### Debugging Agent Behavior

- Add print statements or logging in `chatbot_node()` to inspect message conversions
- Check `state["messages"]` contents at each step
- Verify tool schemas match expected parameter types
- Test individual tools directly: `get_realtime_weather.invoke({"location": "Beijing"})`
