import json
import requests
import time
import urllib
import pymysql
TOKEN="325538102:AAGP4e9HWpXYY2LTvWrDjhh8yyGeyIdcWwA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def my_strip(str,pat):
	strn = str.lstrip(pat)
	low = strn.split(",")
	rlow=[]
	for word in low:
		rlow.append(word.lstrip())
	return rlow

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        print(text+"@")
        if text.startswith("/symptoms"):
            db = pymysql.connect("localhost","root","123456789","MediBOT")
            cursor=db.cursor()
            lst = my_strip(text,"/symptoms")
            str = lst[0]
            cursor.execute("select Symptom from Symptoms where Illness='{}'".format(str))
            try:
                result=cursor.fetchall()
            except:
                continue
            for row in result:
                url = URL + "sendMessage?text={}&chat_id={}".format(row[0] , chat)
                response=requests.get(url)
                content=response.content.decode("utf8")
        else:
	        url = URL + "sendMessage?text={}&chat_id={}".format(text,chat)	
		
		
		

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)



last_update_id = None
while True:
    updates = get_updates(last_update_id)
    if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        handle_updates(updates)
    time.sleep(0.5)
