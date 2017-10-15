import time
import json 
import requests
import pymysql


# def set_reminder():
TOKEN="472863831:AAEvuDp5Zsch7SdQpkOC--uxu_WeNcX9Vo8"
URL="https://api.telegram.org/bot{}/".format(TOKEN)


def call_reminder():
    while True:
        tt=time.localtime(time.time())
        if tt.tm_hour==9:
            try:
                db=pymysql.connect("localhost","root","123456789","MediBOT")
                cursor=db.cursor()
                cursor.execute("select chat_id,medicine from reminder where M=true")
                result=cursor.fetchall()
                cursor.execute("update reminder set days=days-1 where M=true and L=false and N=false")
                cursor.execute(" delete from reminder where days=0")
                for row in result:
                    url = URL + "sendMessage?text={}&chat_id={}".format("Please take your Medicine !! Medicine name : " + row[1] , row[0])
                    response=requests.get(url)
                    content=response.content.decode("utf8")
                db.commit()
                db.close()
            except:
                db.rollback()
                db.close()
        elif tt.tm_hour==13:
                try:
                    db=pymysql.connect("localhost","root","123456789","MediBOT")
                    cursor=db.cursor()
                    cursor.execute("select chat_id,medicine from reminder where L=true")
                    result=cursor.fetchall()
                    cursor.execute("update reminder set days=days-1 where  L=true and N=false")
                    for row in result:
                        url = URL + "sendMessage?text={}&chat_id={}".format("Please take your Medicine !! Medicine name : " + row[1] , row[0])
                        response=requests.get(url)
                        content=response.content.decode("utf8")
                        cursor.execute(" delete from reminder where days=0")
                    db.commit()
                    db.close()
                except:
                    db.rollback()
                    db.close()
        elif tt.tm_hour==21:
                try:
                db=pymysql.connect("localhost","root","123456789","MediBOT")
                cursor=db.cursor()
                cursor.execute("select chat_id,medicine from reminder where N=true")
                result=cursor.fetchall()
                cursor.execute("update reminder set days=days-1 where  N=true")
                for row in result:
                    url = URL + "sendMessage?text={}&chat_id={}".format("Please take your Medicine !! Medicine name : " + row[1] , row[0])
                    response=requests.get(url)
                    content=response.content.decode("utf8")
                    cursor.execute(" delete from reminder where days=0")
                db.commit()
                db.close()
            except:
                db.rollback()
                db.close()
