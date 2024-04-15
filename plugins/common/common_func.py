import bcrypt
#import pybase64
from datetime import datetime, timedelta, timezone
import requests
import json
import time
import pandas as pd

def get_sftp():
    print('sftp작업을 실행합니다.')


def regist(name, sex, *args):
    print(f'이름: {name}')
    print(f'성별: {sex}')
    print(f'기타옵션들: {args}')

def regist2(name, sex, *args, **kwargs):
    print(f'이름 : {name}')
    print(f'성별 : {sex}')
    print(f'기타옵션들 : {args}')
    email = kwargs['email'] or None
    phone = kwargs['phone'] or None
    if email:
        print(email)
    if phone:
        print(phone)

def access_token(**kwargs):

    id = kwargs['nav_id']
    secret = kwargs['nav_secret']
    dev_host = "https://api.commerce.naver.com/external"
    #전자서명 생성
    timestamp = int(round(time.time() * 1000))
    password = id + "_" + str(timestamp)
    #hashed = bcrypt.hashpw(password.encode('utf-8'), secret.encode('utf-8'))
    #sign = pybase64.standard_b64encode(hashed).decode('utf-8')

    #토큰 발급
    url = f"{dev_host}/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 요청 본문 데이터
    data = {
        "client_id": id,
        "timestamp": timestamp,
        "grant_type": 'client_credentials',
    #    "client_secret_sign": sign,
        "type": 'SELF',
    }

    #response = requests.post(url, headers=headers, data=data)
    #access_token = response.json()['access_token']
    access_token = "6U0cEmhjkdGhZuxSVmyoTY"
    return access_token


def list_order(access_token):
    
    # 최종 데이터프레임 출력
    print(f'결제건수 : #건')
