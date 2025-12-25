"""Weather agent powered by DeepSeek and LangGraph with Caiyun Weather API."""
import json
import os
from typing import Annotated, Any

import httpx
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam

from config import (
    get_deepseek_api_key,
    get_deepseek_base_url,
    get_deepseek_model,
)


# Initialize OpenAI client for DeepSeek
client = OpenAI(
    api_key=get_deepseek_api_key(),
    base_url=get_deepseek_base_url(),
)

# Caiyun Weather API token
CAIYUN_API_TOKEN = os.getenv("CAIYUN_WEATHER_API_TOKEN")

# Common city coordinates (longitude, latitude)
CITY_COORDINATES = {
    "beijing": (116.4074, 39.9042),
    "shanghai": (121.4737, 31.2304),
    "guangzhou": (113.2644, 23.1291),
    "shenzhen": (114.0579, 22.5431),
    "chengdu": (104.0659, 30.5728),
    "hangzhou": (120.1551, 30.2875),
    "suzhou": (120.5954, 31.2989),
    "wuhan": (114.3055, 30.5928),
    "xi'an": (108.9398, 34.3416),
    "chongqing": (106.5516, 29.5630),
    "london": (-0.1276, 51.5074),
    "new york": (-74.0060, 40.7128),
    "tokyo": (139.6917, 35.6762),
    "paris": (2.3522, 48.8566),
    "sydney": (151.2093, -33.8688),
}


async def make_caiyun_request(url: str, params: dict) -> dict:
    """Make async request to Caiyun Weather API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


@tool
def get_realtime_weather(location: str) -> str:
    """
    Get the current weather for a location using Caiyun Weather API.

    Args:
        location: City name (e.g., "Beijing", "Shanghai", "London")

    Returns:
        Current weather information as a formatted string
    """
    if not CAIYUN_API_TOKEN:
        return "Error: CAIYUN_WEATHER_API_TOKEN is not set"

    location_lower = location.lower()
    if location_lower not in CITY_COORDINATES:
        available = ", ".join(CITY_COORDINATES.keys())
        return f"Location '{location}' not found. Available locations: {available}"

    lng, lat = CITY_COORDINATES[location_lower]

    try:
        import asyncio

        # Create and run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def fetch():
            return await make_caiyun_request(
                f"https://api.caiyunapp.com/v2.6/{CAIYUN_API_TOKEN}/{lng},{lat}/realtime",
                {"lang": "en_US"},
            )

        result = loop.run_until_complete(fetch())
        loop.close()

        realtime = result["result"]["realtime"]
        return f"""
Weather in {location}:
Temperature: {realtime["temperature"]}°C
Humidity: {realtime["humidity"]}%
Wind: {realtime["wind"]["speed"]} m/s from {realtime["wind"]["direction"]}°
Precipitation: {realtime["precipitation"]["local"]["intensity"]}%
Air Quality:
  PM2.5: {realtime["air_quality"]["pm25"]} μg/m³
  PM10: {realtime["air_quality"]["pm10"]} μg/m³
  AQI (China): {realtime["air_quality"]["aqi"]["chn"]}
Life Index:
  UV: {realtime["life_index"]["ultraviolet"]["desc"]}
  Comfort: {realtime["life_index"]["comfort"]["desc"]}
