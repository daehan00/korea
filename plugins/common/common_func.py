import bcrypt
import pybase64
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
    hashed = bcrypt.hashpw(password.encode('utf-8'), secret.encode('utf-8'))
    sign = pybase64.standard_b64encode(hashed).decode('utf-8')

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
        "client_secret_sign": sign,
        "type": 'SELF',
    }

    response = requests.post(url, headers=headers, data=data)
    access_token = response.json()['access_token']
    return access_token


def list_order(access_token):
    # 상품 주문 내역 조회(default 24시간, 300개)
    headers = {"Authorization" : f"Bearer {access_token}"}
    url = "https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses"
    now = datetime.now(timezone(timedelta(hours=9)))  # UTC+9
    weekday = now.weekday()  # 현재 요일 (월요일: 0, 일요일: 6)

    final_df = pd.DataFrame()

    # 월요일이면 지난 3일간의 정보 조회, 그 외에는 최근 1일간의 정보 조회
    if weekday == 0:
        days_to_fetch = 3  # 월요일에는 금요일부터 일요일까지 3일간 조회
    else:
        days_to_fetch = 1  # 다른 날에는 당일만 조회

    for days in range(days_to_fetch, 0, -1):
        sc_from = now - timedelta(days=days)
        
        sc_from_str = sc_from.strftime('%Y-%m-%dT%H:%M:%S.000+09:00')

        # 요청 파라미터 설정
        params = {
            "lastChangedFrom": sc_from_str
        }

        # GET 요청 실행
        response = requests.get(url, headers=headers, params=params)

        # 응답 검사
        if response.status_code == 200:
            try:
                all_data = response.json().get('data', {}).get('lastChangeStatuses', [])
                data_rows = []

                for data in all_data:
                    payment_date_str = data.get('paymentDate', '')
                    payment_date = pd.to_datetime(payment_date_str) if payment_date_str else None

                    # 'paymentDate'가 'sc_from' 이후인 데이터만 처리
                    if payment_date and payment_date >= sc_from:
                        data_row = {
                            'productOrderId': data.get('productOrderId', ''),
                            'orderId': data.get('orderId', ''),
                            'productOrderStatus': data.get('productOrderStatus', ''),
                            'paymentDate': payment_date_str,
                            'lastChangedDate': data.get('lastChangedDate', ''),
                            'lastChangedType': data.get('lastChangedType', ''),
                            'receiverAddressChanged': data.get('receiverAddressChanged', ''),
                            'claimType': data.get('claimType', ''),
                            'claimStatus': data.get('claimStatus', ''),
                            'giftReceivingStatus': data.get('giftReceivingStatus', '')
                        }
                        data_rows.append(data_row)

                # 일별 데이터프레임 생성
                day_df = pd.DataFrame(data_rows)
                final_df = pd.concat([final_df, day_df], ignore_index=True)
                count = len(final_df)

            except Exception as e:
                print(f"Failed to parse response from {sc_from_str}: {e}")
        else:
            print(f"Failed to fetch data from {sc_from_str}: {response.status_code} {response.text}")

    # 최종 데이터프레임 출력
    print(f'결제건수 : {count}건')
