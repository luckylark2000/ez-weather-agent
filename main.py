"""Main entry point for the EZ Weather Agent."""
import sys

from config import get_deepseek_api_key, get_deepseek_model
from weather_agent import run_weather_agent


def main():
    """Main function that runs the weather agent."""
    try:
        # Verify that the API key is configured
        api_key = get_deepseek_api_key()
        model = get_deepseek_model()

        print("=" * 60)
        print("Welcome to EZ Weather Agent!")
        print("=" * 60)
        print(f"Using model: {model}")
        print("Type 'exit' to quit, or enter a weather query.")
        print("=" * 60)
        print()

        # Interactive loop for weather queries
        while True:
            try:
                user_input = input("Weather Query > ").strip()

                if user_input.lower() in ("exit", "quit", "q"):
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                print("\nProcessing your query...\n")
                response = run_weather_agent(user_input)
                print(f"Assistant: {response}\n")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please make sure DEEPSEEK_API_KEY is set in your .env file.")
        sys.exit(1)


if __name__ == "__main__":
    main()
