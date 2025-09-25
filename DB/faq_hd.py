import pymysql
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# 환경변수 불러오기
load_dotenv()

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database='autoreg_kr',
        charset='utf8mb4'  # 한글 깨짐 방지
    )

# FAQ 크롤링 함수 (여러 개 FAQ를 리스트로 반환)
def get_data():
    qa_list = []

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get('https://www.hyundai.com/kr/ko/faq.html')
        print('사이트 접속 완료')
        time.sleep(3)

        # 차량정비 카테고리 클릭
        category = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div/div[2]/div/div[1]/div[1]/dl[3]/dt/button')
        category.click()
        print('차량정비 카테고리 클릭 완료')
        time.sleep(3)

        # 페이지 소스 가져와서 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # FAQ 목록 추출
        faqs = soup.select('#contents > div.faq > div > div.section_white > div > div.result_area > div.ui_accordion.acc_01 > dl')

        for faq in faqs:
            question = faq.find('dt').get_text().replace('more 닫기', '').replace('[ 차량정비 > 일반 ]', '').strip()
            answer = faq.find('dd').get_text().strip()
            qa_list.append((question, answer))
        
        print(f"총 {len(qa_list)}개의 FAQ 수집 완료")

    except Exception as e:
        print(f"오류: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
        print("크롤링 완료")
    
    return qa_list

# DB 저장
def save_to_db(qa_list):
    if not qa_list:
        print("저장할 데이터 없음")
        return

    with get_connection() as conn:
        sql = 'INSERT INTO faq (question, answer) VALUES (%s, %s)'  # id는 AUTO_INCREMENT
        with conn.cursor() as cur:
            for q, a in qa_list:
                cur.execute(sql, (q, a))
        conn.commit()
    print('DB 저장 완료 ✅')

# 실행
if __name__ == "__main__":
    qa_list = get_data()
    # 3번째 FAQ만 저장
    if len(qa_list) >= 3:
        save_to_db([qa_list[2]])  # 3번째 요소만 리스트로 전달
    else:
        print("FAQ가 3개 미만입니다.")