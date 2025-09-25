# 🚗 SKN20-1ST-1TEAM  
**자동차 등록 현황 및 기업 FAQ 조회 시스템**


## 💻 프로젝트 목표
시장 전체의 등록 현황 흐름을 한눈에 보여주고,  
핵심 FAQ를 바로 해석해주는 대시보드 제작

---

## 📣 팀 소개
### 1TEAM 머선일이조
본 프로젝트는 차량 등록 현황 데이터를 분석하고 시각화하여  
**연령·성별·지역별 차량 선호도 및 등록 추세**를 한눈에 볼 수 있도록 기획되었습니다.

## 👥 팀원
| <img src="./images/효빈.jpg" width="150"> <br> 김효빈 |  <img src="./images/수현.jpg" width="150"> <br> 황수현 |  <img src="./images/지은.jpg" width="150"> <br> 김지은 |  <img src="./images/소영1.jpg" width="150"> <br> 정소영 |  <img src="./images/민지.jpg" width="150"> <br> 강민지 |
|:------:|:------:|:------:|:------:|:------:|

---

## 📑 프로젝트 개요
- 차량 등록 데이터를 기반으로 **연령/성별/지역/연료별 등록 현황 분석**  
- ERD 및 테이블 명세를 통해 **데이터베이스 구조화**  
- 대시보드 형태로 결과를 시각화하여 **활용성 강화**

