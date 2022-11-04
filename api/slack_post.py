import slack
import os
from dotenv import load_dotenv

class Slack():
    def __init__(self) -> None:
        pass
    
    def post(message):
        load_dotenv()
        try:
            client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))
            client.chat_postMessage(channel=os.getenv('SLACK_CHANNEL'), text=message)
        except:
            print('Cannot send message')
