import os
from dotenv import load_dotenv

load_dotenv()
def main():
    print("Hello from ez-weather-agent!")
    print(os.environ["OPEN_WEATHER_API_KEY"])


if __name__ == "__main__":
    main()
