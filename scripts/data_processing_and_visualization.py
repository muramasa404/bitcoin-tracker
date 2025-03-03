import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
df = pd.read_csv('/Users/henry/Desktop/IT_Study/bitcoin-tracker/data/processed/bybit_preprocessed.csv')

df['SMA_50'] = ta.sma(df['close'], length=50)  # 50일 단순 이동 평균
df['SMA_200'] = ta.sma(df['close'], length=200)  # 200일 단순 이동 평균
df['EMA_50'] = ta.ema(df['close'], length=50)  # 50일 지수 이동 평균
df['RSI_14'] = ta.rsi(df['close'], length=14)  # 14일 RSI
df[['BBL', 'BBM', 'BBU']] = ta.bbands(df['close'], length=20)  # 볼린저 밴드

df.dropna(inplace=True)  # 결측치 제거

df.to_csv('/Users/henry/Desktop/IT_Study/bitcoin-tracker/data/processed/bybit_preprocessed.csv', index=False)

print("✅ 기술적 지표 추가 완료!")

# 타임스탬프를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 차트 그리기 (시간에 따른 비트코인 가격 추이)
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Close Price (USD)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 시각화 예시: 비트코인 가격의 분포 (히스토그램)
plt.figure(figsize=(10, 6))
sns.histplot(df['close'], bins=50, kde=True, color='green')
plt.title('Bitcoin Close Price Distribution')
plt.xlabel('Close Price (USD)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()

# 시각화 예시: 가격과 거래량 관계
plt.figure(figsize=(10, 6))
plt.scatter(df['close'], df['volume'], alpha=0.5, color='red')
plt.title('Close Price vs Volume')
plt.xlabel('Close Price (USD)')
plt.ylabel('Volume')
plt.grid(True)
plt.tight_layout()
plt.show()
