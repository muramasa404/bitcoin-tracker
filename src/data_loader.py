import requests
import pandas as pd
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("BYBIT_API_KEY")

def get_bybit_ohlcv(symbol="BTCUSDT", interval="60", limit=200):
    url = "https://api.bybit.com/v5/market/kline"
    headers = {
        "X-BYBIT-API-KEY": API_KEY  # API Key 추가
    }
    params = {
        "category": "spot",
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "result" not in data:
        raise ValueError("API 응답 오류:", data)

    kline_data = data["result"]["list"]
    
    # 데이터프레임 변환
    df = pd.DataFrame(kline_data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "turnover"
    ])
    
    # 시간 변환 (밀리초 → 일반 날짜)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    
    # 숫자로 변환
    df[["open", "high", "low", "close", "volume", "turnover"]] = df[
        ["open", "high", "low", "close", "volume", "turnover"]
    ].astype(float)
    
    return df

if __name__ == "__main__":
    df = get_bybit_ohlcv()
    print(df.head())  # 데이터 확인
