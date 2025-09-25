from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 엔터 키등을 입력하기 위해 사용
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 웹드라이버를 자동으로 설치하고 최신버전을 유지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get('https://stat.eseoul.go.kr/statHtml/statHtml.do?orgId=201&tblId=DT_201004_I020004&conn_path=I2&obj_var_id=&up_itm_id=')
driver.maximize_window()
print('브라우저가 성공적으로 열렸습니다.')
time.sleep(3)

# 시점 -> 시작 지점 -> 2015.12 -> 2024.12

# 시점 클릭
point_click = driver.find_element(By.ID,'tabTimeText')
point_click.click()
time.sleep(2)

# 2015.12 클릭
# start_point_click = driver.find_element(By.XPATH,'//*[@id="timeM"]/h2/select[1]/option[109]')
# start_point_click.click()
# select 요소 찾기
select_element = driver.find_element("css selector", "select.box")  # class="box"인 select
# Select 객체 생성
select = Select(select_element)
# 방법 1: value 값으로 선택
select.select_by_value("201512")  # 2015.12
time.sleep(3)

# 2024.12 클릭
y2020_m01_click = driver.find_element(By.XPATH,'//*[@id="timeM"]/h2/select[1]/option[120]')
y2020_m01_click.click()
time.sleep(3)

# 조회 v 클릭
y2025_m01_click = driver.find_element(By.XPATH,'//*[@id="tabTimeText"]/button[2]')
y2025_m01_click.click()
time.sleep(15)

# 해당 정보를 담은 문자열 추출 (4)
soup = BeautifulSoup(driver.page_source,'html.parser')
fuel_car_datas = soup.select('#mainTable > tbody > tr')

# 행 별로 저장
total_rows = []
for i, row in enumerate(fuel_car_datas[:5]): # 상위 5행만 처리 range(0,4)
    tds = row.select('td')
    total_rows.append([td.text.replace('\xa0','') for td in tds])



###############################################################


car_types = ['승용차','승합차','화물차','특수차']
fuel_list = ['휘발유','경유','LPG','전기','CNG','하이브리드','수소','기타','소계']

# 쿼리를 담을 리스트
queries = []

start_year = 2024
start_month = 12

for idx, row in enumerate(zip(*[data[3:] for data in total_rows[1:]])):
    # 총 몇 개 월이 지나갔는지 계산 (9개 단위로 1개월 감소)
    months_ago = idx // 9

    # 연도 계산
    year = start_year
    month = start_month - months_ago

    # month가 0 이하이면 연도 감소 + 월 12부터 다시 시작
    while month <= 0:
        month += 12
        year -= 1

    # ym 문자열
    ym = f"{year}{month:02d}"

    # 2015년 12월 이전이면 반복 종료
    if int(ym) < 201512:
        break

    fuel = fuel_list[idx % 9]

    for i, car in enumerate(car_types):
        count = row[i]
        try:
            count_int = int(str(count).replace(',',''))
        except:
            count_int = 0
        queries.append((ym, car, fuel, count_int))
#################################################
print(queries[:5])

import pymysql
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

# sautoreg_kr
def get_connection():
    return pymysql.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database= 'autoreg_kr'
    )
conn = get_connection()
cursor = conn.cursor()

# 모든 쿼리를 한 번에 실행

table_name = "fuel_car"
sql = f"INSERT INTO {table_name} (ym, car_type, fuel_type, car_count) VALUES (%s, %s, %s, %s)"
cursor.executemany(sql, queries)

# 커밋
conn.commit()

# 연결 종료
cursor.close()
conn.close()
