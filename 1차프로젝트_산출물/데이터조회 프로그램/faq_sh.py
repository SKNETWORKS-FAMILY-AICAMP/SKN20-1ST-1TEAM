# chevy_faq_upsert.py
import os
import time
import pymysql
from dotenv import load_dotenv

# --- Selenium ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.chevrolet.co.kr/faq"


def get_data():
    """
    쉐보레 FAQ 페이지에서 하드코딩된 첫 번째 항목(예시)을 클릭해
    (질문, 답변) 튜플 리스트로 반환.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 12)

    try:
        driver.get(URL)
        driver.maximize_window()
        print("사이트 접속했습니다.")
        time.sleep(1)  # 초기 렌더 텀

        # 목록의 첫 번째 카드 클릭 (사용자 코드 유지)
        of = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="gb-main-content"]/adv-grid[5]/adv-col/div/div[7]/div/div[1]')))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", of)
        of.click()
        time.sleep(2)

        # 질문 텍스트
        sq = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gb-main-content"]/adv-grid[5]/adv-col/div/div[7]/div/div[1]/h6'))).text
        sq = sq.strip().replace("[차량관리] ", "")

        # 답변 텍스트
        sa_el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="gb-main-content"]/adv-grid[5]/adv-col/div/div[7]/div/div[2]/gb-content-well/adv-grid/adv-col/div/div/div')))
        # 여러 <p>가 있을 수 있으므로 전체 텍스트에서 줄바꿈 정리
        sa = " ".join(sa_el.text.split())

        pair_list = [(sq, sa)]
        return pair_list

    finally:
        driver.quit()


# --- DB 연결/업서트 ---
def get_connection():
    """
    .env에서 DB_HOST, DB_USER, DB_PASSWORD 를 읽어
    autoreg_kr 데이터베이스로 연결
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database="autoreg_kr",
        charset="utf8mb4",
    )


UPSERT_SQL = """
INSERT INTO faq (question, answer)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE
  question = VALUES(question),
  answer   = VALUES(answer);
"""


def main():
    # 1) 환경변수 로드
    load_dotenv()

    # 2) 크롤링
    datas = get_data()  # [(question, answer), ...]
    if not datas:
        print("[info] 수집된 데이터가 없습니다.")
        return

    # 3) DB 업서트
    with get_connection() as conn:
        with conn.cursor() as cur:
            for q, a in datas:
                cur.execute(UPSERT_SQL, (q, a))
        conn.commit()

    print(f"[done] 총 {len(datas)}건 업서트 완료")


main()
