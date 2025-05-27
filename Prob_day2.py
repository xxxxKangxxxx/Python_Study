# # # 과제 2일차 

# 과제 1

# # # 방법1: 데이터 프레임 변환 후 groupby() 함수 사용해서 해결 

# # # 연도별 판매량 계산
# # # 제품별 평균 가격 계산
# # # 최대 판매 지역 찾기
# # # 분기별 매출 분석 

# # import pandas as pd

# # # 데이터: (연도, 분기, 제품, 가격, 판매량, 지역)
# # sales_data = [
# #     (2020, 1, "노트북", 1200, 100, "서울"),
# #     (2020, 1, "스마트폰", 800, 200, "부산"),
# #     (2020, 2, "노트북", 1200, 150, "서울"),
# #     (2020, 2, "스마트폰", 800, 250, "대구"),
# #     (2020, 3, "노트북", 1300, 120, "인천"),
# #     (2020, 3, "스마트폰", 850, 300, "서울"),
# #     (2020, 4, "노트북", 1300, 130, "부산"),
# #     (2020, 4, "스마트폰", 850, 350, "서울"),
# #     (2021, 1, "노트북", 1400, 110, "대구"),
# #     (2021, 1, "스마트폰", 900, 220, "서울"),
# #     (2021, 2, "노트북", 1400, 160, "인천"),
# #     (2021, 2, "스마트폰", 900, 270, "부산"),
# #     (2021, 3, "노트북", 1500, 130, "서울"),
# #     (2021, 3, "스마트폰", 950, 320, "대구"),
# #     (2021, 4, "노트북", 1500, 140, "부산"),
# #     (2021, 4, "스마트폰", 950, 370, "서울"),
# # ]

# # df = pd.DataFrame(sales_data, columns=["연도", "분기", "제품", "가격", "판매량", "지역"])

# # result_1 = df.groupby("연도")["판매량"].sum()
# # result_2 = df.groupby("제품")["가격"].mean()
# # result_3 = df.groupby("지역")["판매량"].sum()
# # df["매출"] = df["가격"] * df["판매량"]
# # result_4 = df.groupby("분기")["매출"].sum()

# # print(f"연도별 판매량: {result_1}\n")
# # print(f"제품별 평균 가격: {result_2}\n")
# # print(f"최대 판매 지역: {result_3}\n")
# # print(f"분기별 매출: {result_4}\n")

# # ----------------------------------------------------------------------------

# # 방법2: 반복문 사용

# # 연도별 판매량 계산
# # 제품별 평균 가격 계산
# # 최대 판매 지역 찾기
# # 분기별 매출 분석 

# # 데이터: (연도, 분기, 제품, 가격, 판매량, 지역)
# sales_data = [
#     (2020, 1, "노트북", 1200, 100, "서울"),
#     (2020, 1, "스마트폰", 800, 200, "부산"),
#     (2020, 2, "노트북", 1200, 150, "서울"),
#     (2020, 2, "스마트폰", 800, 250, "대구"),
#     (2020, 3, "노트북", 1300, 120, "인천"),
#     (2020, 3, "스마트폰", 850, 300, "서울"),
#     (2020, 4, "노트북", 1300, 130, "부산"),
#     (2020, 4, "스마트폰", 850, 350, "서울"),
#     (2021, 1, "노트북", 1400, 110, "대구"),
#     (2021, 1, "스마트폰", 900, 220, "서울"),
#     (2021, 2, "노트북", 1400, 160, "인천"),
#     (2021, 2, "스마트폰", 900, 270, "부산"),
#     (2021, 3, "노트북", 1500, 130, "서울"),
#     (2021, 3, "스마트폰", 950, 320, "대구"),
#     (2021, 4, "노트북", 1500, 140, "부산"),
#     (2021, 4, "스마트폰", 950, 370, "서울"),
# ]

# # ------------------------------------
# # 1. 결과 저장용 딕셔너리 초기화
# # ------------------------------------
# sales_by_year = {}          # 연도별 판매량 누적할 딕셔너리
# product_price_total = {}    # 제품별 가격 총합 누적할 딕셔너리
# product_count = {}          # 제품별 등장 횟수 (평균 계산용)
# region_sales = {}           # 지역별 총 판매량 저장
# quarter_revenue = {}        # 분기별 매출 (가격 * 수량) 저장

# # ------------------------------------
# # 2. 데이터 반복 처리
# # ------------------------------------
# for year, quarter, product, price, quantity, region in sales_data:
#     # 튜플의 각 항목을 변수에 분해
#     # year: 연도, quarter: 분기, product: 제품명, price: 가격, quantity: 판매량, region: 지역

