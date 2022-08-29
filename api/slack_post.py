import slack
import os
from dotenv import load_dotenv
import utils

def postMessage(message):
    load_dotenv()
    client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))
    client.chat_postMessage(channel=os.getenv('SLACK_CHANNEL'), text=message)