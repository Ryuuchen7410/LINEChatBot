from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('USz1oBCXyFuSykq8DL1AvGI2VpgxQd3QIbf2BwnklSroVXllPEyzt6R9SI/Gvecgi3VWNjJE9M4MYQwZZ576Y/2yiUftsUefainXWas6xZd8HaX4A8RcgTEYL4LUpaOFYNJZ3Zf5RQJTLxcsXyl64gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('516537511f9b25ba403ee4194fd3646e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

menu = {
    "漢堡蛋":45,
    "總匯三明治":60,
    "火腿起司蛋餅":35
}

shoppingCart = {}

def similar(target, order, threshold=0.6):
    target_set = set(target)
    order_set = set(order)

    intersect = target_set & order_set

    return (len(intersect) / len(target_set)) >= threshold

def compareItem(itemName):
    itemFound = False
    if not similar("多少錢", itemName):
        for item, price in menu.items():
            if similar (item, itemName):
                itemFound = True
                return item, price
        if itemFound == False:
            return "", -1
    else:
        return "", 0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    item, price = compareItem(event.message.text)

    if price > 0:
        shoppingCart[item] = price
        msg = '好的! 一個{}!'.format(item)
    elif price == -1:
        msg = '我們沒有賣{}耶~ 要不要點點別的?'.format(item)
    elif price == 0:
        msg = '您一共點了: \n'
        totalPrice = 0
        for i, p in shoppingCart.items():
            totalPrice += p
            msg += '一個{}，{}元。\n'.format(i, p)
        msg += '這樣一共 {}元～謝謝惠顧!'.format(totalPrice)
        shoppingCart.clear()


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run()