#     # 연도별 판매량 계산
#     if year not in sales_by_year:
#         # 해당 연도가 처음 등장한 경우, 초기값 0 설정
#         sales_by_year[year] = 0
#     # 해당 연도의 기존 판매량에 현재 판매량을 더함
#     sales_by_year[year] += quantity

#     # 제품별 평균 가격 계산을 위한 누적값 저장
#     if product not in product_price_total:
#         # 처음 등장한 제품일 경우 가격 총합과 등장 횟수 초기화
#         product_price_total[product] = 0
#         product_count[product] = 0
#     # 가격 총합 누적
#     product_price_total[product] += price
#     # 해당 제품의 등장 횟수 증가
#     product_count[product] += 1

#     # 지역별 판매량 계산
#     if region not in region_sales:
#         # 처음 등장한 지역일 경우 초기화
#         region_sales[region] = 0
#     # 해당 지역의 판매량 누적
#     region_sales[region] += quantity

#     # 분기별 매출 계산 (가격 * 판매량)
#     if quarter not in quarter_revenue:
#         # 처음 등장한 분기일 경우 초기화
#         quarter_revenue[quarter] = 0
#     # 해당 분기의 매출에 현재 제품 매출 추가
#     quarter_revenue[quarter] += price * quantity

# # ------------------------------------
# # 3. 분석 결과 출력
# # ------------------------------------

# # 연도별 판매량 출력
# for year, total_quantity in sales_by_year.items():
#     # 각 연도별로 누적된 판매량 출력
#     print(f"{year}년 총 판매량: {total_quantity}")

# print("")  # 줄바꿈

# # 제품별 평균 가격 출력
# for product in product_price_total:
#     # 평균 가격 = 가격 총합 / 등장 횟수
#     avg_price = product_price_total[product] / product_count[product]
#     print(f"{product}의 평균 가격: {avg_price:.1f}")

# print("")  # 줄바꿈

# # 최대 판매 지역 출력
# # 판매량이 가장 높은 지역을 key로 선택
# max_region = max(region_sales, key=region_sales.get)
# print(f"가장 많이 판매된 지역: {max_region} ({region_sales[max_region]}개)")

# print("")  # 줄바꿈

# # 분기별 매출 출력
# # 정렬된 분기 순서대로 출력 (1~4분기)
# for quarter in sorted(quarter_revenue):
#     print(f"{quarter}분기 총 매출: {quarter_revenue[quarter]}")



# # ------------------------------------------------------------------------------------------

# # 방법3: 함수 사용

# # 판매 데이터: (연도, 분기, 제품, 가격, 판매량, 지역)
# sales_data = [
#     (2020, 1, "노트북", 1200, 100, "서울"),
#     (2020, 1, "스마트폰", 800, 200, "부산"),
#     (2020, 2, "노트북", 1200, 150, "서울"),
#     (2020, 2, "스마트폰", 800, 250, "대구"),
#     (2020, 3, "노트북", 1300, 120, "인천"),
#     (2020, 3, "스마트폰", 850, 300, "서울"),
#     (2020, 4, "노트북", 1300, 130, "부산"),
#     (2020, 4, "스마트폰", 850, 350, "서울"),
#     (2021, 1, "노트북", 1400, 110, "대구"),
#     (2021, 1, "스마트폰", 900, 220, "서울"),
#     (2021, 2, "노트북", 1400, 160, "인천"),
#     (2021, 2, "스마트폰", 900, 270, "부산"),
#     (2021, 3, "노트북", 1500, 130, "서울"),
#     (2021, 3, "스마트폰", 950, 320, "대구"),
#     (2021, 4, "노트북", 1500, 140, "부산"),
#     (2021, 4, "스마트폰", 950, 370, "서울"),
# ]

# # ---------------------------------------------
# # ✅ 함수 정의 영역
# # ---------------------------------------------

# # 1. 연도별 총 판매량 계산 함수
# def calc_sales_by_year(data):
#     sales_by_year = {}  # 연도별 판매량 저장할 딕셔너리

#     for year, _, _, _, quantity, _ in data:
#         # 연도가 없으면 초기화
#         if year not in sales_by_year:
#             sales_by_year[year] = 0
#         # 판매량 누적
#         sales_by_year[year] += quantity

#     return sales_by_year


