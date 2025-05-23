import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, Header

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import(
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = FastAPI()

load_dotenv(override=True)

#Line Access Key
get_access_token = os.getenv('ACCESS_TOKEN')
#print(str(get_access_token))
configuration = Configuration(access_token=get_access_token)
#Line Secret Key
get_channel_secret = os.getenv('CHANNEL_SECRET')
handler = WebhookHandler(channel_secret=get_channel_secret)

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature, Please check your channel access token/channel secrets")
        raise HTTPException(status_code=400, detail="Invalid signature")
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_message = "Hello from Automate text environment"
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token = event.reply_token,
                messages=[TextMessage(text = reply_message)]
            )
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")