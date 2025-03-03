import os
import pandas as pd
import requests

BYBIT_URL = "https://api.bybit.com/v5/market/kline"

params = {
    "symbol": "BTCUSDT",
    "interval": "60",  # 1시간 봉
    "start": 1704067200000,  # 시작 시간 (UTC 밀리초 단위)
    "limit": 200  # 가져올 캔들 개수
}

response = requests.get(BYBIT_URL, params=params)
data = response.json()

# 데이터 추출
if "result" in data and "list" in data["result"]:
    kline_data = data["result"]["list"]

    # ✅ 응답 데이터 구조 확인 (디버깅용)
    print(kline_data[:3])  # 처음 3개 데이터 출력

    # ✅ 컬럼 개수 맞춰서 데이터프레임 생성
    df = pd.DataFrame(kline_data, columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"])

    # ✅ 데이터 타입 변환 (문자열 → 숫자)
    df = df.astype({
        "timestamp": "int64",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "turnover": "float64"
    })

    # ✅ 타임스탬프를 날짜로 변환
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # ✅ 디렉토리 확인 및 생성
    output_dir = "/Users/henry/Desktop/IT_Study/bitcoin-tracker/data/processed"
    os.makedirs(output_dir, exist_ok=True)  # 디렉토리가 없으면 생성

    # ✅ CSV 저장
    df.to_csv(f"{output_dir}/bybit_preprocessed.csv", index=False)

    print("✅ 데이터 저장 완료: data/processed/bybit_preprocessed.csv")
