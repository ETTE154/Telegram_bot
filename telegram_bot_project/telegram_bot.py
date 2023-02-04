import telegram
import asyncio
import time
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

tok = "<HTTP API TOKEN>"
bot = telegram.Bot(token= tok)
chat_id = <CHAT ID>
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# 이미지, 텍스트 전송 함수
#-----------------------------------------------------------------------------------
def sendTelegramMessage(message):
    bot.sendMessage(chat_id=chat_id, text=message)

def sendTelegramPhoto(photo):
    bot.sendPhoto(chat_id=chat_id, photo=open(photo, 'rb'))
# 봇을 종료하는 비동기 함수
async def stop_bot():
    sendTelegramMessage("얼굴인식이 종료되었습니다.")
    cv2.destroyAllWindows()
    updater.stop()
#-----------------------------------------------------------------------------------
# 메인함수
#-----------------------------------------------------------------------------------
def main():
    # 노트북 내장 웹캠 사용
    
    cap = cv2.VideoCapture(0)
    # 화면의 절반을 영역으로 설정, 영역에 얼굴이 있으면 캡쳐후 저장 및 전송
    while True:
        # 봇에서 텍스트를 읽어와 new_text에 저장
        _,img = cap.read()  # Capture frame-by-frame
        cv2.rectangle(img, (0, 0), (img.shape[1]//2, img.shape[0]//1), (0, 255, 0), 2)      
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale
        faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect the faces    
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2) # 얼굴주변에 사각형 그리기
            if x < img.shape[1]//2 and y < img.shape[0]//1:
                cv2.putText(img, "Face", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # 텍스트 삽입
                # 이미지 저장
                cv2.imwrite('face.png', img)                
                # 이미지 전송
                sendTelegramPhoto('face.png')
                # 텍스트 전송
                sendTelegramMessage("얼굴이 감지되었습니다.('시작'또는'start'명령시 재시작) \n 종료명령어는 '정지', 'stop' 입니다.")
                # 챗봇을 통해 재시작 을 받을 때까지 대기
                while True:
                    new_text = bot.getUpdates()[-1].message.text    # 챗봇에서 텍스트를 읽어와 new_text에 저장
                    if new_text == "정지" or new_text == "stop":
                        asyncio.run(stop_bot())
                        break
                    elif new_text == '시작' or new_text == 'start':
                        break
                os.remove('face.png')
                break        
            
        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
#-----------------------------------------------------------------------------------

updater = Updater(token=tok, use_context=True) # 토큰을 통해 봇을 선언합니다.
dispatcher = updater.dispatcher # 메세지를 받기 위한 디스패쳐를 선언합니다.
sendTelegramMessage("서비스가 시작되었습니다. \n 시작명령어는 '시작', 'start' 입니다.") # 봇이 실행되면 메세지를 보냅니다.
updater.start_polling()     # 메세지를 받기 위해 봇을 계속 실행합니다.

print('start telegram chat bot')
def handler(update, context): # 메세지를 받는 핸들러를 선언합니다.
    user_text = update.message.text # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    if user_text == "시작" or user_text == "start":
        sendTelegramMessage("얼굴인식이 시작되었습니다.")
        main()
    elif user_text == "정지" or user_text == "stop":
        sendTelegramMessage("얼굴인식이 종료되었습니다.")
        cv2.destroyAllWindows(user_text)    # 봇을 종료합니다.
        updater.stop() # 봇을 종료합니다.
    else:
        sendTelegramMessage("알 수 없는 명령어입니다.")

echo_handler = MessageHandler(Filters.text, handler)    # 메세지 핸들러를 선언합니다. 
dispatcher.add_handler(echo_handler)

#-----------------------------------------------------------------------------------
