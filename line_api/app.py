from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
import json

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
#Channel access token
line_bot_api = LineBotApi('NryT16dSDuNQSX7dJSNzWT6fRuZUvy1aOc34/Mk7gJi4DFvJQImKK9JKI9Vr48GdK0cznpqZJc3RRI4cNnN+ZrCFM8jy7kDVXQiXmm7cmhALTvqKoj9q2R+OX0WJNWP1rB+Qz7az3WdChEFuEa7fmgdB04t89/1O/w1cDnyilFU=')
#Channel secret
handler = WebhookHandler('c9d51920ef1d54e38f5abbbf7476b4c2')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    d = json.loads(body)
    reid=d["events"][0]["message"]["id"]
    print(reid)

    User_id=d["events"][0]["source"]["userId"]
    print("UserID")
    print(User_id)

    
    rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
        # action=URIAction(label='Go to line.me', uri='https://line.me')
        action={  "type":"message",
                    "label":"還沒有功能",
                    "text":"還沒有功能‵‵‵‵`"
                    }

        )]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

    with open("richmenu.png", 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
    line_bot_api.link_rich_menu_to_user(User_id, rich_menu_id)




    

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        # buttons_template = TemplateSendMessage(
    #         alt_text='開始玩 template',
    #         template=ButtonsTemplate(
    #             title='選擇服務',
    #             text='請選擇',
    #             thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
    #             actions=[
    #                 MessageTemplateAction(
    #                     label='新聞',
    #                     text='新聞'
    #                 ),
    #                 MessageTemplateAction(
    #                     label='電影',
    #                     text='電影'
    #                 ),
    #                 MessageTemplateAction(
    #                     label='看廢文',
    #                     text='看廢文'
    #                 ),
    #                 MessageTemplateAction(
    #                     label='正妹',
    #                     text='正妹'
    #                 )
    #             ]
    #         )
    #     )
    # line_bot_api.reply_message(event.reply_token, buttons_template)



    #line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://news.cts.com.tw/photo/cts/201902/201902131951645_l.jpg', preview_image_url='https://news.cts.com.tw/photo/cts/201902/201902131951645_l.jpg'))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()