#!/usr/bin/env python3
"""Test script for Caiyun Weather API integration."""

import os
import sys

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

from weather_agent import run_weather_agent

def test_caiyun_integration():
    """Test the weather agent with Caiyun Weather API."""

    # Check if API token is set
    api_token = os.getenv("CAIYUN_WEATHER_API_TOKEN")
    if not api_token:
        print("[WARNING] CAIYUN_WEATHER_API_TOKEN is not set in .env")
        print("Please add it to use the real weather API:")
        print("  CAIYUN_WEATHER_API_TOKEN=your_token_here")
        print("\nYou can get a free token from: https://www.caiyunapp.com/")
        return False

    print("=" * 60)
    print("Testing Caiyun Weather API Integration")
    print("=" * 60)

    test_queries = [
        "What's the weather in Beijing today?",
        "Get the hourly forecast for Shanghai",
        "Show me the 7-day forecast for Suzhou",
        "How's the weather in London?",
    ]

    for query in test_queries:
        print(f"\n[Query] {query}")
        print("-" * 60)
        try:
            response = run_weather_agent(query)
            print(f"[SUCCESS] Response:\n{response}")
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_caiyun_integration()
    exit(0 if success else 1)
