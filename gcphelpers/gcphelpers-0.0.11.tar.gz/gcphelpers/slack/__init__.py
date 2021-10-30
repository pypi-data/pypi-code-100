from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_slack_simple_message(slack_bot_token, channel, text, emoji=":robot_face:"):
    """
    Sends a simple Slack message.
    :param string slack_bot_token: A Slack bot token (xoxb-*) 
    :param string channel: Either channel name/ID or Slack UID
    :param string text: The message's text
    :param string emoji: Emoji to use as bot icon
    """
    client = WebClient(
        token=slack_bot_token
    )

    try:
        result = client.chat_postMessage(
            channel = f"{channel}",
            text=f"{text}",
            icon_emoji=f"{emoji}",
        )
    except SlackApiError as e:
        print(f"Error posting to Slack: {e}")
