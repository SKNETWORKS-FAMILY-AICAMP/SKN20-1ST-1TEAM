from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import pymysql
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv(dotenv_path=".env")

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database='autoreg_kr',
        charset='utf8mb4'
    )

# --- 셀레니움 크롤링 ---
url = 'https://stat.eseoul.go.kr/statHtml/statHtml.do?orgId=201&tblId=DT_201004_I020002&conn_path=I2&obj_var_id=&up_itm_id='
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(1)

driver.find_element(By.XPATH, "//li[@id='tabTimeText']/a").click()
time.sleep(1)
Select(driver.find_element(By.CSS_SELECTOR, "select[title='시작 시점']")).select_by_value('2015')
Select(driver.find_element(By.CSS_SELECTOR, "select[title='마지막 시점']")).select_by_value('2024')
time.sleep(1)

driver.find_element(By.ID, "searchStat").click()
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')
tr_lists = soup.select('#mainTable > tbody > tr')

male_data, female_data, corp_data = {}, {}, []

current_gender = None
years = list(range(2015, 2025))

for tr in tr_lists:
    td_lists = tr.find_all('td')
    if len(td_lists) < 3:
        continue

    # gender 확인
    gender_title = td_lists[0].get('title', '').strip()
    age_group_title = td_lists[1].get('title', '').strip()

    # 값 추출
    values = []
    for td in td_lists[2:]:
        input_tag = td.find('input')
        if input_tag:
            try:
                values.append(int(input_tag.get('value', '0')))
            except:
                values.append(0)

    if gender_title in ['남성', '여성']:
        current_gender = gender_title
        if age_group_title != '소계':
            if current_gender == '남성':
                male_data[age_group_title] = values
            elif current_gender == '여성':
                female_data[age_group_title] = values
    elif gender_title == '법인 및 사업자':
        corp_data = values
    else:
        # merge row (빈 gender) 처리
        if current_gender == '남성':
            male_data[age_group_title] = values
        elif current_gender == '여성':
            female_data[age_group_title] = values

driver.quit()

# --- DB 삽입용 리스트 생성 ---
data_to_insert = []

for age_group, counts in male_data.items():
    for year, count in zip(years, counts):
        data_to_insert.append((year, '남성', age_group, count))

for age_group, counts in female_data.items():
    for year, count in zip(years, counts):
        data_to_insert.append((year, '여성', age_group, count))

for year, count in zip(years, corp_data):
    data_to_insert.append((year, '법인/사업자', None, count))

# --- DB 삽입 ---
with get_connection() as conn:
    with conn.cursor() as cur:
        sql = "INSERT INTO gender_age_car (year, gender, age_group, car_count) VALUES (%s,%s,%s,%s)"
        print(f"삽입할 데이터 개수: {len(data_to_insert)}")
        print(f"샘플 데이터: {data_to_insert[:5]}")
        cur.executemany(sql, data_to_insert)
    conn.commit()

print("데이터베이스에 삽입 완료!")

