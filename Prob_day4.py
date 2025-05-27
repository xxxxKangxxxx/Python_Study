# # 과제: 제너레이터 함수 작성 

# # 로그 파일을 한 줄씩 읽는 제너레이터 함수 작성
# # 특정 패턴(예: 'ERROR', 'WARNING' 등)이 포함된 줄만 필터링하는 제너레이터 작성

# def read_log_lines(filepath):
#     """로그 파일을 한 줄씩 읽어들이는 제너레이터 함수"""
#     try:
#         # open()을 통해 파일을 '읽기 모드'로 UTF-8 인코딩을 사용해 연다.
#         with open(filepath, 'r', encoding='utf-8') as f:
#             # 파일의 각 줄에 대해 반복
#             for line in f: # for 문을 통해 한줄 단위로 읽는다. 
#                 yield line.strip()  # yield를 통해 한 줄 씩 반환 / 줄 끝 개행 제거하고 한 줄씩 반환 

#     except FileNotFoundError:
#         # 파일이 존재하지 않을 경우 예외 처리
#         print(f"파일을 찾을 수 없습니다: {filepath}")

#     except Exception as e:
#         # 다른 예외가 발생했을 경우 에러 메시지 출력
#         print(f"예외 발생: {e}")

# # log_lines: 로그 텍스트가 한 줄 씩 들어오는 이터러블
# # patterns: 필터링할 문자열 패턴들의 튜플 
# def filter_log_by_level(log_lines, patterns=('ERROR', 'WARNING')): # 주어진 로그 줄 들 중 
#     """특정 패턴이 포함된 로그 줄만 필터링하는 제너레이터"""

#     for line in log_lines:  # log_lines는 제너레이터 또는 리스트도 가능

#         # 패턴 중 하나라도 현재 줄에 포함되어 있다면
#         if any(pat in line for pat in patterns):
#             yield line  # 그 줄을 반환



# ==================================================================================================================

# 과제: 동시성과 병렬처리 

# 5개의 공개 API에 GET 요청을 보냄 
# 세 가지 방식으로 구현하고 성능을 비교 
# - 순차 처리 
# - ThreadPoolExecutor
# - asyncio와 aiohttp 

import time
import requests
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 테스트할 API 목록 
API_URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
]

# 모든 URL에 대해 순차적으로 requests.get으로 HTTP 요청을 보내는 함수 / 하나의 요청이 끝나면 다음 요청 수행 
def fetch_sequential(urls):
    results = [] # 결과 저장 리스트 생성 

    for url in urls: # URL을 하나씩 순회하면서 하나씩 처리 
        response = requests.get(url)  # 현재 URL에 대해 동기 방식의 HTTP GET 요청을 보냄 (블로킹 방식)
        results.append(response.json())  # 응답 객체에서 JSON 데이터를 추출해 리스트에 추가 

    return results # 결과 반환 

# 병렬 처리할 때 각 스레드에서 실행될 단일 URL 요청 함수 
def fetch_single_url(url):
    response = requests.get(url) # 주어진 URL에 대해 동기 방식으로 GET 요청을 보냄 

    return response.json() # 응답에서 JSON을 추출해 반환 

# ThreadPoolExecutor를 사용해 여러 URL을 병렬로 요청하는 함수 
def fetch_threadpool(urls):
    """병렬 작업은 내부적으로 스레드가 나누어 실행"""
    results = [] # 결과를 저장할 리스트 

    with ThreadPoolExecutor() as executor: # ThreadPoolExecutor 컨텍스트 생성 (자동으로 스레드 풀을 관리)
        # executor.map(): URL 리스트의 각 원소에 대해 fetch_single_url을 병렬로 실행 
        # 결과는 입력 순서대로 반환 
        for data in executor.map(fetch_single_url, urls):
            results.append(data) # 각 요청 결과를 리스트에 저장 

    return results

# aiohttp의 비동기 세션을 이용한 단일 URL을 호출하는 함수 / await을 통해 비동기적으로 응답 대기 
async def fetch_async(session, url):
    # aiohttp의 세션을 사용해 비동기 GET 요청을 보냄 
    async with session.get(url) as response:
        return await response.json() # 응답 데이터를 JSON으로 파싱해 반환 (await으로 비동기 대기)

# aiohttp를 사용해 여러 요청을 동시에 처리하는 함수 
async def fetch_asyncio(urls):
    # aiohttp 클라이언트 세션 생성 (세션 재사용으로 성능 최적화)
    async with aiohttp.ClientSession() as session:
        # 각 URL에 대해 fetch_async 호출 -> Task 리스트로 생성 
        tasks = [fetch_async(session, url) for url in urls]
        
        # asyncio.gather(): 모든 task들을 동시에 실행하고 결과를 리스트로 반환 
        results = await asyncio.gather(*tasks)
        return results

# 실행해서 성능을 측정하기 위한 코드 
if __name__ == "__main__":
    print("▶ 순차 처리")
    start = time.time()
    fetch_sequential(API_URLS)
    print(f"⏱ 실행 시간: {time.time() - start:.2f}초\n")

    print("▶ ThreadPoolExecutor 처리")
    start = time.time()
    fetch_threadpool(API_URLS)
    print(f"⏱ 실행 시간: {time.time() - start:.2f}초\n")

    print("▶ asyncio + aiohttp 처리")
    start = time.time()
    asyncio.run(fetch_asyncio(API_URLS))
    print(f"⏱ 실행 시간: {time.time() - start:.2f}초\n")
