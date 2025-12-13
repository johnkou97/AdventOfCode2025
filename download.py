import requests
import json

def DownloadInput(url: str, session_token: str, output_file: str) -> None:
    try:
        cookies = {"session": session_token}
        response = requests.get(url, cookies=cookies)
        
        if response.status_code == 200:
            with open(output_file, "w") as file:
                file.write(response.text)
            print(f"Input saved to {output_file}")
        else:
            print(f"Failed to download input. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import os
    
    SESSION_TOKEN = None    # Pass your session token here
                            # Or save it in a file named config.json

    if os.path.exists("config.json") and SESSION_TOKEN is None:
        with open("config.json") as f:
            config = json.load(f)
            SESSION_TOKEN = config.get("SESSION_TOKEN")

    if not SESSION_TOKEN:
        raise ValueError("SESSION_TOKEN not found in config.json")

    if not os.path.exists("inputs"):
        os.makedirs("inputs")

    for i in range(1, 13):
        if os.path.exists(f"inputs/day{i}.txt"):
            print(f"Input for day {i} already exists. Skipping download.")
            continue
        url = f"https://adventofcode.com/2025/day/{i}/input"
        output = f"inputs/day{i}.txt"
        DownloadInput(url, SESSION_TOKEN, output)