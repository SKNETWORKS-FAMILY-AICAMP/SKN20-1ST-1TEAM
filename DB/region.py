import pandas as pd
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pymysql
from dotenv import load_dotenv
import os

load_dotenv(".env")

# DB 연결 정보
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# 1. 엑셀 파일 읽기
file_path = "DATA/regiondata.xlsx"
df = pd.read_excel(file_path, header=0)

# 컬럼 이름 지정
df.columns = ['ym', 'region', 'passenger_total', 'bus_total', 'truck_total', 'special_total', 'total_count']

# 필요한 열만 선택
df = df[['ym', 'region', 'passenger_total', 'bus_total', 'truck_total', 'special_total', 'total_count']]

# ✅ 숫자형 데이터 전처리 (콤마 제거 후 int 변환)
num_cols = ["passenger_total", "bus_total", "truck_total", "special_total", "total_count"]
for col in num_cols:
    df[col] = df[col].astype(str).str.replace(",", "", regex=False).astype(int)

print(df.head())  # 데이터 확인

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )

# SQLAlchemy 엔진 생성
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)

# 테이블 이름
table_name = "car_reg_region"

# 데이터프레임을 DB로 저장
df.to_sql(
    name=table_name,
    con=engine,
    if_exists='append',  # 기존 테이블 유지 후 추가
    index=False
)

print("데이터베이스 저장 완료! ✅")