"""
    except Exception as e:
        return f"Error fetching weather for {location}: {str(e)}"


@tool
def get_hourly_forecast(location: str, hours: int = 24) -> str:
    """
    Get hourly weather forecast for a location.

    Args:
        location: City name
        hours: Number of hours to forecast (max 72)

    Returns:
        Hourly forecast as formatted string
    """
    if not CAIYUN_API_TOKEN:
        return "Error: CAIYUN_WEATHER_API_TOKEN is not set"

    if hours > 72:
        hours = 72
    if hours < 1:
        hours = 24

    location_lower = location.lower()
    if location_lower not in CITY_COORDINATES:
        return f"Location '{location}' not found"

    lng, lat = CITY_COORDINATES[location_lower]

    try:
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def fetch():
            return await make_caiyun_request(
                f"https://api.caiyunapp.com/v2.6/{CAIYUN_API_TOKEN}/{lng},{lat}/hourly",
                {"hourlysteps": str(hours), "lang": "en_US"},
            )

        result = loop.run_until_complete(fetch())
        loop.close()

        hourly = result["result"]["hourly"]
        forecast = f"{hours}-Hour Forecast for {location}:\n"

        for i in range(min(hours, len(hourly["temperature"]))):
            time = hourly["temperature"][i]["datetime"].split("+")[0]
            temp = hourly["temperature"][i]["value"]
            skycon = hourly["skycon"][i]["value"]
            wind_speed = hourly["wind"]["speed"][i]["value"]

            forecast += f"\n{time}: {temp}°C, {skycon}, Wind: {wind_speed}m/s"

        return forecast
    except Exception as e:
        return f"Error fetching hourly forecast for {location}: {str(e)}"


@tool
def get_daily_forecast(location: str, days: int = 7) -> str:
    """
    Get daily weather forecast for a location.

    Args:
        location: City name
        days: Number of days to forecast (max 7)

    Returns:
        Daily forecast as formatted string
    """
    if not CAIYUN_API_TOKEN:
        return "Error: CAIYUN_WEATHER_API_TOKEN is not set"

    if days > 7:
        days = 7
    if days < 1:
        days = 7

    location_lower = location.lower()
    if location_lower not in CITY_COORDINATES:
        return f"Location '{location}' not found"

    lng, lat = CITY_COORDINATES[location_lower]

    try:
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def fetch():
            return await make_caiyun_request(
                f"https://api.caiyunapp.com/v2.6/{CAIYUN_API_TOKEN}/{lng},{lat}/daily",
                {"dailysteps": str(days), "lang": "en_US"},
            )

        result = loop.run_until_complete(fetch())
        loop.close()

        daily = result["result"]["daily"]
        forecast = f"{days}-Day Forecast for {location}:\n"

        for i in range(min(days, len(daily["temperature"]))):
            date = daily["temperature"][i]["date"].split("T")[0]
            temp_max = daily["temperature"][i]["max"]
            temp_min = daily["temperature"][i]["min"]
            skycon = daily["skycon"][i]["value"]
            rain_prob = daily["precipitation"][i]["probability"]

            forecast += f"\n{date}: {temp_min}°C ~ {temp_max}°C, {skycon}, Rain: {rain_prob}%"

        return forecast
    except Exception as e:
        return f"Error fetching daily forecast for {location}: {str(e)}"


# Define agent state
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Create the weather agent
def create_weather_agent():
    """Create and return the weather agent graph."""

    def chatbot_node(state: AgentState) -> dict[str, list[BaseMessage]]:
        """Process messages and call the LLM."""
        # Prepare tools schema for the model
        tools_schema: list[ChatCompletionToolParam] = [
            {
                "type": "function",
                "function": {
                    "name": "get_realtime_weather",
                    "description": "Get the current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name (e.g., Beijing, Shanghai, London)",
                            }
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_hourly_forecast",
                    "description": "Get hourly weather forecast for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name",
                            },
                            "hours": {
                                "type": "integer",
                                "description": "Number of hours (max 72)",
                            },
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_daily_forecast",
                    "description": "Get daily weather forecast for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name",
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days (max 7)",
                            },
                        },
                        "required": ["location"],
                    },
                },
            },
        ]

        # Convert messages to the format expected by the API
        messages_for_api = []
        for msg in state["messages"]:
            if isinstance(msg, HumanMessage):
                messages_for_api.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                # For assistant messages with tool calls, format them for the API
                api_msg = {"role": "assistant", "content": msg.content or ""}

                if msg.tool_calls:
                    # Convert LangChain tool_calls format to OpenAI/DeepSeek format
                    tool_calls = []
                    for tc in msg.tool_calls:
                        tool_calls.append(
                            {
                                "id": tc["id"],
                                "type": "function",
                                "function": {
                                    "name": tc["name"],
                                    "arguments": json.dumps(tc["args"])
                                    if isinstance(tc["args"], dict)
                                    else tc["args"],
                                },
                            }
                        )
                    api_msg["tool_calls"] = tool_calls

                messages_for_api.append(api_msg)
            elif isinstance(msg, ToolMessage):
                messages_for_api.append(
                    {
                        "role": "tool",
                        "content": msg.content,
                        "tool_call_id": msg.tool_call_id,
                    }
                )

        # Call the DeepSeek API
        response = client.chat.completions.create(
            model=get_deepseek_model(),
            messages=messages_for_api,
            tools=tools_schema,
            temperature=0.7,
            max_tokens=1000,
        )

        response_message = response.choices[0].message

        # Convert response to AIMessage
        ai_message = AIMessage(
            content=response_message.content or "",
        )

        # If the model called tools, add tool_calls to the message
        if response_message.tool_calls:
            ai_message.tool_calls = []
            for tc in response_message.tool_calls:
                # Handle both ChatCompletionMessageToolCall and other types
                tool_name = getattr(tc, 'function', None)
                if tool_name:
                    tool_name = getattr(tool_name, 'name', None)

                tool_args = getattr(tc, 'function', None)
                if tool_args:
                    tool_args = getattr(tool_args, 'arguments', None)

                if tool_name and tool_args:
                    ai_message.tool_calls.append({
                        "id": tc.id,
                        "name": tool_name,
                        "args": json.loads(tool_args),
                    })

        return {"messages": [ai_message]}

    def tool_node(state: AgentState) -> dict[str, list[BaseMessage]]:
        """Execute tools called by the model."""
        last_message = state["messages"][-1]

        if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
            return {"messages": []}

        tool_messages = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Execute the tool
            if tool_name == "get_realtime_weather":
                result = get_realtime_weather.invoke(tool_args)
            elif tool_name == "get_hourly_forecast":
                result = get_hourly_forecast.invoke(tool_args)
            elif tool_name == "get_daily_forecast":
                result = get_daily_forecast.invoke(tool_args)
            else:
                result = f"Unknown tool: {tool_name}"

            tool_messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"],
                    name=tool_name,
                )
            )

        return {"messages": tool_messages}

    def should_continue(state: AgentState) -> str:
        """Determine whether to continue to tool execution or end."""
        last_message = state["messages"][-1]

        # If the last message has tool calls, we should execute tools
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"

        # Otherwise, we're done
        return END

    # Build the graph
    graph_builder = StateGraph(AgentState)

    # Add nodes
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_node("tools", tool_node)

    # Add edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        should_continue,
        {
            "tools": "tools",
            END: END,
        },
    )
    graph_builder.add_edge("tools", "chatbot")

    # Compile the graph
    return graph_builder.compile()


def run_weather_agent(query: str) -> str:
    """
    Run the weather agent with a user query.

    Args:
        query: User's weather query

    Returns:
        Agent's response
    """
    agent = create_weather_agent()

    # Prepare initial state with system message
    messages: list[BaseMessage] = [
        HumanMessage(
            content=f"You are a helpful weather assistant. Answer the user's weather queries by using the available tools. User query: {query}"
        )
    ]

    state: AgentState = {"messages": messages}

    # Run the agent
    result = agent.invoke(state)

    # Extract the final response
    last_message = result["messages"][-1]
    response_text: str = ""
    if isinstance(last_message, AIMessage):
        response_text = last_message.content if isinstance(last_message.content, str) else str(last_message.content)
    else:
        response_text = str(last_message)

    return response_text