## 📚 데이터 출처
- [서울특별시청](https://www.seoul.go.kr/main/index.jsp)  
- [국토교통통계누리](https://stat.molit.go.kr/portal/main/portalMain.do)
- [기아 FAQ](https://www.kia.com/kr/customer-service/center/faq)
- [현대자동차 FAQ](https://www.hyundai.com/kr/ko/e/customer/center/faq)
- [쉐보레 FAQ](https://www.chevrolet.co.kr/faq)

## 📚 데이터 수집 방법
- 엑셀 파일을 이용해 데이터 ERD에 삽입 및 수집
- 웹 크롤링 중 동적 크롤링을 이용하여 데이터 수집



---

## 🗂️ ERD
<img width="764" height="536" alt="ERD IMAGE" src="https://github.com/user-attachments/assets/7889a5e3-91bc-4087-ad6b-bdb3369b976b" />


## 📝 테이블 명세서
<img width="1144" height="761" alt="TABLE SCHEMA" src="https://github.com/user-attachments/assets/43ed1c34-51db-4b64-ab4e-e9601b28f307" />




## 🛠 기술 스택  
<p align="left">
  <img src="https://skillicons.dev/icons?i=python,vscode,mysql,github"/>
</p>

## 👀 시연 이미지
<img width="1000" height="1000" alt="연도별 증감률" src="https://github.com/user-attachments/assets/658eabec-98af-48cd-b6ee-e2878e8b278b" />
<img width="1000" height="1000" alt="성별 연령별" src="https://github.com/user-attachments/assets/c78dfc56-328f-427c-a4e5-096c7538f639" />
<img width="1000" height="1000" alt="연료별 비율" src="https://github.com/user-attachments/assets/f7283030-5384-4bc8-801e-30a75c456eec" />
<img width="1000" height="1000" alt="연료별 차종비율" src="https://github.com/user-attachments/assets/e9a27b8f-e006-4f65-ba76-53d88b1fa6cd" />
<img width="1000" height="1000" alt="지역 차종 자동차 등록 " src="https://github.com/user-attachments/assets/7ace3aea-412e-4610-9811-a0afc76b3c6c" />
<img width="1000" height="1000" alt="지역:차종 등록 지도" src="https://github.com/user-attachments/assets/68cc0bbb-5f9d-4b08-b966-c8e25d5b826b" />
<img width="1000" height="1000" alt="FAQ" src="https://github.com/user-attachments/assets/9f60fd83-ba06-42dc-995c-d4aa2feaad45" />






---

## 💭 한 줄 회고

> #### 김효빈
> 이번 프로젝트에서는 크롤링부터 MySQL 연동, Streamlit까지 구현해볼 수 있어서 매우 의미 있었습니다. 몽고DB만 사용해봤기에 MySQL을 다뤄보고 싶었는데, Workbench가 잘 구조화되어 있어 더 사용하기 편했습니다. 프로젝트 과정에서 모르는 부분은 도움을 받고, 내가 도움을 주는 과정을 통해 성장할 수 있었습니다. 프로젝트를 진행하며 기본적인 속성과 경로 문제가 생각보다 중요하다는 것을 알 수 있었습니다. 우리 팀은 역할 분배가 잘 이루어져 프로젝트를 안정적으로 마무리할 수 있었고, 무엇보다 실제로 프로젝트를 진행하며 이론으로 배운 것들을 직접 경험할 수 있어 좋았습니다.

---

> #### 황수현
> 처음으로 팀원을 꾸려 프로젝트를 하는거라 걱정을 조금 했지만 팀원들이 모두 너무 열정적으로 참여해 줘서 프로젝트를 무사히 끝낼 수 있엇습니다. 웹 크롤링을 처음해보고 DB에 연결하는 과정에서 오류도 많고 실수도 많아 어려움이 있었지만, 팀원의 도움으로 해결하는 과정들이 흥미롭고 재밌었습니다. git을 사용할 줄은 알았지만 이렇게 적극적으로 사용해 본적이 없어 알게된 것도 많아서 좋았습니다. 그리고 개인적 목표인 프로젝트를 하는것에 대한 두려움을 이겨내는 첫번째 시도를 무사히 끝낸 것 같아 기쁩니다.

---

> #### 김지은
> 데이터 크롤링 하는 과정에 많은 심사숙고가 있었습니다.
(사이트에 있는 데이터 인덱스를 파악하고, 그걸 알맞게 데이터 전처리하는 과정에서
사이트 행갯수가 어느기간부터 사라져 데이터가 밀리거나, 표의 열이 초반에 잘안보이던 '계'로인해서 한줄씩 밀리거나.. 등등) 수시로 데이터를 조리하면서 데이터 문제가 없는지 끈기있게 점검해야되는 구나 라는 생각이 들었습니다.
제자신이 이번에 배운 웹 크롤링을 다 습득하고, 다른 팀원분들이 한 엑셀 크롤링과 streamlit 제작 구현에 대해서도 좀더 구체적으로 알아볼 수는 시간을 가지면 좋겠습니다. 그리고 직접 수집된 데이터를 통해 데이터 분석하는 과정을 가져보는 것도 재미있겠다는 생각이 들었습니다!
좋은 팀 분위기에 힘입어 더열심히 할수있게된것같아 팀원분들께 감사합니다.

---

> #### 정소영
> 이번 단기 프로젝트로 동적 크롤링과 MySQL(ERD)를 한 단계 끌어올린 계기가 된 것 같다. 시행착오가 많았지만 서로 배워가며 작업했고, 공유 채널은 통일하자는 교훈도 얻었다. 팀명도 못 정한 채 우다다 달렸지만 열정은 넘쳐서 무척이나 재미있었다. 한 줄로 요약하면, "힘들었지만 어떻게든 해냈으니 좋았어!" 정도이지 않을까 싶다. 다들 고생했고 앞으로 다른 팀으로 가서도, 진도를 나가더라도 죽었다 생각하고 같이 더 고생해봐요!!

---

> #### 강민지
> 팀 프로젝트는 처음이라 적응할 수 있을지 걱정되었지만 팀원들이 같이 으쌰으쌰 해주는 분위기여서 빠르게 적응할 수 있었습니다. 크롤링 작업 도중 ValueError를 포함한 수많은 오류들을 해결하는 데 한데 모여 빨간 오류가 없어질 때까지 해결하는 과정이 너무 즐거웠습니다. 그 과정을 통해 DB 연동 및 git에 대해 어느 정도 흐름을 알게 되었고, AI에게 명령하는 방법이나, 모듈 설치 방법 등 많은 것을 알게 되어 한층 성장할 수 있었습니다.



---
