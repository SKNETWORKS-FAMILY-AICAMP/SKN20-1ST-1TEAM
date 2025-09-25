# kia_faq_upsert.py
import os
import time
import pymysql
from dotenv import load_dotenv

# --- Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# (선택) 헤드리스 옵션 사용하려면 주석 해제
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument("--headless=new")

URL = "https://www.kia.com/kr/customer-service/center/faq"

def get_data():
    """KIA FAQ 특정 항목(하드코딩된 ID)에서 (질문,답변) 튜플 리스트 반환"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)  # , options=chrome_options
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL)
        driver.maximize_window()
        time.sleep(1)  # 초기 렌더 텀

        target_ids = [1, 6, 7, 8, 9]  # 필요한 항목만
        pairs = []

        for i in target_ids:
            btn_id = f"accordion-item-{i}-button"
            panel_id = f"accordion-item-{i}-panel"

            try:
                # 버튼 클릭 가능 대기 후 클릭
                btn = wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                btn.click()

                # 패널 가시화 대기
                wait.until(EC.visibility_of_element_located((By.ID, panel_id)))

                # 질문 / 답변 추출
                question = btn.text.strip().replace("%_", "")  # 필요 없으면 replace 제거
                panel = driver.find_element(By.ID, panel_id)

                # 줄바꿈 정리(빈 줄 제거, 단락 유지)
                answer = "\n".join(
                    line.strip()
                    for line in panel.text.splitlines()
                    if line.strip()
                )

                pairs.append((question, answer))

            except Exception as e:
                print(f"[warn] item {i} skip: {e}")
                continue

        return pairs

    finally:
        driver.quit()


# --- DB 연결/업서트 ---
def get_connection():
    """pymysql 커넥션 반환 (.env 필요: DB_HOST, DB_USER, DB_PASSWORD)"""
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database='autoreg_kr',
        charset='utf8mb4'
    )

UPSERT_SQL = """
INSERT INTO faq (question, answer)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE
  question = VALUES(question),
  answer   = VALUES(answer);
"""


def main():
    # 1) .env 로드
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