# # 2. 제품별 평균 가격 계산 함수
# def calc_avg_price_by_product(data):
#     total_price = {}  # 제품별 가격 총합
#     count = {}        # 제품별 등장 횟수

#     for _, _, product, price, _, _ in data:
#         if product not in total_price:
#             total_price[product] = 0
#             count[product] = 0
#         total_price[product] += price
#         count[product] += 1

#     # 평균 가격 = 총합 / 개수
#     return {product: total_price[product] / count[product] for product in total_price}


# # 3. 최대 판매 지역 찾기 함수
# def calc_top_region_by_sales(data):
#     region_sales = {}  # 지역별 판매량 저장

#     for _, _, _, _, quantity, region in data:
#         if region not in region_sales:
#             region_sales[region] = 0
#         region_sales[region] += quantity

#     # 가장 많이 판매된 지역 찾기
#     max_region = max(region_sales, key=region_sales.get)

#     return max_region, region_sales[max_region], region_sales


# # 4. 분기별 매출 계산 함수 (매출 = 가격 × 판매량)
# def calc_revenue_by_quarter(data):
#     revenue_by_quarter = {}  # 분기별 매출 저장

#     for _, quarter, _, price, quantity, _ in data:
#         if quarter not in revenue_by_quarter:
#             revenue_by_quarter[quarter] = 0
#         revenue_by_quarter[quarter] += price * quantity

#     return revenue_by_quarter

# # ---------------------------------------------
# # ✅ 분석 결과 출력 영역
# # ---------------------------------------------

# # (1) 연도별 판매량 출력
# print("✅ 연도별 총 판매량 (단위: 개)")
# for year, total in sorted(calc_sales_by_year(sales_data).items()):
#     print(f"{year}년: {total:,}개")  # ,로 천 단위 구분

# print("\n✅ 제품별 평균 가격 (단위: 만원)")
# avg_price = calc_avg_price_by_product(sales_data)
# for product in sorted(avg_price):
#     print(f"{product}: {avg_price[product]:.1f}만원")  # 소수점 1자리

# # (3) 최대 판매 지역 출력
# print("\n✅ 최대 판매 지역")
# region, amount, region_sales = calc_top_region_by_sales(sales_data)
# print(f"{region} ({amount:,}개)")  # 최다 판매 지역
# print("지역별 판매량:")
# for r in sorted(region_sales):
#     print(f"- {r}: {region_sales[r]:,}개")

# # (4) 분기별 매출 출력
# print("\n✅ 분기별 총 매출 (단위: 만원)")
# revenue_by_quarter = calc_revenue_by_quarter(sales_data)
# for quarter in sorted(revenue_by_quarter):
#     print(f"{quarter}분기: {revenue_by_quarter[quarter]:,}만원")

# --------------------------------------------------------------------
# 
# # 과제 2

# # 주소록 프로그램
# # 연락처 이름을 키로 하고, 전화번호, 이메일, 주소 등의 정보를 값으로 저장
# # 중첩 딕셔너리 구조를 사용하여 각 연락처마다 여러 정보를 저장
# # 연락처 추가, 삭제, 검색, 수정, 모든 연락처 보기 기능을 구현

# contact_book = {}

# # 연락처 추가 함수
# def add_contact():
#     name = input("이름을 입력하세요: ")
#     if name in contact_book:
#         print("이미 존재하는 이름입니다. ")
#         return # 함수 실행 중단 
#     phone_num = input("연락처를 입력하세요: ")
#     email = input("이메일을 입력하세요: ")
#     address = input("주소를 입력하세요: ")

#     # 중첩 딕셔너리 구조로 저장
#     contact_book[name] = {
#         "전화번호": phone_num,
#         "이메일": email,
#         "주소": address
#     }
#     print(f"{name}님이 추가되었습니다.")

# # 연락처 삭제 함수
# def delete_contact():
#     name = input("삭제할 연락처의 이름을 입력하세요: ")
#     if name in contact_book:
#         del contact_book[name]
#         print(f"{name}의 연락처가 삭제되었습니다. ")
#     else:
#         print("존재하지 않는 연락처입니다. ")

# # 연락처 검색 함수 
# def search_contact():
#     name = input("검색할 연락처의 이름을 입력하세요: ")
#     if name in contact_book:
#         print(f"이름: {name}")
#         for key, value in contact_book[name].items():
#             print(f"{key}: {value}")
#     else:
#         print("해당 연락처가 존재하지 않습니다. ")

# # 연락처 수정 함수 
# def edit_contact():





# ----------------------------------------------------------------

