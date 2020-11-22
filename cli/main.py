import hug
import requests
import yaml
import sys
import os

def loadConfig():
    with open((os.getenv("HOME") + "/.config/hausschrat.yml"), 'r') as stream:
        try:
            CONFIG = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    return CONFIG


if __name__ == "__main__":
    CONFIG = loadConfig()
    response = requests.post('http://localhost:8080/sign', json={'expired': CONFIG["defaults"]["expire"], 'username': CONFIG["defaults"]["user"], 'key': CONFIG["defaults"]["key"], 'api_token': CONFIG["defaults"]["api_token"]})
    print(response)
    print(response.json())

